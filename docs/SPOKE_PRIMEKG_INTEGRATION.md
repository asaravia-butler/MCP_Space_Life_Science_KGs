# SPOKE-OKN and PrimeKG: Common Nodes and Integration Strategy

## Overview

Both the SPOKE-OKN knowledge graph (which GeneLab is based on) and PrimeKG share many common node types and use compatible identifiers. This document outlines the shared nodes and how to leverage them for cross-graph queries.

## Shared Node Types and Identifiers

### 1. Gene/Protein Nodes

**PrimeKG:**
- Node label: `gene/protein`
- Primary identifier: Gene symbol (e.g., "TP53", "BRCA1")
- Secondary identifier: NCBI Gene ID / Entrez ID
- Count: 27,671 genes

**SPOKE-OKN:**
- Node label: `Gene` or `Protein`
- Primary identifier: Gene symbol
- Secondary identifier: Entrez Gene ID, Ensembl ID
- Additional: UniProt IDs for proteins

**Integration Strategy:**
- **Primary key**: Gene symbol (most reliable across both graphs)
- **Fallback**: Entrez Gene ID
- **Handling**: Case-sensitive matching, normalize to uppercase

```cypher
// Example: Link by gene symbol
// PrimeKG
MATCH (pk:`gene/protein` {node_name: "TP53"})

// SPOKE-OKN / GeneLab
MATCH (gl:Gene {gene_symbol: "TP53"})

// Combined query concept:
// 1. Get gene from GeneLab
// 2. Use gene_symbol to query PrimeKG
```

### 2. Disease Nodes

**PrimeKG:**
- Node label: `disease`
- Primary identifier: MONDO ID (e.g., "MONDO:0004992")
- Count: 17,080 diseases

**SPOKE-OKN:**
- Node label: `Disease`
- Primary identifier: MONDO ID, DOID (Disease Ontology ID)
- Secondary: UMLS CUI, ICD codes

**Integration Strategy:**
- **Primary key**: MONDO ID (when available)
- **Fallback**: Disease name (fuzzy matching may be needed)
- **Note**: PrimeKG has broader disease coverage

```cypher
// Link diseases by MONDO ID
// Extract MONDO from node_id in PrimeKG
MATCH (pk:disease)
WHERE pk.node_id CONTAINS 'MONDO'

// Match with SPOKE
MATCH (spoke:Disease)
WHERE spoke.mondo_id = pk.extracted_mondo_id
```

### 3. Anatomy Nodes

**PrimeKG:**
- Node label: `anatomy`
- Primary identifier: UBERON ID (e.g., "UBERON:0001087")
- Count: 14,035 anatomical entities

**SPOKE-OKN:**
- Node label: `Anatomy`
- Primary identifier: UBERON ID
- Includes tissue, organ, cell type entities

**Integration Strategy:**
- **Primary key**: UBERON ID
- **Excellent mapping**: Both use UBERON ontology
- **Use case**: Map tissue expression from both graphs

```cypher
// Perfect mapping via UBERON
// PrimeKG
MATCH (pk:anatomy {node_id: "UBERON:0001087"})

// SPOKE
MATCH (spoke:Anatomy {uberon_id: "UBERON:0001087"})
```

### 4. Biological Process (GO) Nodes

**PrimeKG:**
- Node label: `biological_process`
- Primary identifier: GO ID (e.g., "GO:0008150")
- Count: 28,642 processes

**SPOKE-OKN:**
- Node label: `BiologicalProcess`
- Primary identifier: GO ID
- Hierarchical structure maintained

**Integration Strategy:**
- **Primary key**: GO ID
- **Excellent mapping**: Both use Gene Ontology
- **Use case**: Pathway and process enrichment

```cypher
// Map by GO ID
// PrimeKG
MATCH (pk:biological_process)
WHERE pk.node_id STARTS WITH 'GO:'

// SPOKE  
MATCH (spoke:BiologicalProcess {go_id: pk.node_id})
```

### 5. Molecular Function (GO) Nodes

**PrimeKG:**
- Node label: `molecular_function`
- Primary identifier: GO ID
- Count: 11,169 functions

**SPOKE-OKN:**
- Node label: `MolecularFunction`
- Primary identifier: GO ID

**Integration Strategy:**
- Same as Biological Process
- Use GO ID for perfect mapping

### 6. Cellular Component (GO) Nodes

**PrimeKG:**
- Node label: `cellular_component`
- Primary identifier: GO ID
- Count: 4,176 components

**SPOKE-OKN:**
- Node label: `CellularComponent`
- Primary identifier: GO ID

**Integration Strategy:**
- Same as other GO categories
- Use GO ID for mapping

### 7. Pathway Nodes

**PrimeKG:**
- Node label: `pathway`
- Sources: Reactome, WikiPathways, KEGG
- Count: 2,516 pathways

**SPOKE-OKN:**
- Node label: `Pathway`
- Sources: Reactome, WikiPathways, others
- Primary identifier: Reactome ID or pathway name

**Integration Strategy:**
- **Primary key**: Reactome ID (when available)
- **Secondary**: Pathway name (fuzzy matching)
- **Note**: Some overlap but not complete

```cypher
// Map pathways by Reactome ID
// PrimeKG
MATCH (pk:pathway)
WHERE pk.node_id STARTS WITH 'R-HSA-' OR pk.node_id STARTS WITH 'WP'

// SPOKE
MATCH (spoke:Pathway)
WHERE spoke.reactome_id = pk.node_id
```

### 8. Drug/Compound Nodes

**PrimeKG:**
- Node label: `drug`
- Primary identifier: DrugBank ID
- Count: 7,957 drugs

**SPOKE-OKN:**
- Node label: `Compound` or `Drug`
- Primary identifier: DrugBank ID, PubChem CID
- Secondary: RxNorm, ChEMBL

**Integration Strategy:**
- **Primary key**: DrugBank ID
- **Good coverage**: Both use DrugBank
- **Use case**: Drug repurposing, target identification

```cypher
// Map drugs by DrugBank ID
// PrimeKG
MATCH (pk:drug)
WHERE pk.node_source = 'DrugBank'

// SPOKE
MATCH (spoke:Compound)
WHERE spoke.drugbank_id = pk.node_id
```

## Shared Relationship Types

### Gene-Disease Associations

**PrimeKG:**
- Relationship: `disease_protein`
- Count: 160,822
- Sources: DisGeNET, GWAS Catalog

**SPOKE-OKN:**
- Relationship: `ASSOCIATES_WITH` or `CAUSES`
- Sources: DisGeNET, CTD, others

**Integration:** Use gene symbol + disease MONDO ID

### Gene-Pathway Associations

**PrimeKG:**
- Relationship: `pathway_protein`  
- Count: 85,292

**SPOKE-OKN:**
- Relationship: `PARTICIPATES_IN`
- Source: Reactome, WikiPathways

**Integration:** Use gene symbol + pathway ID

### Protein-Protein Interactions

**PrimeKG:**
- Relationship: `protein_protein`
- Count: 642,150
- Sources: STRING, BioGRID

**SPOKE-OKN:**
- Relationship: `INTERACTS_WITH`
- Sources: STRING, BioGRID, IntAct

**Integration:** Use gene symbols for both proteins

### Drug-Target Relationships

**PrimeKG:**
- Relationship: `drug_protein`
- Count: 51,306
- Source: DrugBank, ChEMBL

**SPOKE-OKN:**
- Relationship: `TARGETS`
- Source: DrugBank, BindingDB

**Integration:** Use DrugBank ID + gene symbol

### Gene-GO Annotations

**PrimeKG:**
- Relationships: `bioprocess_protein`, `molfunc_protein`, `cellcomp_protein`
- Total: ~595K annotations

**SPOKE-OKN:**
- Relationships: `HAS_BIOLOGICAL_PROCESS`, `HAS_MOLECULAR_FUNCTION`, `PART_OF_CELLULAR_COMPONENT`
- Source: GO annotations

**Integration:** Use gene symbol + GO ID

## Integration Patterns

### Pattern 1: Direct Node Matching

When nodes exist in both graphs with same identifiers:

```python
def find_common_nodes(gene_symbols, node_type="gene"):
    """
    Find which nodes exist in both PrimeKG and SPOKE-OKN
    """
    # Query PrimeKG
    primekg_genes = query_primekg(
        f"MATCH (g:`gene/protein`) WHERE g.node_name IN {gene_symbols} RETURN g"
    )
    
    # Query SPOKE
    spoke_genes = query_spoke(
        f"MATCH (g:Gene) WHERE g.gene_symbol IN {gene_symbols} RETURN g"
    )
    
    # Find intersection
    common = set(primekg_genes) & set(spoke_genes)
    return common
```

### Pattern 2: Property Enrichment

Add properties from one graph to nodes from another:

```python
def enrich_genelab_with_primekg(gene_symbols):
    """
    Enrich GeneLab genes with PrimeKG annotations
    """
    enriched = {}
    
    for gene in gene_symbols:
        # Get from GeneLab (SPOKE)
        genelab_data = query_spoke(
            f"MATCH (g:Gene {{gene_symbol: '{gene}'}}) RETURN g"
        )
        
        # Get from PrimeKG
        primekg_data = query_primekg(
            f"""
            MATCH (g:`gene/protein` {{node_name: '{gene}'}})
            OPTIONAL MATCH (g)-[:drug_protein]-(d:drug)
            OPTIONAL MATCH (g)-[:disease_protein]-(dis:disease)
            RETURN g, collect(DISTINCT d) as drugs, collect(DISTINCT dis) as diseases
            """
        )
        
        # Combine
        enriched[gene] = {
            **genelab_data,
            'primekg_drugs': primekg_data['drugs'],
            'primekg_diseases': primekg_data['diseases']
        }
    
    return enriched
```

### Pattern 3: Cross-Graph Traversal

Use one graph to inform queries on another:

```python
def find_therapeutic_targets(assay_id):
    """
    Find drug targets for GeneLab differential expression
    """
    # Step 1: Get DE genes from GeneLab
    de_genes = query_spoke(
        f"""
        MATCH (a:Assay {{assay_id: '{assay_id}'}})-[r:DIFF_GENE_EXPRESSED]->(g:Gene)
        WHERE abs(r.log2fc) > 1 AND r.adj_p_value < 0.05
        RETURN g.gene_symbol as gene
        """
    )
    
    gene_list = [g['gene'] for g in de_genes]
    
    # Step 2: Find drugs targeting these genes in PrimeKG
    drug_targets = query_primekg(
        f"""
        MATCH (g:`gene/protein`)-[r:drug_protein]-(d:drug)
        WHERE g.node_name IN {gene_list}
        RETURN g.node_name as gene, d.node_name as drug, d.node_id as drug_id
        """
    )
    
    return drug_targets
```

### Pattern 4: Pathway Convergence

Find pathways enriched in genes from both graphs:

```python
def find_converging_pathways(genelab_genes, primekg_genes):
    """
    Find pathways that contain genes from both sources
    """
    all_genes = list(set(genelab_genes + primekg_genes))
    
    # Query PrimeKG for pathways
    pathways = query_primekg(
        f"""
        MATCH (g:`gene/protein`)-[:pathway_protein]-(p:pathway)
        WHERE g.node_name IN {all_genes}
        WITH p, collect(g.node_name) as genes, count(g) as gene_count
        WHERE gene_count >= 3
        RETURN p.node_name as pathway, genes, gene_count
        ORDER BY gene_count DESC
        """
    )
    
    # Annotate with source
    for pathway in pathways:
        pathway['from_genelab'] = [g for g in pathway['genes'] if g in genelab_genes]
        pathway['from_primekg'] = [g for g in pathway['genes'] if g in primekg_genes]
    
    return pathways
```

## Data Quality Considerations

### 1. Gene Symbol Variations

Some genes have multiple symbols:
- Use HGNC approved symbols when possible
- Handle aliases (e.g., "TP53" vs "P53")
- Consider historical symbols

```python
GENE_ALIASES = {
    "TP53": ["P53", "TRP53"],
    "BRCA1": ["RNF53"],
    # ... more aliases
}
```

### 2. Missing Nodes

Not all nodes exist in both graphs:
- PrimeKG has more drugs (7,957 vs SPOKE's subset)
- SPOKE has more specific tissue types
- Handle missing gracefully

```python
def safe_enrich(gene):
    try:
        return enrich_gene(gene)
    except NodeNotFound:
        return {"gene": gene, "enrichment": None, "reason": "not_in_primekg"}
```

### 3. Identifier Resolution

Use identifier mapping services:
- MyGene.info for gene ID conversion
- UniProt ID mapping for proteins
- bioDBnet for multi-database conversion

## Example: Complete Integration Workflow

```python
from genelab_client import GeneLabClient
from primekg_client import PrimeKGClient
import pandas as pd

def complete_integration_workflow(assay_id):
    """
    Complete workflow integrating GeneLab and PrimeKG
    """
    genelab = GeneLabClient()
    primekg = PrimeKGClient()
    
    # 1. Get GeneLab differential expression
    print("Step 1: GeneLab differential expression...")
    de_results = genelab.find_differentially_expressed_genes(assay_id, top_n=100)
    genes = de_results['upregulated']['gene_symbol'].tolist()
    
    # 2. Verify genes exist in PrimeKG
    print("Step 2: Checking genes in PrimeKG...")
    validation = primekg.find_genes_in_both_graphs(genes)
    found_genes = validation['found_genes']
    print(f"Found {len(found_genes)}/{len(genes)} genes in PrimeKG")
    
    # 3. Enrich with PrimeKG data
    print("Step 3: Enriching with PrimeKG...")
    enrichment = primekg.enrich_genelab_genes_with_primekg(
        gene_names=found_genes,
        include_drugs=True,
        include_diseases=True,
        include_pathways=True
    )
    
    # 4. Find shared pathways
    print("Step 4: Finding shared pathways...")
    pathways = primekg.find_shared_pathways(found_genes, min_genes=3)
    
    # 5. Find drug targets
    print("Step 5: Finding drug targets...")
    drugs = primekg.find_drug_targets_for_gene_list(found_genes)
    
    # 6. Find disease associations
    print("Step 6: Finding diseases...")
    diseases = primekg.find_disease_associations(found_genes, min_genes=2)
    
    # 7. Create visualizations
    print("Step 7: Creating visualizations...")
    network = primekg.create_gene_network_plot(found_genes[:20])
    heatmap = primekg.create_drug_target_heatmap(found_genes[:30])
    pathway_plot = primekg.create_pathway_enrichment_plot(found_genes)
    
    # 8. Compile results
    results = {
        'assay_id': assay_id,
        'total_genes': len(genes),
        'genes_in_primekg': len(found_genes),
        'enrichment': enrichment,
        'pathways': pathways.to_dict('records'),
        'drugs': drugs.to_dict('records'),
        'diseases': diseases.to_dict('records'),
        'visualizations': {
            'network': network['image_path'],
            'heatmap': heatmap['image_path'],
            'pathways': pathway_plot['image_path']
        }
    }
    
    return results

# Run workflow
results = complete_integration_workflow("OSD-253-assay-id")
print(json.dumps(results, indent=2))
```

## Conclusion

The integration between SPOKE-OKN (GeneLab) and PrimeKG is highly feasible due to:

1. **Common identifiers**: Gene symbols, GO IDs, MONDO IDs, UBERON IDs, DrugBank IDs
2. **Compatible schemas**: Similar node types and relationships
3. **Complementary data**: SPOKE has expression data, PrimeKG has extensive drug/disease info
4. **Clear use cases**: Therapeutic target discovery, mechanism understanding, drug repurposing

This integration enables powerful cross-graph queries that combine space biology research (GeneLab) with precision medicine knowledge (PrimeKG).
