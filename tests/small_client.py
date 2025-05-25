from fastmcp import Client
import asyncio


async def main():
    async with Client("http://192.168.1.20:8000/mcp") as client:
        await client.ping()
        tools = await client.list_tools()
        print(f"Available tools: {tools}")


if __name__ == '__main__':
    asyncio.run(main())
