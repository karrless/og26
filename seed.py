import argparse
import asyncio

from core.db import AsyncSessionFactory
from scripts import seed_faq
from scripts.room_input import seed_rooms


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--faq", action="store_true", help="Заполнить FAQ")
    parser.add_argument("--room", action="store_true", help="Загрузить комнаты")

    args = parser.parse_args()

    if not args.faq and not args.room:
        parser.error("Укажите хотя бы один флаг: --faq или --room")

    async with AsyncSessionFactory() as session:
        if args.faq:
            await seed_faq(session)
            print("FAQ успешно заполнен!")

        if args.room:
            count = await seed_rooms(session)
            print(f"Загружено записей о комнатах: {count}")


if __name__ == "__main__":
    asyncio.run(main())