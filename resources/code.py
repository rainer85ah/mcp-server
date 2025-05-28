from data_sources.github_fetcher import GitHubFetcher
from main import mcp
from tools.code import analyze_structure


github = GitHubFetcher(token="ghp_XXXX")  # store in env


@mcp.resource("github://{owner}/{repo}")
async def analyze_repo(owner: str, repo: str) -> dict:
    contents = await github.get_repo_contents(owner, repo)
    analysis = analyze_structure(contents)
    return {
        "repo": f"{owner}/{repo}",
        "analysis": analysis
    }
