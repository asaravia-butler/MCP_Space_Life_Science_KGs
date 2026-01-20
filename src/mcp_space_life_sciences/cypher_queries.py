"""
COMPREHENSIVE Cypher Query Templates for ALL Common Node Types
GeneLab-PrimeKG Integration

Covers 8 node types: Genes, Diseases, Anatomy, Pathways, Drugs, and 3 GO categories
"""

# ===========================================================================
# SECTION 1: NODE EXISTENCE QUERIES (Check if nodes exist in PrimeKG)
# ===========================================================================

# 1.1 Find genes by symbol
FIND_GENES_BY_SYMBOL = """
MATCH (g:`gene/protein`)
WHERE g.node_name IN $gene_symbols
RETURN g.node_name AS gene_symbol,
       g.node_id AS gene_id,
       g.node_index AS node_index
"""

# 1.2 Find diseases by MONDO ID
FIND_DISEASES_BY_MONDO = """
MATCH (d:disease)
WHERE d.node_id IN $mondo_ids
   OR d.node_name IN $disease_names
RETURN d.node_name AS disease_name,
       d.node_id AS disease_id,
       d.node_source AS source
"""

# 1.3 Find anatomy by UBERON ID
FIND_ANATOMY_BY_UBERON = """
MATCH (a:anatomy)
WHERE a.node_id IN $uberon_ids
   OR a.node_name IN $anatomy_names
RETURN a.node_name AS anatomy_name,
       a.node_id AS uberon_id,
       a.node_index AS node_index
"""

# 1.4 Find pathways by Reactome ID
FIND_PATHWAYS_BY_REACTOME = """
MATCH (p:pathway)
WHERE p.node_id IN $reactome_ids
   OR p.node_name IN $pathway_names
RETURN p.node_name AS pathway_name,
       p.node_id AS reactome_id,
       p.node_source AS source
"""

# 1.5 Find drugs by DrugBank ID
FIND_DRUGS_BY_DRUGBANK = """
MATCH (d:drug)
WHERE d.node_id IN $drugbank_ids
   OR d.node_name IN $drug_names
RETURN d.node_name AS drug_name,
       d.node_id AS drugbank_id,
       d.node_source AS source
"""

# 1.6 Find GO Biological Processes
FIND_GO_BIOLOGICAL_PROCESSES = """
MATCH (bp:biological_process)
WHERE bp.node_id IN $go_ids
   OR bp.node_name IN $term_names
RETURN bp.node_name AS term_name,
       bp.node_id AS go_id
"""

# 1.7 Find GO Molecular Functions
FIND_GO_MOLECULAR_FUNCTIONS = """
MATCH (mf:molecular_function)
WHERE mf.node_id IN $go_ids
   OR mf.node_name IN $term_names
RETURN mf.node_name AS term_name,
       mf.node_id AS go_id
"""

# 1.8 Find GO Cellular Components
FIND_GO_CELLULAR_COMPONENTS = """
MATCH (cc:cellular_component)
WHERE cc.node_id IN $go_ids
   OR cc.node_name IN $term_names
RETURN cc.node_name AS term_name,
       cc.node_id AS go_id
"""

# ===========================================================================
# SECTION 2: CROSS-NODE ENRICHMENT QUERIES
# ===========================================================================

# 2.1 Enrich genes with ALL annotations
COMPREHENSIVE_GENE_ENRICHMENT = """
MATCH (g:`gene/protein`)
WHERE g.node_name IN $gene_names
OPTIONAL MATCH (g)-[r_drug:drug_protein]-(d:drug)
OPTIONAL MATCH (g)-[r_disease:disease_protein]-(dis:disease)
OPTIONAL MATCH (g)-[r_pathway:pathway_protein]-(p:pathway)
OPTIONAL MATCH (g)-[r_bp:bioprocess_protein]-(bp:biological_process)
OPTIONAL MATCH (g)-[r_mf:molfunc_protein]-(mf:molecular_function)
OPTIONAL MATCH (g)-[r_cc:cellcomp_protein]-(cc:cellular_component)
OPTIONAL MATCH (g)-[r_anat_present:anatomy_protein_present]-(a_present:anatomy)
OPTIONAL MATCH (g)-[r_anat_absent:anatomy_protein_absent]-(a_absent:anatomy)
RETURN g.node_name AS gene_name,
       g.node_id AS gene_id,
       collect(DISTINCT {name: d.node_name, id: d.node_id}) AS drugs,
       collect(DISTINCT {name: dis.node_name, id: dis.node_id}) AS diseases,
       collect(DISTINCT {name: p.node_name, id: p.node_id}) AS pathways,
       collect(DISTINCT {name: bp.node_name, id: bp.node_id}) AS biological_processes,
       collect(DISTINCT {name: mf.node_name, id: mf.node_id}) AS molecular_functions,
       collect(DISTINCT {name: cc.node_name, id: cc.node_id}) AS cellular_components,
       collect(DISTINCT {name: a_present.node_name, id: a_present.node_id}) AS expressed_in,
       collect(DISTINCT {name: a_absent.node_name, id: a_absent.node_id}) AS not_expressed_in
"""

# 2.2 Enrich diseases with genes, pathways, drugs, anatomy
COMPREHENSIVE_DISEASE_ENRICHMENT = """
MATCH (dis:disease)
WHERE dis.node_id IN $disease_ids OR dis.node_name IN $disease_names
OPTIONAL MATCH (dis)-[r_gene:disease_protein]-(g:`gene/protein`)
OPTIONAL MATCH (g)-[r_pathway:pathway_protein]-(p:pathway)
OPTIONAL MATCH (g)-[r_drug:drug_protein]-(d:drug)
OPTIONAL MATCH (g)-[r_anat:anatomy_protein_present]-(a:anatomy)
OPTIONAL MATCH (dis)-[r_pheno:disease_phenotype_positive]-(pheno:effect/phenotype)
WITH dis, 
     collect(DISTINCT {gene: g.node_name, gene_id: g.node_id}) AS genes,
     collect(DISTINCT {pathway: p.node_name, pathway_id: p.node_id}) AS pathways,
     collect(DISTINCT {drug: d.node_name, drug_id: d.node_id}) AS drugs,
     collect(DISTINCT {anatomy: a.node_name, anatomy_id: a.node_id}) AS anatomies,
     collect(DISTINCT {phenotype: pheno.node_name}) AS phenotypes
RETURN dis.node_name AS disease_name,
       dis.node_id AS disease_id,
       genes,
       pathways,
       drugs,
       anatomies,
       phenotypes,
       size(genes) AS gene_count,
       size(pathways) AS pathway_count,
       size(drugs) AS drug_count
"""

# 2.3 Enrich anatomy with genes and their functions
COMPREHENSIVE_ANATOMY_ENRICHMENT = """
MATCH (a:anatomy)
WHERE a.node_id IN $anatomy_ids OR a.node_name IN $anatomy_names
OPTIONAL MATCH (a)-[r_present:anatomy_protein_present]-(g_present:`gene/protein`)
OPTIONAL MATCH (a)-[r_absent:anatomy_protein_absent]-(g_absent:`gene/protein`)
OPTIONAL MATCH (g_present)-[r_pathway:pathway_protein]-(p:pathway)
OPTIONAL MATCH (g_present)-[r_disease:disease_protein]-(d:disease)
WITH a,
     collect(DISTINCT {gene: g_present.node_name, gene_id: g_present.node_id}) AS expressed_genes,
     collect(DISTINCT {gene: g_absent.node_name, gene_id: g_absent.node_id}) AS absent_genes,
     collect(DISTINCT {pathway: p.node_name, pathway_id: p.node_id}) AS pathways,
     collect(DISTINCT {disease: d.node_name, disease_id: d.node_id}) AS diseases
RETURN a.node_name AS anatomy_name,
       a.node_id AS anatomy_id,
       expressed_genes,
       absent_genes,
       pathways,
       diseases,
       size(expressed_genes) AS expressed_gene_count,
       size(absent_genes) AS absent_gene_count
"""

# 2.4 Enrich pathways with genes, diseases, drugs
COMPREHENSIVE_PATHWAY_ENRICHMENT = """
MATCH (p:pathway)
WHERE p.node_id IN $pathway_ids OR p.node_name IN $pathway_names
OPTIONAL MATCH (p)-[r_gene:pathway_protein]-(g:`gene/protein`)
OPTIONAL MATCH (g)-[r_disease:disease_protein]-(d:disease)
OPTIONAL MATCH (g)-[r_drug:drug_protein]-(drug:drug)
OPTIONAL MATCH (g)-[r_anat:anatomy_protein_present]-(a:anatomy)
WITH p,
     collect(DISTINCT {gene: g.node_name, gene_id: g.node_id}) AS genes,
     collect(DISTINCT {disease: d.node_name, disease_id: d.node_id}) AS diseases,
     collect(DISTINCT {drug: drug.node_name, drug_id: drug.node_id}) AS drugs,
     collect(DISTINCT {anatomy: a.node_name, anatomy_id: a.node_id}) AS anatomies
RETURN p.node_name AS pathway_name,
       p.node_id AS pathway_id,
       p.node_source AS source,
       genes,
       diseases,
       drugs,
       anatomies,
       size(genes) AS gene_count,
       size(diseases) AS disease_count,
       size(drugs) AS drug_count
"""

# 2.5 Enrich drugs with targets, diseases, pathways, anatomy
COMPREHENSIVE_DRUG_ENRICHMENT = """
MATCH (drug:drug)
WHERE drug.node_id IN $drug_ids OR drug.node_name IN $drug_names
OPTIONAL MATCH (drug)-[r_target:drug_protein]-(g:`gene/protein`)
OPTIONAL MATCH (drug)-[r_indication:indication]-(d_ind:disease)
OPTIONAL MATCH (drug)-[r_contraind:contraindication]-(d_contra:disease)
OPTIONAL MATCH (g)-[r_pathway:pathway_protein]-(p:pathway)
OPTIONAL MATCH (g)-[r_anat:anatomy_protein_present]-(a:anatomy)
WITH drug,
     collect(DISTINCT {gene: g.node_name, gene_id: g.node_id}) AS targets,
     collect(DISTINCT {disease: d_ind.node_name, disease_id: d_ind.node_id}) AS indications,
     collect(DISTINCT {disease: d_contra.node_name, disease_id: d_contra.node_id}) AS contraindications,
     collect(DISTINCT {pathway: p.node_name, pathway_id: p.node_id}) AS affected_pathways,
     collect(DISTINCT {anatomy: a.node_name, anatomy_id: a.node_id}) AS target_tissues
RETURN drug.node_name AS drug_name,
       drug.node_id AS drug_id,
       targets,
       indications,
       contraindications,
       affected_pathways,
       target_tissues,
       size(targets) AS target_count,
       size(indications) AS indication_count
"""

# ===========================================================================
# SECTION 3: ANATOMY-SPECIFIC QUERIES
# ===========================================================================

# 3.1 Find genes expressed in anatomy
FIND_GENES_IN_ANATOMY = """
MATCH (a:anatomy)-[r:anatomy_protein_present]-(g:`gene/protein`)
WHERE a.node_id IN $anatomy_ids OR a.node_name IN $anatomy_names
RETURN a.node_name AS anatomy_name,
       a.node_id AS anatomy_id,
       collect(g.node_name) AS expressed_genes,
       count(g) AS gene_count
ORDER BY gene_count DESC
"""

# 3.2 Find genes NOT expressed in anatomy
FIND_GENES_ABSENT_IN_ANATOMY = """
MATCH (a:anatomy)-[r:anatomy_protein_absent]-(g:`gene/protein`)
WHERE a.node_id IN $anatomy_ids OR a.node_name IN $anatomy_names
RETURN a.node_name AS anatomy_name,
       a.node_id AS anatomy_id,
       collect(g.node_name) AS absent_genes,
       count(g) AS gene_count
"""

# 3.3 Compare gene expression across anatomies
COMPARE_ANATOMICAL_EXPRESSION = """
WITH $anatomy_list AS anatomies
UNWIND anatomies AS anatomy_name
MATCH (a:anatomy {node_name: anatomy_name})-[r:anatomy_protein_present]-(g:`gene/protein`)
WITH anatomy_name, collect(DISTINCT g.node_name) AS genes
RETURN anatomy_name, genes, size(genes) AS gene_count
ORDER BY gene_count DESC
"""

# 3.4 Find anatomies where specific genes are expressed
FIND_ANATOMIES_FOR_GENES = """
MATCH (g:`gene/protein`)-[r:anatomy_protein_present]-(a:anatomy)
WHERE g.node_name IN $gene_names
WITH g.node_name AS gene,
     collect({name: a.node_name, id: a.node_id}) AS anatomies,
     count(a) AS anatomy_count
RETURN gene, anatomies, anatomy_count
ORDER BY anatomy_count DESC
"""

# ===========================================================================
# SECTION 4: DISEASE-CENTERED QUERIES
# ===========================================================================

# 4.1 Find pathways associated with disease (via genes)
FIND_DISEASE_PATHWAYS = """
MATCH (d:disease)-[r_gene:disease_protein]-(g:`gene/protein`)-[r_path:pathway_protein]-(p:pathway)
WHERE d.node_id IN $disease_ids OR d.node_name IN $disease_names
WITH d.node_name AS disease,
     p.node_name AS pathway,
     p.node_id AS pathway_id,
     collect(DISTINCT g.node_name) AS connecting_genes,
     count(DISTINCT g) AS gene_count
WHERE gene_count >= $min_genes
RETURN disease, pathway, pathway_id, connecting_genes, gene_count
ORDER BY gene_count DESC
"""

# 4.2 Find drugs for disease (via indications and gene targets)
FIND_DRUGS_FOR_DISEASE = """
MATCH (d:disease)
WHERE d.node_id IN $disease_ids OR d.node_name IN $disease_names
// Direct indications
OPTIONAL MATCH (drug1:drug)-[r_ind:indication]-(d)
// Via gene targets
OPTIONAL MATCH (d)-[r_gene:disease_protein]-(g:`gene/protein`)-[r_drug:drug_protein]-(drug2:drug)
WITH d.node_name AS disease,
     collect(DISTINCT {drug: drug1.node_name, drug_id: drug1.node_id, type: 'indication'}) AS direct_drugs,
     collect(DISTINCT {drug: drug2.node_name, drug_id: drug2.node_id, type: 'target', gene: g.node_name}) AS target_drugs
RETURN disease, direct_drugs, target_drugs,
       size(direct_drugs) AS direct_drug_count,
       size(target_drugs) AS target_drug_count
"""

# 4.3 Find common pathways across diseases
FIND_COMMON_PATHWAYS_ACROSS_DISEASES = """
MATCH (d:disease)-[r_gene:disease_protein]-(g:`gene/protein`)-[r_path:pathway_protein]-(p:pathway)
WHERE d.node_name IN $disease_names OR d.node_id IN $disease_ids
WITH p.node_name AS pathway,
     p.node_id AS pathway_id,
     collect(DISTINCT d.node_name) AS diseases,
     collect(DISTINCT g.node_name) AS genes,
     count(DISTINCT d) AS disease_count,
     count(DISTINCT g) AS gene_count
WHERE disease_count >= $min_diseases
RETURN pathway, pathway_id, diseases, genes, disease_count, gene_count
ORDER BY disease_count DESC, gene_count DESC
"""

# 4.4 Find anatomical locations associated with disease
FIND_DISEASE_ANATOMY = """
MATCH (d:disease)-[r_gene:disease_protein]-(g:`gene/protein`)-[r_anat:anatomy_protein_present]-(a:anatomy)
WHERE d.node_name IN $disease_names OR d.node_id IN $disease_ids
WITH d.node_name AS disease,
     a.node_name AS anatomy,
     a.node_id AS anatomy_id,
     collect(DISTINCT g.node_name) AS genes,
     count(DISTINCT g) AS gene_count
WHERE gene_count >= $min_genes
RETURN disease, anatomy, anatomy_id, genes, gene_count
ORDER BY gene_count DESC
"""

# ===========================================================================
# SECTION 5: PATHWAY-CENTERED QUERIES
# ===========================================================================

# 5.1 Find drugs targeting pathway
FIND_DRUGS_FOR_PATHWAY = """
MATCH (p:pathway)-[r_gene:pathway_protein]-(g:`gene/protein`)-[r_drug:drug_protein]-(d:drug)
WHERE p.node_name IN $pathway_names OR p.node_id IN $pathway_ids
WITH p.node_name AS pathway,
     d.node_name AS drug,
     d.node_id AS drug_id,
     collect(DISTINCT g.node_name) AS target_genes,
     count(DISTINCT g) AS gene_count
RETURN pathway, drug, drug_id, target_genes, gene_count
ORDER BY gene_count DESC
LIMIT $limit_per_pathway
"""

# 5.2 Find diseases associated with pathway
FIND_DISEASES_FOR_PATHWAY = """
MATCH (p:pathway)-[r_gene:pathway_protein]-(g:`gene/protein`)-[r_disease:disease_protein]-(d:disease)
WHERE p.node_name IN $pathway_names OR p.node_id IN $pathway_ids
WITH p.node_name AS pathway,
     d.node_name AS disease,
     d.node_id AS disease_id,
     collect(DISTINCT g.node_name) AS connecting_genes,
     count(DISTINCT g) AS gene_count
WHERE gene_count >= $min_genes
RETURN pathway, disease, disease_id, connecting_genes, gene_count
ORDER BY gene_count DESC
"""

# 5.3 Find anatomies where pathway genes are expressed
FIND_ANATOMY_FOR_PATHWAY = """
MATCH (p:pathway)-[r_gene:pathway_protein]-(g:`gene/protein`)-[r_anat:anatomy_protein_present]-(a:anatomy)
WHERE p.node_name IN $pathway_names OR p.node_id IN $pathway_ids
WITH p.node_name AS pathway,
     a.node_name AS anatomy,
     a.node_id AS anatomy_id,
     collect(DISTINCT g.node_name) AS genes,
     count(DISTINCT g) AS gene_count
WHERE gene_count >= $min_genes
RETURN pathway, anatomy, anatomy_id, genes, gene_count
ORDER BY gene_count DESC
"""

# ===========================================================================
# SECTION 6: DRUG-DISEASE MECHANISM QUERIES
# ===========================================================================

# 6.1 Comprehensive drug-disease mechanism
FIND_DRUG_DISEASE_MECHANISMS = """
MATCH (drug:drug {node_name: $drug_name})
MATCH (disease:disease {node_name: $disease_name})

// Path 1: Direct indication
OPTIONAL MATCH path1 = (drug)-[r_ind:indication]-(disease)

// Path 2: Via gene targets
OPTIONAL MATCH path2 = (drug)-[r_drug:drug_protein]-(g:`gene/protein`)-[r_disease:disease_protein]-(disease)

// Path 3: Via pathways
OPTIONAL MATCH path3 = (drug)-[r_drug3:drug_protein]-(g3:`gene/protein`)-[r_path:pathway_protein]-(p:pathway)-[r_path2:pathway_protein]-(g4:`gene/protein`)-[r_disease3:disease_protein]-(disease)

// Path 4: Via anatomy
OPTIONAL MATCH (g2:`gene/protein`)-[r_drug2:drug_protein]-(drug)
OPTIONAL MATCH (g2)-[r_anat1:anatomy_protein_present]-(a:anatomy)-[r_anat2:anatomy_protein_present]-(g5:`gene/protein`)-[r_disease2:disease_protein]-(disease)

WITH drug, disease,
     CASE WHEN path1 IS NOT NULL THEN 'direct_indication' ELSE NULL END AS direct,
     collect(DISTINCT {gene: g.node_name, gene_id: g.node_id}) AS gene_targets,
     collect(DISTINCT {pathway: p.node_name, pathway_id: p.node_id, genes: [g3.node_name, g4.node_name]}) AS pathway_mechanisms,
     collect(DISTINCT {anatomy: a.node_name, anatomy_id: a.node_id, genes: [g2.node_name, g5.node_name]}) AS anatomical_context

RETURN drug.node_name AS drug_name,
       disease.node_name AS disease_name,
       direct,
       gene_targets,
       pathway_mechanisms,
       anatomical_context,
       size(gene_targets) AS target_count,
       size(pathway_mechanisms) AS pathway_count,
       size(anatomical_context) AS anatomy_count
"""

# 6.2 Find drug repurposing candidates for disease
FIND_DRUG_REPURPOSING_CANDIDATES = """
MATCH (disease:disease)
WHERE disease.node_name = $disease_name OR disease.node_id = $disease_id

// Get genes associated with disease
MATCH (disease)-[r_gene:disease_protein]-(g:`gene/protein`)
WITH disease, collect(g) AS disease_genes

// Find drugs targeting these genes
UNWIND disease_genes AS dg
MATCH (dg)-[r_drug:drug_protein]-(drug:drug)

// Exclude drugs with contraindication for this disease
WHERE NOT (drug)-[:contraindication]-(disease)

WITH disease.node_name AS disease,
     drug.node_name AS drug,
     drug.node_id AS drug_id,
     collect(DISTINCT dg.node_name) AS target_genes,
     count(DISTINCT dg) AS target_count

// Check if drug has indication for related diseases
OPTIONAL MATCH (drug)-[r_ind:indication]-(related_disease:disease)
WITH disease, drug, drug_id, target_genes, target_count,
     collect(DISTINCT related_disease.node_name) AS indicated_for

RETURN drug, drug_id, target_genes, target_count, indicated_for,
       CASE 
         WHEN size(indicated_for) > 0 THEN 'approved_for_related'
         ELSE 'novel_repurposing'
       END AS repurposing_type
ORDER BY target_count DESC
LIMIT $limit
"""

# ===========================================================================
# SECTION 7: MULTI-NODE INTEGRATION QUERIES
# ===========================================================================

# 7.1 Find all connections between gene list and entity types
MULTI_NODE_ENTITY_ENRICHMENT = """
WITH $gene_names AS genes
UNWIND genes AS gene_name
MATCH (g:`gene/protein` {node_name: gene_name})

// Get all connected entities
OPTIONAL MATCH (g)-[r_drug:drug_protein]-(d:drug)
OPTIONAL MATCH (g)-[r_disease:disease_protein]-(dis:disease)
OPTIONAL MATCH (g)-[r_pathway:pathway_protein]-(p:pathway)
OPTIONAL MATCH (g)-[r_bp:bioprocess_protein]-(bp:biological_process)
OPTIONAL MATCH (g)-[r_mf:molfunc_protein]-(mf:molecular_function)
OPTIONAL MATCH (g)-[r_cc:cellcomp_protein]-(cc:cellular_component)
OPTIONAL MATCH (g)-[r_anat:anatomy_protein_present]-(a:anatomy)

RETURN gene_name,
       collect(DISTINCT {type: 'drug', name: d.node_name, id: d.node_id}) AS drugs,
       collect(DISTINCT {type: 'disease', name: dis.node_name, id: dis.node_id}) AS diseases,
       collect(DISTINCT {type: 'pathway', name: p.node_name, id: p.node_id}) AS pathways,
       collect(DISTINCT {type: 'go_bp', name: bp.node_name, id: bp.node_id}) AS go_biological_processes,
       collect(DISTINCT {type: 'go_mf', name: mf.node_name, id: mf.node_id}) AS go_molecular_functions,
       collect(DISTINCT {type: 'go_cc', name: cc.node_name, id: cc.node_id}) AS go_cellular_components,
       collect(DISTINCT {type: 'anatomy', name: a.node_name, id: a.node_id}) AS anatomies
"""

# 7.2 Cross-entity comparison
COMPARE_ENTITIES_ACROSS_TYPES = """
WITH $entity_set_1 AS set1, $entity_set_2 AS set2

// For genes in set 1
UNWIND set1.genes AS gene1
MATCH (g1:`gene/protein` {node_name: gene1})
OPTIONAL MATCH (g1)-[r:pathway_protein]-(p1:pathway)
WITH collect(DISTINCT p1.node_name) AS pathways1

// For genes in set 2
UNWIND set2.genes AS gene2
MATCH (g2:`gene/protein` {node_name: gene2})
OPTIONAL MATCH (g2)-[r:pathway_protein]-(p2:pathway)
WITH pathways1, collect(DISTINCT p2.node_name) AS pathways2

// Find overlaps
WITH [x IN pathways1 WHERE x IN pathways2] AS shared_pathways,
     [x IN pathways1 WHERE NOT x IN pathways2] AS set1_unique,
     [x IN pathways2 WHERE NOT x IN pathways1] AS set2_unique

RETURN shared_pathways,
       set1_unique,
       set2_unique,
       size(shared_pathways) AS overlap_count
"""

# ===========================================================================
# EXAMPLE USAGE PARAMETERS
# ===========================================================================

EXAMPLE_PARAMS = {
    "multi_node_query": {
        "gene_names": ["TP53", "BRCA1", "EGFR"],
        "disease_names": ["breast cancer", "lung cancer"],
        "anatomy_names": ["lung", "breast"],
        "pathway_names": ["Apoptosis"],
        "drug_names": ["Aspirin"]
    },
    "disease_enrichment": {
        "disease_ids": ["MONDO:0004992"],
        "disease_names": ["breast cancer"]
    },
    "anatomy_expression": {
        "anatomy_ids": ["UBERON:0002048"],
        "anatomy_names": ["lung"]
    },
    "pathway_drugs": {
        "pathway_names": ["Apoptosis", "MAPK signaling"],
        "pathway_ids": ["R-HSA-109581"],
        "limit_per_pathway": 20
    },
    "drug_disease_mechanism": {
        "drug_name": "Aspirin",
        "disease_name": "cardiovascular disease"
    },
    "common_pathways_diseases": {
        "disease_names": ["breast cancer", "ovarian cancer", "prostate cancer"],
        "min_diseases": 2
    }
}

"""
USAGE NOTES:
============

1. All queries use parameterized inputs for safety and reusability
2. Queries support both ID-based and name-based lookups
3. Most queries include optional MATCH clauses to handle missing relationships
4. Results are aggregated to avoid cartesian products
5. Ordering prioritizes most relevant results (by count, relevance)

INTEGRATION WORKFLOW:
=====================

1. Get entities from GeneLab (genes, diseases from experiments)
2. Use FIND_* queries to verify entities exist in PrimeKG
3. Use COMPREHENSIVE_*_ENRICHMENT to get full annotations
4. Use specific relationship queries for targeted analysis
5. Use MULTI_NODE_* queries for cross-entity insights

EXAMPLE INTEGRATION:
====================

# Step 1: Get GeneLab genes
genelab_genes = query_genelab("MATCH (a:Assay {assay_id: 'OSD-253...'})-[r:DIFF_GENE_EXPRESSED]->(g:Gene) RETURN g.gene_symbol")

# Step 2: Check which exist in PrimeKG
primekg_genes = query_primekg(FIND_GENES_BY_SYMBOL, {"gene_symbols": genelab_genes})

# Step 3: Get comprehensive enrichment
enrichment = query_primekg(COMPREHENSIVE_GENE_ENRICHMENT, {"gene_names": primekg_genes})

# Step 4: Find therapeutic targets
drug_targets = query_primekg(FIND_DRUGS_FOR_PATHWAY, {"pathway_names": enrichment['pathways']})

# Step 5: Understand mechanisms
mechanisms = query_primekg(FIND_DRUG_DISEASE_MECHANISMS, {"drug_name": drug_targets[0], "disease_name": ...})
"""
