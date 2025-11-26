from typing import Dict, Any, Sequence
from mcp import Tool
from mcp.types import TextContent
from .base import BaseHandler, ToolRegistry

class Crawl4aiHtml(BaseHandler):
    """Get preprocessed HTML structure for schema extraction"""
    
    name = "html"
    description = "Get cleaned and preprocessed HTML content for further processing"
    
    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL to crawl and extract HTML from"
                    }
                },
                "required": ["url"]
            }
        )
    
    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Execute HTML extraction via crawl4ai API"""
        try:
            # Use dedicated /html endpoint to fetch cleaned HTML
            request_data = {
                "url": arguments["url"],
            }

            result = await self.call_crawl4ai_api("html", request_data)

            if isinstance(result, dict):
                content = result.get("cleaned_html", result.get("html", str(result)))
            else:
                content = str(result)

            return [TextContent(type="text", text=str(content) if content is not None else "")]

        except Exception as e:
            return [TextContent(type="text", text=f"Error extracting HTML: {str(e)}")]

# Register the tool
ToolRegistry.register_tool(Crawl4aiHtml())