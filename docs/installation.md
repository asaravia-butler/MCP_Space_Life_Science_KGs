# Installation Guide

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Access to knowledge graph endpoints (optional for local testing)

## Installation Methods

### Option 1: Install from PyPI (Recommended)

```bash
pip install mcp-space-life-sciences
```

### Option 2: Install from Source

```bash
git clone https://github.com/YOUR-USERNAME/MCP_Space_Life_Science_KGs.git
cd MCP_Space_Life_Science_KGs
pip install -e .
```

### Option 3: Install with Development Dependencies

```bash
pip install -e ".[dev]"
```

## Configuration

### Environment Variables

Set these environment variables for knowledge graph access:

```bash
# GeneLab-SPOKE (Neo4j)
export GENELAB_NEO4J_URI="bolt://localhost:7687"
export GENELAB_NEO4J_USER="neo4j"
export GENELAB_NEO4J_PASSWORD="your_password"

# PrimeKG (Neo4j or DataFrame)
export PRIMEKG_NEO4J_URI="bolt://localhost:7688"
export PRIMEKG_NEO4J_USER="neo4j"
export PRIMEKG_NEO4J_PASSWORD="your_password"

# OR use data files for PrimeKG
export PRIMEKG_DATA_PATH="/path/to/primekg/data"

# SPOKE-OKN uses public SPARQL endpoint (no credentials needed)
```

### Configuration File

Create `~/.mcp_space_life_sciences/config.yaml`:

```yaml
genelab:
  neo4j_uri: "bolt://localhost:7687"
  neo4j_user: "neo4j"
  neo4j_password: "your_password"

primekg:
  neo4j_uri: "bolt://localhost:7688"
  neo4j_user: "neo4j"
  neo4j_password: "your_password"
  # OR
  data_path: "/path/to/primekg/data"

spoke_okn:
  sparql_endpoint: "https://frink.renci.org/spoke-okn/sparql"
```

## Verify Installation

```python
from mcp_space_life_sciences import IntegratedKGClient

client = IntegratedKGClient()
print("Installation successful!")
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'mcp'`
**Solution**: `pip install mcp`

**Issue**: Neo4j connection fails
**Solution**: Check URI, credentials, and that Neo4j is running

**Issue**: SPARQL queries timeout
**Solution**: Check network connection to SPOKE-OKN endpoint

For more help, see the [GitHub Issues](https://github.com/YOUR-USERNAME/MCP_Space_Life_Science_KGs/issues).
