# SQLite3 不支持对 CREATE TABLE 和 PRAGMA 中的表名与字段名使用参数化，
# 因此必须使用 Python 字符串格式化。
# 对参数施加 `check_identifier` 可防止 SQL 注入。

import sqlite3
from typing import NamedTuple, Optional, Iterator, Any

DEFAULT_DB_PATH = ':memory:'
CONNECTION: Optional[sqlite3.Connection] = None


class NoConnection(Exception):
    """请调用 connect() 来打开连接。"""


class SchemaMismatch(ValueError):
    """表结构与类不匹配。"""

    def __init__(self, table_name):
        self.table_name = table_name


class NoSuchRecord(LookupError):
    """给定的主键不存在。"""

    def __init__(self, pk):
        self.pk = pk


class UnexpectedMultipleResults(Exception):
    """查询返回了多于 1 行。"""


SQLType = str

TypeMap = dict[type, SQLType]

SQL_TYPES: TypeMap = {
    int: 'INTEGER',
    str: 'TEXT',
    float: 'REAL',
    bytes: 'BLOB',
}


class ColumnSchema(NamedTuple):
    name: str
    sql_type: SQLType


FieldMap = dict[str, type]


def check_identifier(name: str) -> None:
    if not name.isidentifier():
        raise ValueError(f'{name!r} is not an identifier')


def connect(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    global CONNECTION
    CONNECTION = sqlite3.connect(db_path)
    CONNECTION.row_factory = sqlite3.Row
    return CONNECTION


def get_connection() -> sqlite3.Connection:
    if CONNECTION is None:
        raise NoConnection()
    return CONNECTION


def gen_columns_sql(fields: FieldMap) -> Iterator[ColumnSchema]:
    for name, py_type in fields.items():
        check_identifier(name)
        try:
            sql_type = SQL_TYPES[py_type]
        except KeyError as e:
            raise ValueError(f'type {py_type!r} is not supported') from e
        yield ColumnSchema(name, sql_type)


def make_schema_sql(table_name: str, fields: FieldMap) -> str:
    check_identifier(table_name)
    pk = 'pk INTEGER PRIMARY KEY,'
    spcs = ' ' * 4
    columns = ',\n    '.join(
        f'{field_name} {sql_type}'
        for field_name, sql_type in gen_columns_sql(fields)
    )
    return f'CREATE TABLE {table_name} (\n{spcs}{pk}\n{spcs}{columns}\n)'


def create_table(table_name: str, fields: FieldMap) -> None:
    con = get_connection()
    con.execute(make_schema_sql(table_name, fields))


def read_columns_sql(table_name: str) -> list[ColumnSchema]:
    check_identifier(table_name)
    con = get_connection()
    rows = con.execute(f'PRAGMA table_info({table_name!r})')
    return [ColumnSchema(r['name'], r['type']) for r in rows]


def valid_table(table_name: str, fields: FieldMap) -> bool:
    table_columns = read_columns_sql(table_name)
    return set(gen_columns_sql(fields)) <= set(table_columns)


def ensure_table(table_name: str, fields: FieldMap) -> None:
    table_columns = read_columns_sql(table_name)
    if len(table_columns) == 0:
        create_table(table_name, fields)
    if not valid_table(table_name, fields):
        raise SchemaMismatch(table_name)


def insert_record(table_name: str, data: dict[str, Any]) -> int:
    check_identifier(table_name)
    con = get_connection()
    placeholders = ', '.join(['?'] * len(data))
    sql = f'INSERT INTO {table_name} VALUES (NULL, {placeholders})'
    cursor = con.execute(sql, tuple(data.values()))
    pk = cursor.lastrowid
    con.commit()
    cursor.close()
    return pk


def fetch_record(table_name: str, pk: int) -> sqlite3.Row:
    check_identifier(table_name)
    con = get_connection()
    sql = f'SELECT * FROM {table_name} WHERE pk = ? LIMIT 2'
    result = list(con.execute(sql, (pk,)))
    if len(result) == 0:
        raise NoSuchRecord(pk)
    elif len(result) == 1:
        return result[0]
    else:
        raise UnexpectedMultipleResults()


def update_record(
    table_name: str, pk: int, data: dict[str, Any]
) -> tuple[str, tuple[Any, ...]]:
    check_identifier(table_name)
    con = get_connection()
    names = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    values = tuple(data.values()) + (pk,)
    sql = f'UPDATE {table_name} SET ({names}) = ({placeholders}) WHERE pk = ?'
    con.execute(sql, values)
    con.commit()
    return sql, values


def delete_record(table_name: str, pk: int) -> sqlite3.Cursor:
    con = get_connection()
    check_identifier(table_name)
    sql = f'DELETE FROM {table_name} WHERE pk = ?'
    return con.execute(sql, (pk,))
