# Quick Start Guide

Get started with MCP Space Life Sciences KGs in 5 minutes!

## Basic Usage

```python
from mcp_space_life_sciences import IntegratedKGClient

# Initialize client
client = IntegratedKGClient()

# Get differential expression from GeneLab
de_genes = client.get_genelab_de_genes(
    assay_id="OSD-253-EXAMPLE",
    log2fc_threshold=1.0
)

# Enrich with PrimeKG
enrichment = client.enrich_genes_with_primekg(
    gene_names=de_genes['upregulated'][:50]
)

# Add geospatial context from SPOKE-OKN
prevalence = client.get_disease_prevalence_by_location(
    disease_names=enrichment['diseases'][:10],
    location="United States"
)

print(f"Found {len(enrichment['drugs'])} potential drug targets")
```

See full documentation in [api_reference.md](api_reference.md)
