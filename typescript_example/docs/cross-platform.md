# Cross-Platform Development Guide

## Overview

This TypeScript RAG system is designed to work seamlessly across Windows, macOS, and Linux. This guide covers platform-specific considerations and best practices.

## Platform Compatibility Matrix

| Feature | Windows | macOS | Linux | Notes |
|---------|---------|-------|-------|-------|
| Node.js 18+ | ✅ | ✅ | ✅ | All platforms supported |
| Ollama | ✅ | ✅ | ✅ | Native installers available |
| File System | ✅ | ✅ | ✅ | Path handling normalized |
| GPU Support | ✅ CUDA | ✅ Metal | ✅ CUDA | Platform-specific |
| Shell Scripts | PowerShell | Bash | Bash | Different syntax |
| Package Manager | npm/yarn | npm/yarn | npm/yarn | Same everywhere |

## Writing Cross-Platform Code

### 1. File Paths

Always use Node.js path module:

```typescript
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

// Cross-platform path handling
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Good: Platform-agnostic
const configPath = path.join(__dirname, "..", "config", "settings.json");

// Bad: Platform-specific
const badPath = __dirname + "/../config/settings.json";  // Unix only
const badPath2 = __dirname + "\\..\\config\\settings.json";  // Windows only
```

### 2. Line Endings

Configure Git and editors:

```bash
# .gitattributes
* text=auto eol=lf
*.ts text eol=lf
*.json text eol=lf
*.md text eol=lf

# Windows-specific
*.ps1 text eol=crlf
*.bat text eol=crlf

# Unix-specific  
*.sh text eol=lf
```

### 3. Environment Variables

Handle platform differences:

```typescript
import { platform } from "os";

// Cross-platform environment handling
function getDataDir(): string {
  if (platform() === "win32") {
    return process.env.APPDATA || path.join(os.homedir(), "AppData", "Roaming");
  } else if (platform() === "darwin") {
    return path.join(os.homedir(), "Library", "Application Support");
  } else {
    return process.env.XDG_DATA_HOME || path.join(os.homedir(), ".local", "share");
  }
}

// Use cross-platform temp directory
import { tmpdir } from "os";
const tempFile = path.join(tmpdir(), "rag-temp.json");
```

### 4. Process Management

Handle process signals correctly:

```typescript
// Cross-platform graceful shutdown
const shutdown = async () => {
  console.log("Shutting down...");
  await cleanup();
  process.exit(0);
};

// Windows
if (platform() === "win32") {
  const readline = require("readline");
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  rl.on("SIGINT", shutdown);
}

// Unix-like systems
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
```

## Platform-Specific Scripts

### Package.json Scripts

```json
{
  "scripts": {
    "start": "node dist/index.js",
    "dev": "tsx watch src/example.ts",
    "build": "tsc",
    "test": "tsx src/test.ts",
    
    // Platform-specific
    "setup:windows": "powershell -ExecutionPolicy Bypass -File ./scripts/setup.ps1",
    "setup:unix": "bash ./scripts/setup.sh",
    "setup": "node scripts/setup.js",  // Cross-platform Node.js script
    
    // Use cross-env for environment variables
    "dev:debug": "cross-env DEBUG=* tsx src/example.ts",
    "test:ci": "cross-env CI=true npm test"
  }
}
```

### Cross-Platform Setup Script

`scripts/setup.js`:

```javascript
#!/usr/bin/env node

const { exec } = require("child_process");
const { platform } = require("os");
const { promisify } = require("util");

const execAsync = promisify(exec);

async function setup() {
  console.log(`Setting up for ${platform()}...`);
  
  try {
    // Check Node version
    const nodeVersion = process.version;
    if (!nodeVersion.match(/^v(1[89]|[2-9]\d)/)) {
      throw new Error("Node.js 18+ required");
    }
    
    // Install Ollama
    if (platform() === "win32") {
      await execAsync("winget install Ollama.Ollama");
    } else if (platform() === "darwin") {
      await execAsync("brew install ollama");
    } else {
      await execAsync("curl -fsSL https://ollama.ai/install.sh | sh");
    }
    
    // Start Ollama
    if (platform() === "win32") {
      exec("start ollama serve");
    } else {
      exec("ollama serve &");
    }
    
    // Wait for Ollama to start
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Pull models
    await execAsync("ollama pull tinyllama");
    await execAsync("ollama pull nomic-embed-text");
    
    console.log("✅ Setup complete!");
  } catch (error) {
    console.error("❌ Setup failed:", error.message);
    process.exit(1);
  }
}

setup();
```

## Docker for Ultimate Portability

### Multi-Stage Dockerfile

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY src ./src

# Build
RUN npm run build

# Runtime stage
FROM node:20-alpine

# Install Ollama
RUN apk add --no-cache curl bash
RUN curl -fsSL https://ollama.ai/install.sh | sh

WORKDIR /app

# Copy built app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

# Install production dependencies only
RUN npm ci --production

# Create data directory
RUN mkdir -p /data

# Environment variables
ENV NODE_ENV=production
ENV OLLAMA_HOST=0.0.0.0:11434
ENV DATA_DIR=/data

# Expose ports
EXPOSE 3000 11434

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:11434/api/tags', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

# Start script
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
```

### Docker Compose

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  rag:
    build: .
    ports:
      - "3000:3000"
      - "11434:11434"
    volumes:
      - ./data:/data
      - ollama-models:/root/.ollama
    environment:
      - NODE_ENV=production
      - OLLAMA_NUM_THREADS=4
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G

volumes:
  ollama-models:
```

## CI/CD Considerations

### GitHub Actions Workflow

`.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [18, 20]
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Build
        run: npm run build
      
      - name: Test
        run: npm test
        env:
          CI: true
```

## Platform-Specific Optimizations

### Windows Optimizations

```typescript
// Windows-specific performance tuning
if (platform() === "win32") {
  // Use Windows-specific APIs
  const { exec } = require("child_process");
  
  // Increase process priority
  exec(`wmic process where processid=${process.pid} CALL setpriority 128`);
  
  // Use Windows temp directory
  process.env.TEMP = process.env.TEMP || "C:\\Temp";
}
```

### macOS Optimizations

```typescript
// macOS-specific optimizations
if (platform() === "darwin") {
  // Use Metal Performance Shaders if available
  process.env.OLLAMA_USE_METAL = "1";
  
  // macOS file watching
  const { FSWatcher } = require("fs");
  // Use native FSEvents for better performance
}
```

### Linux Optimizations

```typescript
// Linux-specific optimizations
if (platform() === "linux") {
  // Check for GPU support
  const hasNvidia = fs.existsSync("/usr/bin/nvidia-smi");
  if (hasNvidia) {
    process.env.OLLAMA_USE_CUDA = "1";
  }
  
  // Use Linux-specific memory management
  process.env.MALLOC_ARENA_MAX = "2";
}
```

## Development Tools

### Cross-Platform Terminal

```typescript
// Detect and use appropriate terminal
import { platform } from "os";
import { spawn } from "child_process";

function openTerminal(command: string) {
  const isWindows = platform() === "win32";
  const isMac = platform() === "darwin";
  
  if (isWindows) {
    spawn("cmd", ["/c", "start", "cmd", "/k", command]);
  } else if (isMac) {
    spawn("osascript", ["-e", `tell app "Terminal" to do script "${command}"`]);
  } else {
    spawn("gnome-terminal", ["--", "bash", "-c", command]);
  }
}
```

### File Watcher

```typescript
// Cross-platform file watching
import { watch } from "fs";
import { platform } from "os";

function watchFiles(dir: string, callback: (event: string, filename: string) => void) {
  const options = {
    recursive: true,
    // Windows doesn't support persistent
    persistent: platform() !== "win32"
  };
  
  watch(dir, options, (event, filename) => {
    if (filename) {
      // Normalize path for Windows
      const normalizedPath = filename.replace(/\\/g, "/");
      callback(event, normalizedPath);
    }
  });
}
```

## Testing Across Platforms

### Platform-Specific Tests

```typescript
import { platform } from "os";

describe("Cross-platform tests", () => {
  it("should handle paths correctly", () => {
    const testPath = path.join("dir", "file.txt");
    
    if (platform() === "win32") {
      expect(testPath).toContain("\\");
    } else {
      expect(testPath).toContain("/");
    }
  });
  
  // Skip platform-specific tests
  const itWindows = platform() === "win32" ? it : it.skip;
  const itUnix = platform() !== "win32" ? it : it.skip;
  
  itWindows("Windows-specific test", () => {
    // Windows only
  });
  
  itUnix("Unix-specific test", () => {
    // Unix only
  });
});
```

## Distribution

### Building for Different Platforms

```json
{
  "scripts": {
    "build:windows": "npm run build && pkg . --targets node18-win-x64 --output dist/rag-windows.exe",
    "build:mac": "npm run build && pkg . --targets node18-macos-x64 --output dist/rag-macos",
    "build:linux": "npm run build && pkg . --targets node18-linux-x64 --output dist/rag-linux",
    "build:all": "npm run build:windows && npm run build:mac && npm run build:linux"
  }
}
```

### Electron App (Optional)

```typescript
// main.js - Electron main process
const { app, BrowserWindow } = require("electron");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });
  
  win.loadFile("index.html");
}

app.whenReady().then(createWindow);

// Platform-specific app behavior
if (process.platform === "darwin") {
  app.on("window-all-closed", () => {
    // On macOS, keep app running
  });
} else {
  app.on("window-all-closed", () => {
    app.quit();
  });
}
```

## Best Practices

1. **Always test on all target platforms** before release
2. **Use CI/CD** to automatically test across platforms
3. **Document platform-specific requirements** clearly
4. **Provide platform-specific installation scripts**
5. **Use cross-platform libraries** when possible
6. **Handle errors gracefully** with platform context
7. **Log platform information** for debugging

## Troubleshooting Guide

### Common Cross-Platform Issues

| Issue | Windows | macOS | Linux |
|-------|---------|-------|-------|
| Path separators | Use `path.join()` | Use `path.join()` | Use `path.join()` |
| Line endings | CRLF → LF issues | LF native | LF native |
| Permissions | Run as Admin | Use sudo | Use sudo |
| Ports blocked | Windows Firewall | Check Security settings | Check iptables |
| GPU not detected | Update CUDA | Update Xcode | Install CUDA toolkit |

---

Remember: Write once, test everywhere! 🌍
