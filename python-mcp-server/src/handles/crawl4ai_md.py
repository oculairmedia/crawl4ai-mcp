from typing import Dict, Any, Sequence
from mcp import Tool
from mcp.types import TextContent
from .base import BaseHandler, ToolRegistry

class Crawl4aiMd(BaseHandler):
    """Convert webpage content to clean markdown format with content filtering"""
    
    name = "md"
    description = "Convert webpage to clean markdown format with content filtering options"
    
    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Target URL to crawl and convert to markdown"
                    },
                    "c": {
                        "type": "string", 
                        "default": "0",
                        "description": "Cache-bust counter for forcing fresh content"
                    },
                    "f": {
                        "type": "string",
                        "default": "fit", 
                        "enum": ["raw", "fit", "bm25", "llm"],
                        "description": "Content filter strategy: raw, fit, bm25, or llm"
                    },
                    "q": {
                        "type": "string",
                        "description": "Query string for BM25/LLM content filtering"
                    },
                    "provider": {
                        "type": "string",
                        "description": "LLM provider override (e.g., 'anthropic/claude-3-opus')"
                    }
                },
                "required": ["url"]
            }
        )
    
    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:
        """Execute markdown conversion via crawl4ai API"""
        try:
            # Build request for /md endpoint with optional filter parameters
            request_data: Dict[str, Any] = {
                "url": arguments["url"],
            }

            if "f" in arguments:
                request_data["f"] = arguments["f"]
            if "q" in arguments:
                request_data["q"] = arguments["q"]
            if "c" in arguments:
                request_data["c"] = arguments["c"]
            if "provider" in arguments:
                request_data["provider"] = arguments["provider"]

            # Call dedicated /md endpoint to leverage LLM/BM25 filters
            result = await self.call_crawl4ai_api("md", request_data)

            # /md returns a simple object with markdown content
            if isinstance(result, dict):
                content = result.get("markdown", "") or str(result)
            else:
                content = str(result)

            return [TextContent(type="text", text=content)]

        except Exception as e:
            return [TextContent(type="text", text=f"Error converting to markdown: {str(e)}")]

# Register the tool
ToolRegistry.register_tool(Crawl4aiMd())