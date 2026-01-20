# Technical Architecture

## System Overview

The MCP Space Life Sciences KGs server integrates three knowledge graphs:

1. **GeneLab-SPOKE** (Neo4j) - Space biology experiments
2. **PrimeKG** (Neo4j/DataFrame) - Precision medicine
3. **SPOKE-OKN** (SPARQL) - Geospatial health data

## Integration Layers

### Query Layer
- Cypher for Neo4j (GeneLab, PrimeKG)
- SPARQL for RDF (SPOKE-OKN)
- Query optimization and caching

### Integration Layer
- Node type mappings (8 types)
- Cross-graph entity resolution
- Result aggregation

### API Layer
- MCP server interface
- RESTful endpoints
- Client SDK

## Data Flow

```
User Request
    ↓
MCP Server
    ↓
[GeneLab] [PrimeKG] [SPOKE-OKN]
    ↓         ↓         ↓
Integration Layer
    ↓
Aggregated Response
```

## Performance Considerations

- Query batching (50 items/batch)
- Result caching
- Async operations where possible
- Connection pooling for Neo4j

See source code for implementation details.
