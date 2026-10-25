import anyio

from mcp import Client
from mcp.types import TextContent


async def main() -> None:
    async with Client("http://127.0.0.1:8100/mcp") as client:
        tools = await client.list_tools()
        print("TOOLS:", [tool.name for tool in tools.tools])

        result = await client.call_tool(
            "search_products",
            {"query": "laptop for local AI", "limit": 3},
        )
        print("ERROR:", result.is_error)
        print("STRUCTURED:", result.structured_content)
        for block in result.content:
            if isinstance(block, TextContent):
                print("TEXT:", block.text)


if __name__ == "__main__":
    anyio.run(main)
