# API Reference

## IntegratedKGClient

Main client for accessing all three knowledge graphs.

### Initialization

```python
client = IntegratedKGClient(
    genelab_uri="bolt://localhost:7687",
    primekg_uri="bolt://localhost:7688",
    spoke_okn_endpoint="https://frink.renci.org/spoke-okn/sparql"
)
```

### Methods

#### GeneLab Methods
- `get_genelab_de_genes()` - Get differentially expressed genes
- `find_genes_in_both_graphs()` - Find common genes

#### PrimeKG Methods  
- `enrich_genes_with_primekg()` - Enrich genes with annotations
- `find_drug_targets()` - Find drug targets
- `find_disease_genes()` - Find disease-associated genes

#### SPOKE-OKN Methods
- `get_disease_prevalence_by_location()` - Geographic disease data
- `get_chemical_exposures_by_location()` - Environmental exposures
- `get_sdoh_by_location()` - Social determinants of health

#### Multi-KG Methods
- `find_common_nodes()` - Nodes across all KGs
- `analyze_complete_mechanism()` - End-to-end analysis

See [examples/](../examples/) for detailed usage.
