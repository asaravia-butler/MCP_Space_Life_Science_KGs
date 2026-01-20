# MCP Server Configuration Guide

## Overview

To use this MCP server with Claude Desktop, you need to add it to your `claude_desktop_config.json` file. This guide covers both development (local) and production (PyPI) setups.

---

## Quick Start

### Option 1: Development Mode (Local Installation)

Use this when developing or testing the server locally.

#### 1. Install in Development Mode

```bash
git clone https://github.com/YOUR-USERNAME/MCP_Space_Life_Science_KGs.git
cd MCP_Space_Life_Science_KGs
pip install -e .
```

#### 2. Configure Claude Desktop

**Location of config file:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Add to your `claude_desktop_config.json`:**

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "python",
      "args": [
        "-m",
        "mcp_space_life_sciences.server"
      ],
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "your_genelab_password",
        "PRIMEKG_NEO4J_URI": "bolt://localhost:7688",
        "PRIMEKG_NEO4J_USER": "neo4j",
        "PRIMEKG_NEO4J_PASSWORD": "your_primekg_password"
      }
    }
  }
}
```

**Note**: SPOKE-OKN uses a public SPARQL endpoint, so no credentials are needed for it.

---

### Option 2: Production Mode (After PyPI Deployment)

Use this after the package is published to PyPI.

#### 1. Install from PyPI

```bash
pip install mcp-space-life-sciences
```

#### 2. Configure Claude Desktop

**Add to your `claude_desktop_config.json`:**

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "your_genelab_password",
        "PRIMEKG_NEO4J_URI": "bolt://localhost:7688",
        "PRIMEKG_NEO4J_USER": "neo4j",
        "PRIMEKG_NEO4J_PASSWORD": "your_primekg_password"
      }
    }
  }
}
```

---

## Alternative: Using PrimeKG Data Files (No Neo4j)

If you don't have Neo4j set up for PrimeKG, you can use CSV data files instead:

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "your_genelab_password",
        "PRIMEKG_DATA_PATH": "/path/to/primekg/data/folder"
      }
    }
  }
}
```

Download PrimeKG data from: https://zitniklab.hms.harvard.edu/projects/PrimeKG/

---

## Configuration Examples

### Example 1: All Three KGs via Neo4j

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "genelab123",
        "PRIMEKG_NEO4J_URI": "bolt://localhost:7688",
        "PRIMEKG_NEO4J_USER": "neo4j",
        "PRIMEKG_NEO4J_PASSWORD": "primekg456"
      }
    }
  }
}
```

### Example 2: GeneLab + PrimeKG Files + SPOKE-OKN

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "genelab123",
        "PRIMEKG_DATA_PATH": "/Users/yourname/data/primekg"
      }
    }
  }
}
```

### Example 3: Development Mode with Virtual Environment

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "/Users/yourname/projects/MCP_Space_Life_Science_KGs/venv/bin/python",
      "args": [
        "-m",
        "mcp_space_life_sciences.server"
      ],
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "password",
        "PRIMEKG_DATA_PATH": "/Users/yourname/data/primekg"
      }
    }
  }
}
```

---

## Multiple MCP Servers

You can run this alongside other MCP servers. Here's an example with multiple servers:

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "genelab123",
        "PRIMEKG_DATA_PATH": "/Users/yourname/data/primekg"
      }
    },
    "mcp-genelab": {
      "command": "mcp-genelab",
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "genelab123"
      }
    },
    "mcp-proto-okn": {
      "command": "mcp-proto-okn"
    }
  }
}
```

**Note**: This integrated server combines functionality from all three, so you typically don't need the individual servers running simultaneously.

---

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GENELAB_NEO4J_URI` | Yes* | GeneLab Neo4j connection | `bolt://localhost:7687` |
| `GENELAB_NEO4J_USER` | Yes* | GeneLab Neo4j username | `neo4j` |
| `GENELAB_NEO4J_PASSWORD` | Yes* | GeneLab Neo4j password | `your_password` |
| `PRIMEKG_NEO4J_URI` | No** | PrimeKG Neo4j connection | `bolt://localhost:7688` |
| `PRIMEKG_NEO4J_USER` | No** | PrimeKG Neo4j username | `neo4j` |
| `PRIMEKG_NEO4J_PASSWORD` | No** | PrimeKG Neo4j password | `your_password` |
| `PRIMEKG_DATA_PATH` | No** | PrimeKG CSV data directory | `/path/to/primekg/data` |

\* Required for GeneLab functionality  
\** Either Neo4j credentials OR data path required for PrimeKG

**SPOKE-OKN** requires no configuration - it uses the public endpoint automatically.

---

## Verifying Installation

After configuring, restart Claude Desktop and verify the server is running:

### Method 1: Check Claude Desktop Logs

**macOS/Linux:**
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

**Windows:**
```powershell
Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Wait
```

Look for:
```
[mcp-space-life-sciences] Server started successfully
[mcp-space-life-sciences] Connected to GeneLab Neo4j
[mcp-space-life-sciences] Connected to PrimeKG
[mcp-space-life-sciences] SPOKE-OKN endpoint accessible
```

### Method 2: Test in Claude Desktop

Ask Claude:
```
Can you list the available MCP tools from mcp-space-life-sciences?
```

You should see tools like:
- `get_genelab_de_genes`
- `enrich_genes_with_primekg`
- `get_disease_prevalence_by_location`
- And 27+ more...

---

## Troubleshooting

### Error: "Server failed to start"

**Check:**
1. Python is accessible from the command line
2. Package is installed: `pip list | grep mcp-space-life-sciences`
3. Config file JSON is valid (use a JSON validator)

**Fix:**
```bash
# Reinstall the package
pip install --force-reinstall mcp-space-life-sciences

# Or in development mode
pip install -e . --force-reinstall
```

### Error: "Cannot connect to Neo4j"

**Check:**
1. Neo4j is running: `neo4j status`
2. Connection URI is correct (bolt:// not http://)
3. Credentials are correct
4. Port is accessible: `telnet localhost 7687`

**Fix:**
```bash
# Start Neo4j
neo4j start

# Or restart
neo4j restart
```

### Error: "Module not found: mcp_space_life_sciences"

**Check:**
1. Package is installed in the correct Python environment
2. Python path in config matches installation

**Fix (Development Mode):**
```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "/full/path/to/python",
      "args": ["-m", "mcp_space_life_sciences.server"],
      "env": { ... }
    }
  }
}
```

Find Python path:
```bash
which python  # macOS/Linux
where python  # Windows
```

### Error: "SPOKE-OKN queries failing"

**Check:**
1. Internet connection is active
2. SPARQL endpoint is accessible

**Test:**
```bash
curl https://frink.renci.org/spoke-okn/sparql
```

---

## Advanced Configuration

### Custom Log Level

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "LOG_LEVEL": "DEBUG",
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        ...
      }
    }
  }
}
```

### Connection Pooling

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "NEO4J_MAX_CONNECTION_LIFETIME": "3600",
        "NEO4J_MAX_CONNECTION_POOL_SIZE": "50",
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        ...
      }
    }
  }
}
```

### Timeout Settings

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "NEO4J_CONNECTION_TIMEOUT": "30",
        "SPARQL_TIMEOUT": "60",
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        ...
      }
    }
  }
}
```

---

## Security Best Practices

### 1. Use Environment Variables

Instead of hardcoding passwords in the config:

```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "${GENELAB_USER}",
        "GENELAB_NEO4J_PASSWORD": "${GENELAB_PASSWORD}",
        "PRIMEKG_NEO4J_URI": "bolt://localhost:7688",
        "PRIMEKG_NEO4J_USER": "${PRIMEKG_USER}",
        "PRIMEKG_NEO4J_PASSWORD": "${PRIMEKG_PASSWORD}"
      }
    }
  }
}
```

Then set in your shell:
```bash
export GENELAB_USER="neo4j"
export GENELAB_PASSWORD="your_secure_password"
export PRIMEKG_USER="neo4j"
export PRIMEKG_PASSWORD="your_secure_password"
```

### 2. File Permissions

Protect your config file:
```bash
chmod 600 ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

---

## Getting Help

If you encounter issues:

1. **Check logs** in Claude Desktop
2. **Test connections** manually (Neo4j browser, SPARQL endpoint)
3. **Verify installation**: `pip show mcp-space-life-sciences`
4. **Open an issue**: https://github.com/YOUR-USERNAME/MCP_Space_Life_Science_KGs/issues

Include in your issue:
- Operating system
- Python version (`python --version`)
- Config file (redact passwords!)
- Error messages from logs
- Steps to reproduce

---

## Related Documentation

- [Installation Guide](installation.md)
- [Quick Start Guide](quickstart.md)
- [API Reference](api_reference.md)
- [Troubleshooting Guide](troubleshooting.md)

---

## Example Complete Setup

Here's a complete step-by-step setup:

```bash
# 1. Install the package
pip install mcp-space-life-sciences

# 2. Start Neo4j databases (if using)
neo4j start

# 3. Edit Claude Desktop config
code ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Add:
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "mcp-space-life-sciences",
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "your_password",
        "PRIMEKG_DATA_PATH": "/Users/yourname/data/primekg"
      }
    }
  }
}

# 4. Restart Claude Desktop

# 5. Test in Claude Desktop
# Ask: "List available mcp-space-life-sciences tools"
```

**You're ready to go!** 🚀
