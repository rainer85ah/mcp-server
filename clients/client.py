import asyncio
from mcp import McpError
from fastmcp import Client
from fastmcp.exceptions import ClientError


async def main():

    async with Client("http://192.168.1.20:8000/mcp") as client:
        await client.ping()
        print(f"Client connected: {client.is_connected()}")

        # Make MCP calls within the context
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        resources = await client.list_resources()
        print(f"Available resources: {resources}")
        templates = await client.list_resource_templates()
        print(f"Available templates: {templates}")
        prompts = await client.list_prompts()
        print(f"Available prompts: {prompts}")

        try:
            result = await client.call_tool(name="chat_ask_question_tool", arguments={"question": "Why is the sky blue?"})
            print("Inference result:", result[0].text)
        except ClientError as e:
            print(f"Tool call failed: {e}")
        except McpError as e:
            print(f"The task timed out: {e}")
        except ConnectionError as e:
            print(f"Connection failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}.")

    # Connection is closed automatically here
    print(f"Client connected: {client.is_connected()}")


if __name__ == "__main__":
        asyncio.run(main())
