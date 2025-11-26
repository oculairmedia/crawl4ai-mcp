# Deployment Guide

## Automated Docker Image Publishing

This repository uses GitHub Actions to automatically build and publish Docker images to GitHub Container Registry (GHCR).

### Automatic Builds

Images are automatically built and published when:
- **Push to `main` branch** - Creates `ghcr.io/oculairmedia/crawl4ai-mcp:latest`
- **Creating version tags** (e.g., `v1.0.0`) - Creates versioned images
- **Manual workflow dispatch** - Can be triggered manually from GitHub Actions tab

### Available Image Tags

Images are published at: `ghcr.io/oculairmedia/crawl4ai-mcp`

Available tags:
- `latest` - Latest build from main branch
- `main` - Same as latest
- `v1.0.0` - Specific version tags (when created)
- `sha-abc123` - Commit-specific builds

### Using the Published Image

#### In Docker Compose

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
```

#### Pull Directly

```bash
docker pull ghcr.io/oculairmedia/crawl4ai-mcp:latest
```

#### Run Standalone

```bash
docker run -d \
  --name crawl4ai-mcp-server \
  -p 3055:3000 \
  -e CRAWL4AI_ENDPOINT=http://crawl4ai-engine:11235 \
  ghcr.io/oculairmedia/crawl4ai-mcp:latest
```

### Multi-Platform Support

The GitHub Action builds images for multiple architectures:
- `linux/amd64` - Standard x86_64 servers
- `linux/arm64` - ARM servers (Apple Silicon, AWS Graviton, etc.)

Docker will automatically pull the correct architecture for your system.

### Build Cache

The workflow uses GitHub Actions cache to speed up builds:
- Layer cache is preserved between builds
- Rebuilds are significantly faster
- Cache is automatically managed by GitHub

### Viewing Build Status

Check the status of builds at:
https://github.com/oculairmedia/crawl4ai-mcp/actions

### Building Locally

To build the image locally instead of using the published version:

```bash
cd python-mcp-server
docker build -t crawl4ai-mcp:local .
```

Or use docker-compose with local build:

```yaml
services:
  crawl4ai-mcp:
    build:
      context: ./python-mcp-server
      dockerfile: Dockerfile
```

### Triggering Manual Builds

1. Go to: https://github.com/oculairmedia/crawl4ai-mcp/actions
2. Select "Build and Push Docker Image" workflow
3. Click "Run workflow"
4. Select branch (usually `main`)
5. Click "Run workflow" button

### Creating Version Releases

To create a versioned release:

```bash
# Tag the commit
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push the tag
git push origin v1.0.0
```

This will automatically build and publish:
- `ghcr.io/oculairmedia/crawl4ai-mcp:v1.0.0`
- `ghcr.io/oculairmedia/crawl4ai-mcp:1.0`
- `ghcr.io/oculairmedia/crawl4ai-mcp:1`
- `ghcr.io/oculairmedia/crawl4ai-mcp:latest`

### Troubleshooting

#### Image Pull Fails

If you get permission errors pulling the image:

```bash
# Login to GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

The image is public, so this shouldn't be necessary unless you're hitting rate limits.

#### Build Fails

Check the Actions tab for build logs:
https://github.com/oculairmedia/crawl4ai-mcp/actions

Common issues:
- Dockerfile syntax errors
- Missing dependencies in requirements.txt
- File path issues in COPY commands

#### Old Image Cached

Force pull the latest version:

```bash
docker pull --no-cache ghcr.io/oculairmedia/crawl4ai-mcp:latest
```

### Security

The GitHub Action uses `GITHUB_TOKEN` which is automatically provided by GitHub:
- No manual secrets configuration needed
- Token has minimal permissions (contents:read, packages:write)
- Token is automatically scoped to the repository

### Image Metadata

Each published image includes labels with:
- Build date and time
- Git commit SHA
- Git repository URL
- GitHub workflow URL
- Version information (for tagged builds)

View metadata:

```bash
docker inspect ghcr.io/oculairmedia/crawl4ai-mcp:latest
```
