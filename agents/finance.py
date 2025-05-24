from os import getenv
from typing import Literal, cast
from mcp.server.fastmcp import FastMCP
from tools.finance import analyze_company, estimate_valuation


finance_agent = FastMCP(
    "FinanceAgent",
    instructions="You are the best Value Investing expert in the world, analyze businesses financials and calculate "
                 "the intrinsic value using cash-flow methods like discounted cashflow and dividend discount models.",
    dependencies=[analyze_company, estimate_valuation],
)


if __name__ == "__main__":
    TransportType = Literal["stdio", "streamable-http"]
    transport = cast(TransportType, getenv("MCP_TRANSPORT", "stdio"))
    finance_agent.run(transport=transport)