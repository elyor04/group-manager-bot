import pandas as pd
from tortoise import Tortoise, run_async
from app.database import initialize_db, close_db
from app.database.models import UserInfo


async def init_db():
    await initialize_db()

    conn = Tortoise.get_connection("default")
    await conn.execute_query("DROP TABLE IF EXISTS UserInfos")

    await Tortoise.generate_schemas()


async def import_data():
    csv_file = "data/sqlite.csv"
    df = pd.read_csv(csv_file)

    await init_db()

    users = [
        UserInfo(
            id=row["id"],
            chat_id=row["chat_id"],
            user_id=row["user_id"],
            warnings=row["warnings"],
            muted=row["muted"],
            banned=row["banned"],
            messages=row["messages"],
        )
        for _, row in df.iterrows()
    ]
    await UserInfo.bulk_create(users)

    await close_db()
    print(f"Data from {csv_file} has been written to the database.")


run_async(import_data())
