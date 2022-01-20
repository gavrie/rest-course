import httpx
import pytest
from anyio import create_task_group

pytestmark = pytest.mark.anyio


async def test_async_client():
    async def operation(num):
        print(f"Start operation {num}")
        await client.get("https://httpbin.org/delay/1")
        print(f"End operation {num}")

    async with httpx.AsyncClient() as client:

        async with create_task_group() as tg:
            for num in range(5):
                tg.start_soon(operation, num)
