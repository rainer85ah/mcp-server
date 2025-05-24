from agents.finance import finance_agent


@finance_agent.tool()
def analyze_company(ticker: str) -> str:
    """Perform a mock qualitative analysis on a company given its ticker."""
    return f"Company {ticker.upper()} shows consistent revenue growth, moderate debt levels, and high return on equity."


@finance_agent.tool()
def estimate_valuation(ticker: str, earnings: float, growth_rate: float, discount_rate: float = 0.10) -> float:
    """
    Estimate intrinsic value using a simplified DCF model.
    Formula: Value = Earnings * (1 + g) / (r - g)
    """
    g = growth_rate
    r = discount_rate
    if g >= r:
        return -1  # invalid input: growth rate must be < discount rate
    return round(earnings * (1 + g) / (r - g), 2)
