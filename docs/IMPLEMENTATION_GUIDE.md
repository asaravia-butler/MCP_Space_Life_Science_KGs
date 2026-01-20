# Implementation Guide: GeneLab-PrimeKG Integration

## Quick Start

### 1. Installation

```bash
# Install the enhanced MCP PrimeKG server
pip install mcp-primekg-enhanced

# Install visualization dependencies
pip install matplotlib seaborn networkx matplotlib-venn

# Optional: Neo4j driver for direct database access
pip install neo4j pandas
```

### 2. Configuration

```bash
# Set environment variables
export PRIMEKG_DATA_PATH="/path/to/primekg/data"
export PRIMEKG_NEO4J_URI="bolt://localhost:7687"
export PRIMEKG_NEO4J_USER="neo4j"
export PRIMEKG_NEO4J_PASSWORD="your_password"
```

### 3. Basic Usage

```python
from primekg_client import PrimeKGClient

# Initialize client
client = PrimeKGClient(data_path="/path/to/data")

# Search for genes
genes = client.search_nodes(query="BRCA", node_type="gene/protein", limit=10)
print(genes)
```

## Complete Example Workflows

### Example 1: Space Biology Study Analysis

This example shows how to analyze genes from a spaceflight experiment and find therapeutic implications.

```python
import pandas as pd
from primekg_client import PrimeKGClient
from genelab_client import GeneLabClient

# Initialize clients
genelab = GeneLabClient()
primekg = PrimeKGClient()

# Step 1: Get differentially expressed genes from GeneLab
print("Step 1: Getting differentially expressed genes from GeneLab...")
assay_id = "OSD-253-6c5f9f37b9cb2ebeb2743875af4bdc86"
de_results = genelab.find_differentially_expressed_genes(
    assay_id=assay_id,
    top_n=50
)

# Extract upregulated and downregulated genes
upregulated = de_results['upregulated']['gene_symbol'].tolist()
downregulated = de_results['downregulated']['gene_symbol'].tolist()

print(f"Found {len(upregulated)} upregulated and {len(downregulated)} downregulated genes")

# Step 2: Enrich genes with PrimeKG annotations
print("\nStep 2: Enriching genes with PrimeKG data...")
enrichment = primekg.enrich_genelab_genes_with_primekg(
    gene_names=upregulated[:20],  # Top 20 for example
    include_drugs=True,
    include_diseases=True,
    include_pathways=True
)

# Display enrichment summary
print(f"\nEnrichment Summary:")
print(f"- Genes with drug targets: {enrichment['summary']['genes_with_drug_targets']}")
print(f"- Genes with disease associations: {enrichment['summary']['genes_with_disease_associations']}")
print(f"- Genes in pathways: {enrichment['summary']['genes_in_pathways']}")

# Step 3: Find drug targets
print("\nStep 3: Finding drug targets...")
drug_targets = primekg.find_drug_targets_for_gene_list(
    gene_names=upregulated[:20],
    limit_per_gene=5
)

print(f"Found {len(drug_targets)} drug-gene relationships")
print("\nTop drug targets:")
print(drug_targets.head(10))

# Step 4: Find shared pathways
print("\nStep 4: Finding shared biological pathways...")
pathways = primekg.find_shared_pathways(
    gene_names=upregulated[:30],
    min_genes=3
)

print(f"Found {len(pathways)} shared pathways")
print("\nTop pathways:")
print(pathways.head(10))

# Step 5: Visualize results
print("\nStep 5: Creating visualizations...")

# Create pathway enrichment plot
pathway_viz = primekg.create_pathway_enrichment_plot(
    gene_names=upregulated[:30],
    top_n=15,
    figsize=(12, 8)
)
print(f"Pathway plot saved to: {pathway_viz['image_path']}")

# Create drug-target heatmap
drug_viz = primekg.create_drug_target_heatmap(
    gene_names=upregulated[:20],
    figsize=(14, 10)
)
print(f"Drug-target heatmap saved to: {drug_viz['image_path']}")

# Create gene network
network_viz = primekg.create_gene_network_plot(
    gene_names=upregulated[:15],
    include_relationships=["protein_protein", "pathway_protein"],
    max_neighbors=5,
    figsize=(12, 10)
)
print(f"Network plot saved to: {network_viz['image_path']}")

print("\nAnalysis complete!")
```

### Example 2: Comparative Analysis of Two Conditions

Compare gene expression between microgravity and radiation conditions.

```python
# Get genes from two different assays
assay_microgravity = "OSD-253-assay1"
assay_radiation = "OSD-253-assay2"

# Get DE genes for both conditions
print("Getting genes from both conditions...")
genes_micro = genelab.find_differentially_expressed_genes(assay_microgravity, top_n=100)
genes_rad = genelab.find_differentially_expressed_genes(assay_radiation, top_n=100)

micro_up = genes_micro['upregulated']['gene_symbol'].tolist()
rad_up = genes_rad['upregulated']['gene_symbol'].tolist()

# Compare gene sets
print("\nComparing gene sets...")
comparison = primekg.compare_gene_sets(
    gene_set_1=micro_up,
    gene_set_2=rad_up,
    gene_set_1_name="Microgravity",
    gene_set_2_name="Radiation"
)

print(f"\nComparison Results:")
print(f"Microgravity genes: {comparison['set_1_size']}")
print(f"Radiation genes: {comparison['set_2_size']}")
print(f"Overlap: {comparison['overlap_size']}")
print(f"Jaccard Index: {comparison['jaccard_index']:.3f}")

print(f"\nOverlapping genes: {', '.join(comparison['overlap_genes'][:10])}...")

# Find pathways enriched in overlap
overlap_genes = comparison['overlap_genes']
if len(overlap_genes) >= 3:
    print("\nFinding pathways in overlapping genes...")
    shared_pathways = primekg.find_shared_pathways(
        gene_names=overlap_genes,
        min_genes=2
    )
    print(f"Found {len(shared_pathways)} shared pathways")
    print(shared_pathways.head())

# Find pathways unique to each condition
print("\nFinding condition-specific pathways...")
micro_pathways = primekg.find_shared_pathways(
    gene_names=comparison['set_1_unique'][:50],
    min_genes=2
)
rad_pathways = primekg.find_shared_pathways(
    gene_names=comparison['set_2_unique'][:50],
    min_genes=2
)

print(f"Microgravity-specific pathways: {len(micro_pathways)}")
print(f"Radiation-specific pathways: {len(rad_pathways)}")
```

### Example 3: Disease Association Discovery

Identify diseases potentially affected by spaceflight conditions.

```python
# Get genes from spaceflight experiment
assay_id = "OSD-253-spaceflight"
de_genes = genelab.find_differentially_expressed_genes(assay_id, top_n=100)
all_de_genes = (de_genes['upregulated']['gene_symbol'].tolist() + 
                de_genes['downregulated']['gene_symbol'].tolist())

# Find disease associations
print("Finding disease associations...")
diseases = primekg.find_disease_associations(
    gene_names=all_de_genes,
    min_genes=5  # At least 5 genes must be associated
)

print(f"\nFound {len(diseases)} diseases associated with {len(all_de_genes)} genes")
print("\nTop 10 diseases by gene count:")
print(diseases.head(10)[['disease_name', 'gene_count', 'genes']])

# For top disease, get more details
top_disease = diseases.iloc[0]['disease_name']
print(f"\nAnalyzing top disease: {top_disease}")

# Find drugs indicated for this disease
top_disease_genes = diseases.iloc[0]['genes']
disease_drugs = primekg.find_drug_targets_for_gene_list(
    gene_names=top_disease_genes,
    limit_per_gene=10
)

print(f"Found {len(disease_drugs)} potential drug targets")
print(disease_drugs.head())

# Create disease-gene network visualization
disease_network = primekg.create_disease_gene_network(
    gene_names=all_de_genes[:30],
    figsize=(16, 12)
)
print(f"\nDisease-gene network saved to: {disease_network['image_path']}")
```

### Example 4: Protein-Protein Interaction Network

Build interaction networks from differentially expressed genes.

```python
# Get DE genes
assay_id = "OSD-253-example"
de_results = genelab.find_differentially_expressed_genes(assay_id, top_n=50)
upregulated = de_results['upregulated']['gene_symbol'].tolist()

# Find protein-protein interactions
print("Finding protein-protein interactions...")
interactions = primekg.find_protein_protein_interactions(
    gene_names=upregulated,
    include_indirect=False  # Only direct interactions
)

print(f"\nFound {len(interactions)} direct protein-protein interactions")
print(interactions.head(10))

# Calculate network statistics
num_genes = len(set(interactions['gene_1'].tolist() + interactions['gene_2'].tolist()))
print(f"\n{num_genes} genes out of {len(upregulated)} form a connected network")
print(f"Network density: {len(interactions) / (num_genes * (num_genes-1) / 2):.3f}")

# Visualize network
network_viz = primekg.create_gene_network_plot(
    gene_names=upregulated[:20],
    include_relationships=["protein_protein"],
    max_neighbors=10,
    figsize=(14, 12)
)
print(f"Network visualization saved to: {network_viz['image_path']}")
```

### Example 5: GO Term Enrichment Analysis

Perform comprehensive Gene Ontology enrichment.

```python
# Get DE genes
de_genes = ["TP53", "BRCA1", "EGFR", "MYC", "VEGFA", 
            "HIF1A", "PTEN", "AKT1", "MAPK1", "PIK3CA"]

# Find GO enrichment for all ontologies
print("Performing GO enrichment analysis...")
go_enrichment = primekg.find_gene_ontology_enrichment(
    gene_names=de_genes,
    ontology_type="all",
    min_genes=2
)

# Display results for each ontology
for ontology, results in go_enrichment.items():
    print(f"\n{ontology.upper()}:")
    print(f"Found {len(results)} enriched terms")
    if len(results) > 0:
        print(results.head())

# Create visualization for biological processes
if len(go_enrichment['biological_process']) > 0:
    # Convert to gene list format for visualization
    bp_genes = go_enrichment['biological_process'].iloc[0]['genes']
    
    pathway_viz = primekg.create_pathway_enrichment_plot(
        gene_names=de_genes,
        top_n=20,
        figsize=(12, 10)
    )
    print(f"\nGO enrichment plot saved to: {pathway_viz['image_path']}")
```

### Example 6: Anatomical Expression Analysis

Find where genes are expressed in the body.

```python
# Get genes of interest
genes = ["ACTB", "GAPDH", "TP53", "BRCA1", "EGFR"]

# Find anatomical expression
print("Finding anatomical expression patterns...")
expression = primekg.find_anatomical_expression(
    gene_names=genes,
    presence_type="present"
)

print(f"\nFound {len(expression)} expression records")

# Group by gene
for gene in genes:
    gene_expr = expression[expression['gene_name'] == gene]
    anatomies = gene_expr['anatomy_name'].tolist()
    print(f"\n{gene} expressed in {len(anatomies)} anatomical locations:")
    print(f"  {', '.join(anatomies[:5])}...")

# Find tissue-specific genes
tissue_counts = expression.groupby('gene_name')['anatomy_name'].count()
print("\nGenes by number of expression sites:")
print(tissue_counts.sort_values(ascending=False))
```

## Advanced Usage

### Custom Neo4j Queries

For advanced users who want to write custom queries:

```python
from neo4j import GraphDatabase

# Connect to PrimeKG Neo4j database
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)

# Custom query: Find genes in specific pathway
def find_pathway_genes(pathway_name):
    with driver.session() as session:
        query = """
        MATCH (p:pathway {node_name: $pathway_name})-[r:pathway_protein]-(g:`gene/protein`)
        RETURN g.node_name AS gene, g.node_id AS gene_id
        ORDER BY gene
        """
        result = session.run(query, pathway_name=pathway_name)
        return pd.DataFrame([dict(record) for record in result])

# Use custom query
pathway_genes = find_pathway_genes("MAPK signaling pathway")
print(pathway_genes)
```

### Batch Processing

Process multiple assays in batch:

```python
# List of assay IDs to process
assay_ids = [
    "OSD-253-assay1",
    "OSD-253-assay2", 
    "OSD-253-assay3"
]

# Process each assay
results = {}
for assay_id in assay_ids:
    print(f"\nProcessing {assay_id}...")
    
    # Get DE genes
    de = genelab.find_differentially_expressed_genes(assay_id, top_n=50)
    genes = de['upregulated']['gene_symbol'].tolist()
    
    # Enrich with PrimeKG
    enrichment = primekg.enrich_genelab_genes_with_primekg(genes)
    
    # Find pathways
    pathways = primekg.find_shared_pathways(genes, min_genes=2)
    
    # Store results
    results[assay_id] = {
        'genes': genes,
        'enrichment': enrichment,
        'pathways': pathways
    }

# Compare pathways across assays
all_pathways = set()
for assay_id, data in results.items():
    assay_pathways = set(data['pathways']['pathway_name'].tolist())
    all_pathways.update(assay_pathways)
    print(f"{assay_id}: {len(assay_pathways)} pathways")

print(f"\nTotal unique pathways: {len(all_pathways)}")
```

### Export Results

Export results for further analysis:

```python
import json

# Export enrichment data
with open('primekg_enrichment.json', 'w') as f:
    json.dump(enrichment, f, indent=2)

# Export pathways to CSV
pathways.to_csv('shared_pathways.csv', index=False)

# Export drug targets
drug_targets.to_csv('drug_targets.csv', index=False)

print("Results exported successfully!")
```

## Performance Tips

### 1. Batch Queries

Instead of querying genes one at a time:

```python
# BAD: Individual queries
for gene in genes:
    data = client.enrich_gene(gene)  # Slow!

# GOOD: Batch query
data = client.enrich_genelab_genes_with_primekg(genes)  # Fast!
```

### 2. Limit Result Sets

Use appropriate limits:

```python
# Get top 20 pathways (not all thousands)
pathways = client.find_shared_pathways(genes, min_genes=2, limit=20)
```

### 3. Cache Results

Cache expensive queries:

```python
import pickle

# Save results
with open('enrichment_cache.pkl', 'wb') as f:
    pickle.dump(enrichment, f)

# Load cached results
with open('enrichment_cache.pkl', 'rb') as f:
    enrichment = pickle.load(f)
```

## Troubleshooting

### Issue: Missing Genes

Some genes may not be in PrimeKG:

```python
# Check which genes are found
result = client.find_genes_in_both_graphs(gene_list)
found = result['found_genes']
missing = result['missing_genes']

print(f"Found: {len(found)}, Missing: {len(missing)}")
if missing:
    print(f"Missing genes: {', '.join(missing)}")
```

### Issue: No Results

Adjust thresholds if getting no results:

```python
# Try with lower threshold
pathways = client.find_shared_pathways(
    genes, 
    min_genes=1  # Lower threshold
)
```

### Issue: Slow Queries

Enable query logging to identify slow queries:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all queries will be logged
```

## Next Steps

1. Explore the example notebooks in `/examples`
2. Read the API reference documentation
3. Join our community forum for support
4. Contribute your own analyses!

## Resources

- **PrimeKG Paper**: https://doi.org/10.1038/s41597-023-01960-3
- **GeneLab**: https://genelab.nasa.gov
- **Documentation**: See README_INTEGRATION.md
- **Cypher Queries**: See cypher_queries_integration.py
