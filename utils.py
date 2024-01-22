from sqlalchemy import text
from typing import Union, Dict, Tuple

import pandas as pd

from session import get_session


def format_value(value):
    if isinstance(value, str):
        return f"'{value}'"
    return f"{value}"


def data_to_line(
    data: Dict[str, Union[str, int, float]],
    sep: str = ','
) -> str:
    lines = []
    for column, value in data.items():
        lines.append(f"{column} = {format_value(value)}")
    return f"{sep}".join(lines)


async def delete_row(
    table: str,
    conditions: Dict[str, int] = None,
    schema: str = "public",
) -> None:
    """
    Удаление записи из таблицы по условию
    """
    condition_line = ""
    if conditions is not None:
        condition_line = "WHERE " + data_to_line(data=conditions, sep=" AND ")
    with get_session() as session:
        session.execute(
            text(
                f"""
                DELETE FROM {schema}.{table}
                {condition_line}
                """
            )
        )
        session.commit()


async def update_row(
    data: Dict[str, Union[str, int, float]],
    table: str,
    conditions: Dict[str, int] = None,
    schema: str = "public",
) -> None:
    """
    Обновление записи по условию
    """
    condition_line = ""
    if conditions is not None:
        condition_line = "WHERE " + data_to_line(data=conditions, sep=" AND ")
    data_line = data_to_line(data=data)
    with get_session() as session:
        session.execute(
            text(
                f"""
                UPDATE {schema}.{table}
                SET {data_line}
                {condition_line}
                """
            )
        )
        session.commit()


async def get_rows(
    table: str,
    conditions: Dict[str, int] = None,
    schema: str = "public",
) -> pd.DataFrame:
    """
    Получение записей из таблицы по условиям
    """
    condition_line = ""
    if conditions is not None:
        condition_line = "WHERE " + data_to_line(data=conditions, sep=" AND ")
    with get_session() as session:
        rows = pd.read_sql(
            f"""
            SELECT *
            FROM {schema}.{table}
            {condition_line}
            """,
            session.get_bind()
        )
    return rows


async def create_row(
    data: Dict[str, Union[str, int, float]],
    table: str,
    schema: str = "public",
) -> None:
    """
    Создание записи в таблицу
    """
    with get_session() as session:
        values = list(map(format_value, data.values()))
        session.execute(
            text(
                f"""
                INSERT INTO {schema}.{table} ({", ".join(data)})
                VALUES ({", ".join(values)})
                """
            )
        )
        session.commit()