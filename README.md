# MCP Space Life Science KGs

**A unified Model Context Protocol (MCP) server integrating three major biomedical knowledge graphs for space life sciences research.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Overview

This MCP server creates a comprehensive integration layer connecting three complementary knowledge graphs:

1. **GeneLab-SPOKE** - NASA space biology experiments with differential gene expression
2. **PrimeKG** - Precision medicine knowledge graph with 129K biomedical entities  
3. **SPOKE-OKN** - Open Knowledge Network with social determinants of health and environmental factors

By bridging these graphs through common node types (genes, diseases, anatomy, pathways, drugs, GO terms), researchers can perform powerful cross-graph queries to understand the biological impacts of spaceflight and discover therapeutic interventions.

## Key Features

- **🔗 Multi-Graph Integration**: Seamlessly query across 3 knowledge graphs
- **🧬 8 Common Node Types**: Genes, Diseases, Anatomy, Pathways, Drugs, and 3 GO categories
- **📊 30+ Analysis Tools**: From gene enrichment to drug-disease mechanisms
- **📈 7+ Visualizations**: Networks, heatmaps, pathway enrichment plots
- **🌍 Geospatial Context**: Link biological findings to geographic locations via SPOKE-OKN
- **💊 Therapeutic Discovery**: Find drug candidates for space-induced changes

## Knowledge Graph Sources

### GeneLab-SPOKE
- **Purpose**: NASA space biology experiments
- **Content**: Differential gene expression from spaceflight conditions
- **GitHub**: [sbl-sdsc/mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab)
- **Source**: [BaranziniLab/spoke_genelab](https://github.com/BaranziniLab/spoke_genelab)

### PrimeKG  
- **Purpose**: Precision medicine knowledge graph
- **Content**: 129,375 biomedical entities, 8.1M relationships
- **GitHub**: [asaravia-butler/MCP_Harvard_PrimeKG](https://github.com/asaravia-butler/MCP_Harvard_PrimeKG)
- **Website**: [zitniklab.hms.harvard.edu/projects/PrimeKG](https://zitniklab.hms.harvard.edu/projects/PrimeKG/)
- **Paper**: [Chandak et al., Scientific Data 2023](https://doi.org/10.1038/s41597-023-01960-3)

### SPOKE-OKN
- **Purpose**: Open Knowledge Network with social & environmental determinants
- **Content**: Disease prevalence, chemical exposures, SDoH by location
- **GitHub**: [sbl-sdsc/mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn)
- **Overview**: [SPOKE-OKN Docs](https://github.com/sbl-sdsc/mcp-proto-okn/blob/main/docs/examples/spoke-okn_overview.md)
- **Website**: [proto-okn.net](https://www.proto-okn.net/)
- **Endpoint**: [frink.renci.org/registry/kgs/spoke-okn](https://frink.renci.org/registry/kgs/spoke-okn/)

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GeneLab-SPOKE (Neo4j)                         │
│         Space Biology | Differential Expression                 │
├─────────────────────────────────────────────────────────────────┤
│  Gene │ Assay │ Study │ Tissue │ Cell Type │ Protein           │
└────┬────────────────────────────────────────────────────────┬───┘
     │                                                        │
     │  Common Identifiers:                                  │
     │  • Genes: gene_symbol                                 │
     │  • Diseases: mondo_id                                 │
     │  • Anatomy: uberon_id                                 │
     │  • GO Terms: go_id                                    │
     ▼                                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│          MCP Space Life Sciences Integration Server             │
│                    (This Repository)                             │
├─────────────────────────────────────────────────────────────────┤
│  • Cross-graph queries        • Enrichment analysis             │
│  • Mechanism discovery        • Therapeutic identification      │
│  • Visualization generation   • Geospatial contextualization    │
└────┬────────────────────────────────────────────────────────┬───┘
     │                                                        │
     ▼                                                        ▼
┌──────────────────────────────┐  ┌──────────────────────────────┐
│    PrimeKG (Neo4j/DataFrame) │  │   SPOKE-OKN (SPARQL)         │
│  Precision Medicine KG        │  │  Open Knowledge Network      │
├──────────────────────────────┤  ├──────────────────────────────┤
│ gene/protein │ disease        │  │ ChemicalEntity │ Disease     │
│ anatomy      │ pathway        │  │ AdministrativeArea │ SDoH   │
│ drug         │ 3 GO types     │  │ Gene │ OrganismTaxon        │
└──────────────────────────────┘  └──────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Access to knowledge graph endpoints (GeneLab Neo4j, PrimeKG, SPOKE-OKN SPARQL)

### Install via pip

```bash
pip install mcp-space-life-sciences
```

### Install from source

```bash
git clone https://github.com/asaravia-butler/MCP_Space_Life_Science_KGs.git
cd MCP_Space_Life_Science_KGs
pip install -e .
```

### Configuration

Set environment variables for knowledge graph access:

```bash
# GeneLab-SPOKE
export GENELAB_NEO4J_URI="bolt://localhost:7687"
export GENELAB_NEO4J_USER="neo4j"
export GENELAB_NEO4J_PASSWORD="your_password"

# PrimeKG (if using Neo4j backend)
export PRIMEKG_NEO4J_URI="bolt://localhost:7688"
export PRIMEKG_NEO4J_USER="neo4j"
export PRIMEKG_NEO4J_PASSWORD="your_password"

# Or use PrimeKG data path for DataFrame backend
export PRIMEKG_DATA_PATH="/path/to/primekg/data"

# SPOKE-OKN uses public SPARQL endpoint (no credentials needed)
```

## Configuration for Claude Desktop

**⚠️ Important**: To use this MCP server with Claude Desktop, you must configure it in your `claude_desktop_config.json` file.

See the complete guide: [Claude Desktop Configuration](docs/claude_desktop_config.md)

**Quick Config (Development Mode)**:
```json
{
  "mcpServers": {
    "mcp-space-life-sciences": {
      "command": "python",
      "args": ["-m", "mcp_space_life_sciences.server"],
      "env": {
        "GENELAB_NEO4J_URI": "bolt://localhost:7687",
        "GENELAB_NEO4J_USER": "neo4j",
        "GENELAB_NEO4J_PASSWORD": "your_password",
        "PRIMEKG_DATA_PATH": "/path/to/primekg/data"
      }
    }
  }
}
```


## Quick Start

### Start the MCP Server

```bash
mcp-space-life-sciences
```

### Example 1: Space Biology to Drug Discovery

```python
from mcp_space_life_sciences import IntegratedKGClient

client = IntegratedKGClient()

# 1. Get differentially expressed genes from space experiment
de_genes = client.get_genelab_de_genes(
    assay_id="OSD-253-6c5f9f37b9cb2ebeb2743875af4bdc86",
    log2fc_threshold=1.0
)

# 2. Enrich with PrimeKG annotations
enrichment = client.enrich_with_primekg(
    gene_names=de_genes['upregulated'][:50],
    include_drugs=True,
    include_diseases=True,
    include_pathways=True
)

# 3. Find therapeutic candidates
drug_targets = client.find_drug_targets_for_genes(
    gene_names=de_genes['upregulated'][:50]
)

# 4. Add geospatial context from SPOKE-OKN
diseases_by_location = client.get_disease_prevalence_by_location(
    disease_names=enrichment['diseases'][:10],
    location="United States"
)

print(f"Found {len(drug_targets)} potential therapeutic targets")
print(f"Disease prevalence data for {len(diseases_by_location)} diseases")
```

### Example 2: Complete Mechanism Analysis

```python
# Analyze mechanism from genes through pathways to drugs and diseases
mechanism = client.analyze_complete_mechanism(
    gene_list=["TP53", "BRCA1", "EGFR"],
    include_anatomy=True,
    include_geospatial=True
)

# Creates visualization showing:
# - Gene interactions
# - Pathway memberships  
# - Disease associations
# - Drug targets
# - Tissue expression
# - Geographic disease prevalence
```

## Common Node Types & Mappings

| Node Type | GeneLab | PrimeKG | SPOKE-OKN | Identifier |
|-----------|---------|---------|-----------|------------|
| **Genes** | Gene | gene/protein | Gene | gene_symbol |
| **Diseases** | Disease | disease | Disease | mondo_id |
| **Anatomy** | Anatomy | anatomy | (related) | uberon_id |
| **Pathways** | Pathway | pathway | - | reactome_id |
| **Drugs** | Compound | drug | ChemicalEntity | drugbank_id |
| **GO BP** | BiologicalProcess | biological_process | - | go_id |
| **GO MF** | MolecularFunction | molecular_function | - | go_id |
| **GO CC** | CellularComponent | cellular_component | - | go_id |
| **Locations** | - | - | AdministrativeArea | geonames_code |

**Total Integration**: 8 node types × 3 KGs = Comprehensive biomedical coverage

## Available Tools

### Gene-Focused Analysis
- `get_genelab_de_genes` - Get differentially expressed genes from space experiments
- `enrich_genes_with_primekg` - Add PrimeKG annotations
- `find_drug_targets_for_genes` - Identify therapeutic candidates
- `find_genes_in_anatomy` - Tissue-specific expression patterns
- `find_genes_by_location` - Genes relevant to geographic diseases (via SPOKE-OKN)

### Disease-Focused Analysis  
- `find_disease_genes` - Genes associated with diseases
- `find_disease_pathways` - Mechanisms underlying diseases
- `find_drugs_for_disease` - Therapeutic options
- `get_disease_prevalence_by_location` - Geographic distribution (SPOKE-OKN)
- `find_sdoh_disease_associations` - Social determinants impact (SPOKE-OKN)

### Pathway Analysis
- `find_shared_pathways` - Pathways enriched in gene lists
- `find_drugs_for_pathway` - Target specific biological pathways
- `compare_pathway_enrichment` - Cross-condition analysis

### Drug Discovery
- `find_drug_disease_mechanisms` - Complete mechanistic understanding
- `find_drug_targets` - Gene targets for drugs
- `find_drug_interactions` - Drug-drug interactions (SPOKE-OKN)
- `find_drug_environmental_interactions` - Drug-environment factors (SPOKE-OKN)

### Geospatial Analysis (SPOKE-OKN)
- `get_disease_prevalence_by_location` - Disease rates by state/county
- `get_chemical_exposures_by_location` - Environmental contaminants
- `get_sdoh_by_location` - Social determinants of health
- `find_organism_antimicrobial_resistance` - AMR patterns by location

### Multi-Graph Integration
- `find_common_nodes` - Nodes present in multiple KGs
- `enrich_across_all_kgs` - Complete annotation from all sources
- `analyze_complete_mechanism` - End-to-end mechanistic analysis
- `compare_gene_sets_multi_kg` - Cross-graph gene set comparison

### Visualization
- `create_multi_kg_network` - Network across all 3 KGs
- `create_gene_network` - Gene interaction networks
- `create_drug_target_heatmap` - Drug-gene targeting matrix
- `create_pathway_enrichment_plot` - Enriched pathways
- `create_disease_gene_network` - Disease-gene associations
- `create_anatomical_heatmap` - Tissue expression patterns
- `create_geospatial_disease_map` - Geographic disease distribution (SPOKE-OKN)

## Use Cases

### 1. Space Biology Research
**Question**: What are the biological consequences of microgravity exposure?

**Workflow**:
1. Query GeneLab for differentially expressed genes from microgravity experiments
2. Enrich genes with PrimeKG pathways, diseases, and drug targets
3. Check SPOKE-OKN for terrestrial disease prevalence of identified conditions
4. Identify drug countermeasures

### 2. Countermeasure Development
**Question**: What drugs could mitigate space-induced bone loss?

**Workflow**:
1. Get bone loss-related genes from GeneLab experiments
2. Find diseases associated with these genes in PrimeKG
3. Identify drugs targeting these genes/pathways in PrimeKG
4. Check drug-drug interactions and contraindications via SPOKE-OKN

### 3. Risk Assessment
**Question**: Which diseases show increased risk in space environments?

**Workflow**:
1. Analyze GeneLab gene expression changes
2. Map to diseases in PrimeKG
3. Compare with terrestrial disease prevalence in SPOKE-OKN
4. Identify geographic populations at higher baseline risk

### 4. Environmental Health
**Question**: Do chemical exposures on Earth mirror biological effects seen in space?

**Workflow**:
1. Get GeneLab differential expression signatures
2. Find chemicals that cause similar gene expression in PrimeKG
3. Check SPOKE-OKN for geographic distribution of those chemicals
4. Correlate with disease prevalence patterns

### 5. Systems Medicine
**Question**: How do genes, pathways, diseases, drugs, and environment interact?

**Workflow**:
1. Start with any entity (gene, disease, drug, location)
2. Trace connections across all three knowledge graphs
3. Build comprehensive multi-entity network
4. Visualize and analyze system-level patterns

## Documentation

- [Installation Guide](docs/installation.md)
- [Quick Start Tutorial](docs/quickstart.md)
- [API Reference](docs/api_reference.md)
- [Integration Architecture](docs/architecture.md)
- [Example Workflows](examples/)
- [Cypher Query Library](docs/cypher_queries.md)
- [SPARQL Query Library](docs/sparql_queries.md)

## Examples

See the [`examples/`](examples/) directory for Jupyter notebooks:

- `01_space_biology_to_therapeutics.ipynb` - From GeneLab to drug discovery
- `02_disease_mechanism_discovery.ipynb` - Multi-KG disease analysis
- `03_geospatial_disease_patterns.ipynb` - Geographic health patterns
- `04_environmental_health_connections.ipynb` - Chemical exposures and biology
- `05_complete_mechanism_analysis.ipynb` - End-to-end systems analysis

## Citation

If you use this integration in your research, please cite:

### This Work
```bibtex
@software{mcp_space_life_sciences2025,
  author = {[Amanda Saravia-Butler]},
  title = {MCP Space Life Sciences KGs: Integrated Knowledge Graph Server},
  year = {2026},
  url = {https://github.com/asaravia-butler/MCP_Space_Life_Science_KGs}
}
```

### Constituent Knowledge Graphs

**PrimeKG**:
```bibtex
@article{chandak2023building,
  title={Building a knowledge graph to enable precision medicine},
  author={Chandak, Payal and Huang, Kexin and Zitnik, Marinka},
  journal={Scientific Data},
  volume={10},
  number={1},
  pages={67},
  year={2023},
  publisher={Nature Publishing Group}
}
```

**GeneLab**:
```bibtex
@article{gebre2025osdr,
  title={NASA open science data repository: open science for life in space},
  author={Gebre SG, Scott RT, Saravia-Butler AM, Lopez DK, Sanders LM, Costes SV},
  journal={Nucleic Acids Res.},
  volume={53},
  number={D1},
  pages={D1697-D1710},
  year={2025}
}
```

**SPOKE**:
```bibtex
@article{nelson2022spoke,
  title={The SPOKE knowledge graph},
  author={Nelson, Charlotte A and Butte, Atul J and Baranzini, Sergio E},
  journal={Bioinformatics},
  volume={38},
  number={15},
  pages={3749--3756},
  year={2022}
}
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/asaravia-butler/MCP_Space_Life_Science_KGs.git
cd MCP_Space_Life_Science_KGs
pip install -e ".[dev]"
pytest tests/
```

## License

Apache 2.0 License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

This work integrates three exceptional knowledge graph resources:

- **GeneLab Team** at NASA Ames Research Center
- **Zitnik Lab** at Harvard Medical School (PrimeKG)
- **Baranzini Lab** at UCSF (SPOKE/SPOKE-OKN)
- **RENCI** (Renaissance Computing Institute) for SPOKE-OKN infrastructure

Special thanks to the open science community for making these resources available.

## Contact

- **Issues**: [GitHub Issues](https://github.com/asaravia-butler/MCP_Space_Life_Science_KGs/issues)
- **Discussions**: [GitHub Discussions](https://github.com/asaravia-butler/MCP_Space_Life_Science_KGs/discussions)

## Related Projects

- [mcp-genelab](https://github.com/sbl-sdsc/mcp-genelab) - GeneLab MCP server
- [MCP_Harvard_PrimeKG](https://github.com/asaravia-butler/MCP_Harvard_PrimeKG) - PrimeKG MCP server
- [mcp-proto-okn](https://github.com/sbl-sdsc/mcp-proto-okn) - SPOKE-OKN MCP server
- [spoke_genelab](https://github.com/BaranziniLab/spoke_genelab) - GeneLab knowledge graph

---

**Built with ❤️ for space life sciences research**
