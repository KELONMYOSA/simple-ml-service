import flet

from src.pages import deposit, login
from src.utils.auth import get_user_info, logout
from src.utils.balance import get_user_balance
from src.utils.task import create_task, get_user_tasks, modelId2cost, modelLabel2id, refresh_table


async def main(page: flet.Page):
    user = await get_user_info(page)
    balance = await get_user_balance(page)
    if user:
        page.appbar.actions = [
            flet.Row(
                controls=[
                    flet.TextButton(
                        text=f"{balance} cu",
                        icon=flet.icons.ACCOUNT_BALANCE_WALLET,
                        on_click=to_deposit,
                    ),
                    flet.Text(
                        value=user["email"],
                        style=flet.TextThemeStyle.BODY_LARGE,
                    ),
                    flet.IconButton(icon=flet.icons.LOGOUT, tooltip="Logout", on_click=logout),
                ],
                spacing=10,
            ),
        ]
    else:
        await login.main(page)
        return

    await page.clean_async()

    user_tasks = await get_user_tasks(page)
    user_tasks_rows = []
    for task in reversed(user_tasks):
        pred = "-"
        if task["prediction"]:
            pred = 1
        elif task["prediction"] is False:
            pred = 0

        user_tasks_rows.append(
            flet.DataRow(
                cells=[
                    flet.DataCell(flet.Text(task["id"])),
                    flet.DataCell(flet.Text(task["model_name"])),
                    flet.DataCell(flet.Text(task["cost"])),
                    flet.DataCell(flet.Text(task["input_data"]["temperature"])),
                    flet.DataCell(flet.Text(task["input_data"]["humidity"])),
                    flet.DataCell(flet.Text(task["input_data"]["CO2CosIRValue"])),
                    flet.DataCell(flet.Text(task["input_data"]["CO2MG811Value"])),
                    flet.DataCell(flet.Text(task["input_data"]["MOX1"])),
                    flet.DataCell(flet.Text(task["input_data"]["MOX2"])),
                    flet.DataCell(flet.Text(task["input_data"]["MOX3"])),
                    flet.DataCell(flet.Text(task["input_data"]["MOX4"])),
                    flet.DataCell(flet.Text(task["input_data"]["COValue"])),
                    flet.DataCell(flet.Text(pred)),
                    flet.DataCell(flet.Text(task["task_result"])),
                ]
            )
        )

    create_task_fields = [
        flet.Dropdown(
            width=250,
            value="Linear Regression (5 cu)",
            options=[
                flet.dropdown.Option("Linear Regression (5 cu)"),
                flet.dropdown.Option("Random Forest (15 cu)"),
                flet.dropdown.Option("Neural Network (30 cu)"),
            ],
        ),
        flet.TextField(label="Temperature", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="Humidity", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="CO2CosIRValue", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="CO2MG811Value", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="MOX1", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="MOX2", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="MOX3", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="MOX4", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.TextField(label="COValue", input_filter=flet.NumbersOnlyInputFilter(), width=135, value="10"),
        flet.ElevatedButton("Predict", width=150, height=50, disabled=True),
    ]

    async def validate_fields(e: flet.ControlEvent) -> None:
        if (
            all([x.value for x in create_task_fields[:-1]])
            and modelId2cost[modelLabel2id[create_task_fields[0].value]] < balance
        ):
            create_task_fields[-1].disabled = False
        else:
            create_task_fields[-1].disabled = True
        await page.update_async()

    for item in create_task_fields[:-1]:
        item.on_change = validate_fields

    async def do_predict(e: flet.ControlEvent) -> None:
        data = {
            "model_id": modelLabel2id[create_task_fields[0].value],
            "input_data": {
                "temperature": create_task_fields[1].value,
                "humidity": create_task_fields[2].value,
                "CO2CosIRValue": create_task_fields[3].value,
                "CO2MG811Value": create_task_fields[4].value,
                "MOX1": create_task_fields[5].value,
                "MOX2": create_task_fields[6].value,
                "MOX3": create_task_fields[7].value,
                "MOX4": create_task_fields[8].value,
                "COValue": create_task_fields[9].value,
            },
        }
        await create_task(page, data)

    create_task_fields[-1].on_click = do_predict

    await page.add_async(
        flet.Column(
            controls=[
                flet.Column(height=50),
                flet.Row(controls=create_task_fields, width=page.width * 0.9),
                flet.Row(controls=[flet.Divider()], width=page.width * 0.9),
                flet.Text("History:", style=flet.TextThemeStyle.HEADLINE_SMALL, width=page.width * 0.9),
                flet.Row(controls=[flet.Divider()], width=page.width * 0.9),
                flet.Column(
                    controls=[flet.IconButton(flet.icons.REFRESH, on_click=refresh_table)],
                    width=page.width * 0.9,
                    alignment=flet.alignment.center_right,
                ),
                flet.DataTable(
                    columns=[
                        flet.DataColumn(flet.Text("ID")),
                        flet.DataColumn(flet.Text("Model")),
                        flet.DataColumn(flet.Text("Cost")),
                        flet.DataColumn(flet.Text("Temperature")),
                        flet.DataColumn(flet.Text("Humidity")),
                        flet.DataColumn(flet.Text("CO2CosIRValue")),
                        flet.DataColumn(flet.Text("CO2MG811Value")),
                        flet.DataColumn(flet.Text("MOX1")),
                        flet.DataColumn(flet.Text("MOX2")),
                        flet.DataColumn(flet.Text("MOX3")),
                        flet.DataColumn(flet.Text("MOX4")),
                        flet.DataColumn(flet.Text("COValue")),
                        flet.DataColumn(flet.Text("Prediction")),
                        flet.DataColumn(flet.Text("Status")),
                    ],
                    rows=user_tasks_rows,
                    width=page.width * 0.9,
                ),
            ]
        )
    )


async def to_deposit(e: flet.ControlEvent):
    page = e.page
    await deposit.main(page)
