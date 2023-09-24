from datetime import datetime
from typing import Dict, Optional

from aiogoogle import Aiogoogle

from app.api.exceptions import InvalidSizeTable
from app.core.config import settings
from app.models.charity_project import CharityProject

FORMAT = "%Y/%m/%d %H:%M:%S"

SHEETS_ROWS_COUNT = 100

SHEETS_COLUMN_COUNT = 11

TABLE_NAME = 'Отчет от {}'

SPREADSHEET_BODY = dict(
    properties=dict(
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=SHEETS_ROWS_COUNT,
            columnCount=SHEETS_COLUMN_COUNT,
        )
    ))]
)

HEADER = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(
    wrapper_services: Aiogoogle,
    spreadsheet_body: Optional[Dict] = None
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    if not spreadsheet_body:
        spreadsheet_body = SPREADSHEET_BODY.copy()
    spreadsheet_body['properties']['title'] = TABLE_NAME.format(
        str(now_date_time))
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheetid: str,
        projects: list[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_head = HEADER.copy()
    table_head[0].append(now_date_time)
    table_values = [
        *table_head,
        *[list(map(str, project.values())) for project in projects]
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    table_rows = len(table_values)
    if table_rows > SHEETS_ROWS_COUNT:
        raise InvalidSizeTable(
            f'Количество строк в отчете больше {SHEETS_ROWS_COUNT}.')

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=f'A1:C{table_rows}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
