# Crawl4AI MCP Server - Fixed Fork

[![Build and Push Docker Image](https://github.com/oculairmedia/crawl4ai-mcp/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/oculairmedia/crawl4ai-mcp/actions/workflows/docker-publish.yml)

This is a fixed and improved fork of [stgmt/crawl4ai-mcp](https://github.com/stgmt/crawl4ai-mcp) with critical bug fixes and automated Docker image publishing.

## 🐛 Critical Bugs Fixed

This fork fixes several critical bugs in the original MCP server that prevented it from working correctly:

### 1. **Wrong Endpoints Called**
- ❌ **Original**: `md` tool called `/crawl` endpoint instead of `/md`
- ❌ **Original**: `html` tool called `/crawl` endpoint instead of `/html`
- ✅ **Fixed**: Both tools now call their correct specialized endpoints

### 2. **LLM Parameters Ignored**
- ❌ **Original**: LLM filtering parameters (`f`, `q`, `provider`) were not passed to endpoints
- ✅ **Fixed**: All parameters now properly forwarded to enable LLM-powered extraction

### 3. **Import Errors**
- ❌ **Original**: `ask` tool had incorrect import path (`from config.settings`)
- ❌ **Original**: Relative imports broke when running in containers
- ✅ **Fixed**: All imports corrected and tested in containerized environment

### 4. **Containerization Issues**
- ❌ **Original**: Server couldn't run as a module due to import structure
- ✅ **Fixed**: Dockerfile updated to run as Python module with proper imports

## 🚀 Quick Start

### Using Pre-built Image (Recommended)

```bash
docker pull ghcr.io/oculairmedia/crawl4ai-mcp:latest

docker run -d \
  --name crawl4ai-mcp \
  -p 3055:3000 \
  -e CRAWL4AI_ENDPOINT=http://your-crawl4ai-engine:11235 \
  ghcr.io/oculairmedia/crawl4ai-mcp:latest
```

### Using Docker Compose

```yaml
services:
  crawl4ai-mcp:
    image: ghcr.io/oculairmedia/crawl4ai-mcp:latest
    container_name: crawl4ai-mcp-server
    ports:
      - "3055:3000"
    environment:
      - CRAWL4AI_ENDPOINT=http://crawl4ai-engine:11235
      - PORT=3000
    restart: unless-stopped
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

## 📦 Available Images

Images are automatically built and published to GitHub Container Registry:

- **Latest stable**: `ghcr.io/oculairmedia/crawl4ai-mcp:latest`
- **Tagged versions**: `ghcr.io/oculairmedia/crawl4ai-mcp:v1.0.0`
- **Commit-specific**: `ghcr.io/oculairmedia/crawl4ai-mcp:sha-abc123`

**Multi-platform support:**
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM, Apple Silicon)

## 🛠️ Available Tools

The MCP server provides these tools to AI agents:

- `md` - Extract markdown content from webpages ✅ **FIXED**
- `html` - Get raw HTML content ✅ **FIXED**
- `screenshot` - Take webpage screenshots
- `pdf` - Convert webpages to PDF
- `execute_js` - Execute JavaScript on pages
- `crawl` - Full web crawling with extraction
- `ask` - LLM-powered question answering ✅ **FIXED**

## 🔧 Configuration

### Environment Variables

- `CRAWL4AI_ENDPOINT` - URL of Crawl4AI engine (default: `http://localhost:11235`)
- `PORT` - Server port (default: `3000`)
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR (default: `INFO`)

### LLM Configuration

The server supports LLM-powered extraction when connected to a Crawl4AI engine with LLM configured:

```yaml
services:
  crawl4ai-engine:
    image: unclecode/crawl4ai:0.7.4
    environment:
      - OPENAI_API_KEY=sk-your-key
      - OPENAI_BASE_URL=https://api.openai.com/v1
      - LLM_PROVIDER=openai/gpt-4
```

Or use OpenAI-compatible endpoints (like LiteLLM):

```yaml
environment:
  - OPENAI_API_KEY=dummy-key
  - OPENAI_BASE_URL=http://your-llm-proxy:8082/v1
  - LLM_PROVIDER=openai/sonnet-4-5
```

## 📝 Example Usage

### With MCP Client

```typescript
// List available tools
const tools = await mcp.listTools();

// Extract markdown with LLM filtering
const result = await mcp.callTool("md", {
  url: "https://example.com",
  f: true,              // Enable LLM filtering
  q: "Extract main article content",
  provider: "openai/gpt-4"
});

// Get HTML content
const html = await mcp.callTool("html", {
  url: "https://example.com"
});

// Ask questions about webpage
const answer = await mcp.callTool("ask", {
  url: "https://example.com",
  question: "What is this page about?"
});
```

## 🏗️ Building Locally

```bash
# Clone the repository
git clone https://github.com/oculairmedia/crawl4ai-mcp.git
cd crawl4ai-mcp/python-mcp-server

# Build the image
docker build -t crawl4ai-mcp:local .

# Run locally
docker run -p 3000:3000 \
  -e CRAWL4AI_ENDPOINT=http://localhost:11235 \
  crawl4ai-mcp:local
```

## 🧪 Testing

```bash
cd python-mcp-server

# Run tests
CRAWL4AI_ENDPOINT=http://localhost:11235 pytest

# Check specific handler
pytest tests/test_handlers.py -k test_md_handler
```

## 📊 Changes from Original

| Component | Original | Fixed |
|-----------|----------|-------|
| `md` endpoint | ❌ `/crawl` | ✅ `/md` |
| `html` endpoint | ❌ `/crawl` | ✅ `/html` |
| LLM parameters | ❌ Ignored | ✅ Passed through |
| Module imports | ❌ Broken | ✅ Working |
| Container deployment | ❌ Failed | ✅ Working |
| GitHub Actions | ❌ None | ✅ Auto-build |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Same as original repository - check original for license information.

## 🙏 Credits

- Original MCP server: [stgmt/crawl4ai-mcp](https://github.com/stgmt/crawl4ai-mcp)
- Crawl4AI engine: [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai)
- Bug fixes and improvements by [oculairmedia](https://github.com/oculairmedia)

## 🔗 Links

- **GitHub Repository**: https://github.com/oculairmedia/crawl4ai-mcp
- **Docker Images**: https://github.com/oculairmedia/crawl4ai-mcp/pkgs/container/crawl4ai-mcp
- **GitHub Actions**: https://github.com/oculairmedia/crawl4ai-mcp/actions
- **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Original Repository**: https://github.com/stgmt/crawl4ai-mcp

## 📮 Support

For issues and questions:
- Open an issue: https://github.com/oculairmedia/crawl4ai-mcp/issues
- Original issues: https://github.com/stgmt/crawl4ai-mcp/issues

---

**Note**: This is an independent fork with fixes. Consider submitting these fixes as a PR to the original repository.
