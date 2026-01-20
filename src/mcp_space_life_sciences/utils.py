"""
Utility functions for MCP Space Life Sciences integration
"""

from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


def normalize_gene_symbol(gene_symbol: str) -> str:
    """
    Normalize gene symbol to standard format.
    
    Args:
        gene_symbol: Gene symbol to normalize
        
    Returns:
        Normalized gene symbol (uppercase, stripped)
    """
    return gene_symbol.strip().upper()


def normalize_gene_list(gene_list: List[str]) -> List[str]:
    """
    Normalize a list of gene symbols.
    
    Args:
        gene_list: List of gene symbols
        
    Returns:
        List of normalized gene symbols
    """
    return list(set([normalize_gene_symbol(g) for g in gene_list]))


def validate_mondo_id(mondo_id: str) -> bool:
    """
    Validate MONDO ID format.
    
    Args:
        mondo_id: MONDO identifier
        
    Returns:
        True if valid format
    """
    if not mondo_id:
        return False
    
    # Accept with or without prefix
    if mondo_id.startswith("MONDO:"):
        return len(mondo_id) > 6 and mondo_id[6:].isdigit()
    return mondo_id.isdigit()


def format_mondo_id(mondo_id: str) -> str:
    """
    Format MONDO ID with prefix.
    
    Args:
        mondo_id: MONDO identifier (with or without prefix)
        
    Returns:
        MONDO ID with MONDO: prefix
    """
    if not mondo_id.startswith("MONDO:"):
        return f"MONDO:{mondo_id}"
    return mondo_id


def validate_drugbank_id(drugbank_id: str) -> bool:
    """
    Validate DrugBank ID format.
    
    Args:
        drugbank_id: DrugBank identifier
        
    Returns:
        True if valid format (DB##### pattern)
    """
    if not drugbank_id:
        return False
    
    if drugbank_id.startswith("DB") and len(drugbank_id) == 7:
        return drugbank_id[2:].isdigit()
    return False


def batch_list(items: List[Any], batch_size: int = 50) -> List[List[Any]]:
    """
    Split list into batches.
    
    Args:
        items: List to batch
        batch_size: Size of each batch
        
    Returns:
        List of batches
    """
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]


def merge_enrichment_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge enrichment results from multiple queries.
    
    Args:
        results: List of enrichment dictionaries
        
    Returns:
        Merged enrichment dictionary
    """
    merged = {
        "genes": {},
        "summary": {
            "total_genes": 0,
            "genes_with_annotations": 0,
        }
    }
    
    for result in results:
        if "genes" in result:
            merged["genes"].update(result["genes"])
    
    merged["summary"]["total_genes"] = len(merged["genes"])
    merged["summary"]["genes_with_annotations"] = sum(
        1 for g in merged["genes"].values() 
        if any(g.get(k) for k in ["drugs", "diseases", "pathways"])
    )
    
    return merged


def extract_entity_names(entities: List[Dict[str, Any]], 
                         name_key: str = "name") -> List[str]:
    """
    Extract entity names from list of dictionaries.
    
    Args:
        entities: List of entity dictionaries
        name_key: Key for name field
        
    Returns:
        List of entity names
    """
    return [e.get(name_key) for e in entities if e.get(name_key)]


def format_sparql_list(items: List[str]) -> str:
    """
    Format Python list for SPARQL IN clause.
    
    Args:
        items: List of strings
        
    Returns:
        SPARQL-formatted list: ("item1" "item2")
    """
    return "(" + " ".join([f'"{item}"' for item in items]) + ")"


def parse_neo4j_result(result) -> List[Dict[str, Any]]:
    """
    Parse Neo4j query result to list of dictionaries.
    
    Args:
        result: Neo4j query result
        
    Returns:
        List of result dictionaries
    """
    return [dict(record) for record in result]


def calculate_enrichment_pvalue(gene_count: int, 
                                total_genes: int,
                                category_size: int,
                                total_categories: int) -> float:
    """
    Calculate enrichment p-value using hypergeometric test.
    
    Args:
        gene_count: Genes in category
        total_genes: Total genes queried
        category_size: Total genes in category
        total_categories: Total genes in database
        
    Returns:
        P-value
    """
    from scipy.stats import hypergeom
    
    pval = hypergeom.sf(
        gene_count - 1,
        total_categories,
        category_size,
        total_genes
    )
    
    return pval


def log_query_execution(query_type: str, 
                        num_results: int,
                        execution_time: float):
    """
    Log query execution statistics.
    
    Args:
        query_type: Type of query executed
        num_results: Number of results returned
        execution_time: Time taken in seconds
    """
    logger.info(
        f"Query: {query_type} | "
        f"Results: {num_results} | "
        f"Time: {execution_time:.2f}s"
    )
