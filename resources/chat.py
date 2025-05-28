from fastmcp import Context
from main import mcp


@mcp.resource("local://{path}")
async def read_local(path: str, ctx: Context):
    return await ctx.local_fs.download(path)

@mcp.resource("s3://{path}")
async def read_s3(path: str, ctx: Context):
    return await ctx.s3.download(path)

@mcp.resource("http://{url:path}")
async def fetch_api(url: str, ctx: Context):
    return await ctx.api.fetch(f"http://{url}")

@mcp.resource("scrape://{url:path}")
async def fetch_webpage(url: str, ctx: Context):
    return await ctx.scraper.fetch(f"https://{url}")
