import asyncio

from core.db import AsyncSessionFactory
from scripts import seed_faq


async def main():
    async with AsyncSessionFactory() as session:
        await seed_faq(session)
        print("FAQ успешно заполнен!")


if __name__ == "__main__":
    asyncio.run(main())