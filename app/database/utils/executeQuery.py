from tortoise import Tortoise


async def execute_query(query: str, query_params: list = None, connection_name: str = "default"):
    connection = Tortoise.get_connection(connection_name)
    _, rows = await connection.execute_query(query, query_params)
    return [{key: row[key] for key in row.keys()} for row in rows]
