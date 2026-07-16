from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather-hw")

@mcp.tool()
def get_forecast(city: str) -> str:
    data = {
        "Kyiv": "18C, partly cloudy",
        "London": "12C, rain",
        "Tokyo": "24C, clear",
    }
    return data.get(city, f"No forecast available for {city}")

@mcp.tool()
def get_air_quality(city: str) -> str:
    data = {
        "Kyiv": "AQI 42 (good)",
        "London": "AQI 58 (moderate)",
        "Tokyo": "AQI 35 (good)",
    }
    return data.get(city, f"AQI unknown for {city}")

if __name__ == "__main__":
    mcp.run(transport="stdio")
