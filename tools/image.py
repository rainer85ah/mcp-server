from PIL import Image
from agents.server import mcp
from mcp.server.fastmcp import Context
from mcp.server.fastmcp import Image as MCPImage


@mcp.tool()
def create_thumbnail(image_path: str) -> MCPImage:
    """Create a thumbnail from an image"""
    img = Image.open(image_path)
    img.thumbnail((100, 100))
    return MCPImage(data=img.tobytes(), format="png")


@mcp.tool()
async def long_task(files: list[str], ctx: Context) -> str:
    """Process multiple files with progress tracking"""
    for i, file in enumerate(files):
        await ctx.info(f"Processing {file}")
        await ctx.report_progress(i, len(files))
        data, mime_type = await ctx.read_resource(f"file://{file}")
    return "Processing complete"