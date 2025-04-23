from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

# Defining a tool (function) for addition
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    print("Math server is running...")  # Added message to indicate the server is running
    # Running the MCP server with "stdio" as the transport mechanism
    mcp.run(transport="stdio")