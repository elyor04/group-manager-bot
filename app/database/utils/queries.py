from app.database.utils import execute_query


async def get_chat_ids(limit: int = None, offset: int = None):
    queryParams = []

    def addSqlParam(param):
        if (param is not None) and (param != ""):
            queryParams.append(param)
            return True
        return False

    query = f"""
        SELECT DISTINCT
            T0."chat_id"
        FROM
            UserInfos T0
        WHERE
            T0."chat_id" <> T0."user_id"
        ORDER BY
            T0."id" ASC
        {'LIMIT ?' if addSqlParam(limit) else ''}
        {'OFFSET ?' if addSqlParam(offset) else ''}
    """

    data = await execute_query(query, queryParams or None)
    return [d["chat_id"] for d in data]


async def get_user_ids(limit: int = None, offset: int = None):
    queryParams = []

    def addSqlParam(param):
        if (param is not None) and (param != ""):
            queryParams.append(param)
            return True
        return False

    query = f"""
        SELECT DISTINCT
            T0."chat_id"
        FROM
            UserInfos T0
        WHERE
            T0."chat_id" = T0."user_id"
        ORDER BY
            T0."id" ASC
        {'LIMIT ?' if addSqlParam(limit) else ''}
        {'OFFSET ?' if addSqlParam(offset) else ''}
    """

    data = await execute_query(query, queryParams or None)
    return [d["chat_id"] for d in data]
