from fastmcp import Client
import asyncio

# The Client automatically uses StreamableHttpTransport for HTTP URLs
client = Client("http://192.168.1.20:8000/mcp")


async def main():
    async with client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")


if __name__ == '__main__':
    asyncio.run(main())
