# Node Type Mappings

## Complete Mapping Table

| Node Type | GeneLab | PrimeKG | SPOKE-OKN | Identifier |
|-----------|---------|---------|-----------|------------|
| Genes | Gene | gene/protein | Gene | gene_symbol |
| Diseases | Disease | disease | Disease | mondo_id |
| Anatomy | Anatomy | anatomy | - | uberon_id |
| Pathways | Pathway | pathway | - | reactome_id |
| Drugs | Compound | drug | ChemicalEntity | drugbank_id |
| GO BP | BiologicalProcess | biological_process | - | go_id |
| GO MF | MolecularFunction | molecular_function | - | go_id |
| GO CC | CellularComponent | cellular_component | - | go_id |

## Integration Strategies

### Gene Mapping
- Primary: gene_symbol (e.g., "TP53")
- Secondary: ensembl_id, entrez_id

### Disease Mapping
- Primary: mondo_id (e.g., "MONDO:0004992")
- Secondary: disease_name, doid, umls_cui

### Drug Mapping
- Primary: drugbank_id (e.g., "DB00001")
- Secondary: chembl_id, pubchem_cid

See [COMPLETE_INTEGRATION_SUMMARY.md](COMPLETE_INTEGRATION_SUMMARY.md) for details.
