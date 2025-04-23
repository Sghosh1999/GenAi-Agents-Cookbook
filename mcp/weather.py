"""
This script implements a weather service using the FastMCP framework. It provides tools to fetch 
weather alerts and forecasts for specific locations in the United States by interacting with the 
National Weather Service (NWS) API.

Key Features:
1. **Weather Alerts**:
   - Fetches active weather alerts for a given US state using the NWS API.
   - Formats the alert data into a human-readable string.

2. **Weather Forecast**:
   - Retrieves weather forecast data for a specific latitude and longitude.
   - Formats the forecast data into a readable format, showing details for the next 5 periods.

3. **Asynchronous HTTP Requests**:
   - Uses the `httpx` library to make asynchronous HTTP requests to the NWS API.
   - Includes proper error handling to manage API failures or invalid responses.

4. **FastMCP Integration**:
   - The script uses the FastMCP framework to expose the weather alert and forecast functionalities 
     as tools that can be accessed via the MCP server.

Constants:
- `NWS_API_BASE`: Base URL for the National Weather Service API.
- `USER_AGENT`: Custom user agent string for API requests.

Functions:
- `make_nws_request`: Makes an asynchronous HTTP GET request to the NWS API and handles errors.
- `format_alert`: Formats a weather alert feature into a readable string.
- `get_alerts`: Fetches and formats active weather alerts for a given US state.
- `get_forecast`: Fetches and formats the weather forecast for a specific location.

Usage:
- The script initializes a FastMCP server named "weather".
- The `get_alerts` and `get_forecast` functions are registered as tools in the MCP server.
- The server runs using the Server-Sent Events (SSE) transport mechanism.

To run the script:
- Execute the file directly. The MCP server will start and expose the weather tools for use.
"""

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""


@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # First get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    return "\n---\n".join(forecasts)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='sse')