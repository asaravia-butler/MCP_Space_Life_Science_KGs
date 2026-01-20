"""
Enhanced MCP Server for Harvard PrimeKG Knowledge Graph
Provides tools to query and explore the PrimeKG precision medicine knowledge graph
with GeneLab integration and visualization capabilities.
"""

import os
import logging
from typing import Any, Optional
from pathlib import Path
import json

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from .primekg_client import PrimeKGClient

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-primekg")

# Get configuration from environment
DATA_PATH = os.getenv("PRIMEKG_DATA_PATH", str(Path.home() / "primekg_data"))
AUTO_UPDATE = os.getenv("PRIMEKG_AUTO_UPDATE", "true").lower() == "true"
UPDATE_INTERVAL_DAYS = int(os.getenv("PRIMEKG_UPDATE_INTERVAL_DAYS", "7"))
INSTRUCTIONS = os.getenv("INSTRUCTIONS", 
    "Query the PrimeKG knowledge graph for precision medicine insights, including drug-disease-gene relationships.")

# Initialize server
server = Server("mcp-primekg")

# Initialize PrimeKG client with auto-update
primekg_client = PrimeKGClient(
    data_path=DATA_PATH,
    auto_update=AUTO_UPDATE,
    update_interval_days=UPDATE_INTERVAL_DAYS
)


@server.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available PrimeKG resources."""
    return [
        Resource(
            uri="primekg://schema",
            name="PrimeKG Schema",
            description="Schema and structure of the PrimeKG knowledge graph",
            mimeType="text/plain",
        ),
        Resource(
            uri="primekg://statistics",
            name="PrimeKG Statistics",
            description="Statistics about nodes and relationships in PrimeKG",
            mimeType="text/plain",
        ),
        Resource(
            uri="primekg://node_types",
            name="PrimeKG Node Types",
            description="Available node types and their counts in PrimeKG",
            mimeType="application/json",
        ),
        Resource(
            uri="primekg://relationship_types",
            name="PrimeKG Relationship Types",
            description="Available relationship types and their counts in PrimeKG",
            mimeType="application/json",
        ),
    ]


@server.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read a PrimeKG resource."""
    if uri == "primekg://schema":
        return primekg_client.get_schema()
    elif uri == "primekg://statistics":
        return primekg_client.get_statistics()
    elif uri == "primekg://node_types":
        return primekg_client.get_node_types_json()
    elif uri == "primekg://relationship_types":
        return primekg_client.get_relationship_types_json()
    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available PrimeKG query tools."""
    return [
        # Existing tools
        Tool(
            name="search_nodes",
            description="Search for nodes in PrimeKG by name or ID. Returns nodes with their type and properties.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (gene name, drug name, disease name, etc.)",
                    },
                    "node_type": {
                        "type": "string",
                        "description": "Filter by node type (e.g., 'gene/protein', 'drug', 'disease', 'biological_process')",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_node_relationships",
            description="Get all relationships for a specific node in PrimeKG",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "Node ID or name",
                    },
                    "relationship_type": {
                        "type": "string",
                        "description": "Filter by relationship type (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of relationships to return",
                        "default": 50,
                    },
                },
                "required": ["node_id"],
            },
        ),
        Tool(
            name="find_drug_targets",
            description="Find gene/protein targets for a given drug",
            inputSchema={
                "type": "object",
                "properties": {
                    "drug_name": {
                        "type": "string",
                        "description": "Name of the drug",
                    },
                },
                "required": ["drug_name"],
            },
        ),
        Tool(
            name="find_disease_genes",
            description="Find genes associated with a disease",
            inputSchema={
                "type": "object",
                "properties": {
                    "disease_name": {
                        "type": "string",
                        "description": "Name of the disease",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of genes to return",
                        "default": 50,
                    },
                },
                "required": ["disease_name"],
            },
        ),
        Tool(
            name="find_drug_disease_paths",
            description="Find potential drug-disease connections through genes/proteins",
            inputSchema={
                "type": "object",
                "properties": {
                    "drug_name": {
                        "type": "string",
                        "description": "Name of the drug",
                    },
                    "disease_name": {
                        "type": "string",
                        "description": "Name of the disease",
                    },
                    "max_path_length": {
                        "type": "integer",
                        "description": "Maximum length of connection path",
                        "default": 3,
                    },
                },
                "required": ["drug_name", "disease_name"],
            },
        ),
        Tool(
            name="get_node_details",
            description="Get detailed information about a specific node",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_id": {
                        "type": "string",
                        "description": "Node ID or name",
                    },
                },
                "required": ["node_id"],
            },
        ),
        
        # New GeneLab integration tools - Multi-node type support
        Tool(
            name="find_common_nodes",
            description="Find common nodes between PrimeKG and GeneLab across ALL node types (genes, diseases, anatomy, pathways, drugs, GO terms). This enables comprehensive cross-graph queries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "node_identifiers": {
                        "type": "object",
                        "description": "Dictionary mapping node types to lists of identifiers. Supported types: genes, diseases, anatomies, pathways, drugs, biological_processes, molecular_functions, cellular_components",
                        "properties": {
                            "genes": {"type": "array", "items": {"type": "string"}},
                            "diseases": {"type": "array", "items": {"type": "string"}},
                            "anatomies": {"type": "array", "items": {"type": "string"}},
                            "pathways": {"type": "array", "items": {"type": "string"}},
                            "drugs": {"type": "array", "items": {"type": "string"}},
                            "biological_processes": {"type": "array", "items": {"type": "string"}},
                            "molecular_functions": {"type": "array", "items": {"type": "string"}},
                            "cellular_components": {"type": "array", "items": {"type": "string"}},
                        }
                    },
                },
                "required": ["node_identifiers"],
            },
        ),
        Tool(
            name="find_genes_in_both_graphs",
            description="Find common genes between PrimeKG and GeneLab knowledge graphs. This enables cross-graph queries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names to check in both graphs",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of genes to check",
                        "default": 50,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="enrich_genelab_genes_with_primekg",
            description="Enrich GeneLab differentially expressed genes with PrimeKG data (pathways, diseases, drugs)",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names from GeneLab to enrich",
                    },
                    "include_drugs": {
                        "type": "boolean",
                        "description": "Include drug associations",
                        "default": True,
                    },
                    "include_diseases": {
                        "type": "boolean",
                        "description": "Include disease associations",
                        "default": True,
                    },
                    "include_pathways": {
                        "type": "boolean",
                        "description": "Include pathway associations",
                        "default": True,
                    },
                    "include_anatomy": {
                        "type": "boolean",
                        "description": "Include anatomical expression data",
                        "default": True,
                    },
                    "include_go_terms": {
                        "type": "boolean",
                        "description": "Include GO term annotations",
                        "default": True,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="enrich_genelab_entities_with_primekg",
            description="Enrich ANY GeneLab entities (genes, diseases, anatomies, pathways, etc.) with PrimeKG cross-references and relationships",
            inputSchema={
                "type": "object",
                "properties": {
                    "entities": {
                        "type": "object",
                        "description": "Dictionary of entity types to identifiers",
                        "properties": {
                            "genes": {"type": "array", "items": {"type": "string"}},
                            "diseases": {"type": "array", "items": {"type": "string"}},
                            "anatomies": {"type": "array", "items": {"type": "string"}},
                            "pathways": {"type": "array", "items": {"type": "string"}},
                            "drugs": {"type": "array", "items": {"type": "string"}},
                            "go_terms": {"type": "array", "items": {"type": "string"}},
                        }
                    },
                    "relationship_depth": {
                        "type": "integer",
                        "description": "How many relationship hops to explore (1-3)",
                        "default": 1,
                    },
                },
                "required": ["entities"],
            },
        ),
        Tool(
            name="find_drug_targets_for_gene_list",
            description="Find drugs that target any genes in a gene list (useful for GeneLab results)",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names to find drug targets for",
                    },
                    "limit_per_gene": {
                        "type": "integer",
                        "description": "Maximum drugs per gene",
                        "default": 10,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="find_shared_pathways",
            description="Find biological pathways shared among multiple genes",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "min_genes": {
                        "type": "integer",
                        "description": "Minimum number of genes that must share a pathway",
                        "default": 2,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="find_disease_associations",
            description="Find diseases associated with a list of genes and rank by number of gene associations",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "min_genes": {
                        "type": "integer",
                        "description": "Minimum number of genes associated with disease",
                        "default": 1,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        
        # Visualization tools
        Tool(
            name="create_gene_network_plot",
            description="Create a network visualization showing genes and their connections (protein-protein, pathways, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names to visualize",
                    },
                    "include_relationships": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Relationship types to include (e.g., ['protein_protein', 'pathway_protein'])",
                        "default": ["protein_protein"],
                    },
                    "max_neighbors": {
                        "type": "integer",
                        "description": "Maximum neighbors per gene to include",
                        "default": 10,
                    },
                    "figsize_width": {
                        "type": "integer",
                        "description": "Figure width in inches",
                        "default": 12,
                    },
                    "figsize_height": {
                        "type": "integer",
                        "description": "Figure height in inches",
                        "default": 10,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="create_drug_target_heatmap",
            description="Create a heatmap showing which drugs target which genes",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "drug_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional list of specific drugs to include",
                    },
                    "figsize_width": {
                        "type": "integer",
                        "description": "Figure width in inches",
                        "default": 12,
                    },
                    "figsize_height": {
                        "type": "integer",
                        "description": "Figure height in inches",
                        "default": 8,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="create_pathway_enrichment_plot",
            description="Create a bar plot showing pathway enrichment for a gene list",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "Number of top pathways to show",
                        "default": 20,
                    },
                    "figsize_width": {
                        "type": "integer",
                        "description": "Figure width in inches",
                        "default": 10,
                    },
                    "figsize_height": {
                        "type": "integer",
                        "description": "Figure height in inches",
                        "default": 8,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="create_disease_gene_network",
            description="Create a bipartite network showing diseases and associated genes",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "figsize_width": {
                        "type": "integer",
                        "description": "Figure width in inches",
                        "default": 14,
                    },
                    "figsize_height": {
                        "type": "integer",
                        "description": "Figure height in inches",
                        "default": 10,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        
        # Analysis tools
        Tool(
            name="compare_gene_sets",
            description="Compare two gene sets and find their overlaps, unique genes, and shared characteristics",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_set_1": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "First gene set",
                    },
                    "gene_set_2": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Second gene set",
                    },
                    "gene_set_1_name": {
                        "type": "string",
                        "description": "Name for first gene set",
                        "default": "Set 1",
                    },
                    "gene_set_2_name": {
                        "type": "string",
                        "description": "Name for second gene set",
                        "default": "Set 2",
                    },
                },
                "required": ["gene_set_1", "gene_set_2"],
            },
        ),
        Tool(
            name="find_gene_ontology_enrichment",
            description="Find enriched GO terms (biological processes, molecular functions, cellular components) for a gene list",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "ontology_type": {
                        "type": "string",
                        "description": "GO ontology type: 'biological_process', 'molecular_function', 'cellular_component', or 'all'",
                        "default": "all",
                    },
                    "min_genes": {
                        "type": "integer",
                        "description": "Minimum genes per term",
                        "default": 2,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="find_protein_protein_interactions",
            description="Find protein-protein interactions among genes in a list",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "include_indirect": {
                        "type": "boolean",
                        "description": "Include indirect interactions (through intermediate proteins)",
                        "default": False,
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="find_anatomical_expression",
            description="Find anatomical locations where genes are expressed or absent",
            inputSchema={
                "type": "object",
                "properties": {
                    "gene_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of gene names",
                    },
                    "presence_type": {
                        "type": "string",
                        "description": "'present', 'absent', or 'both'",
                        "default": "present",
                    },
                },
                "required": ["gene_names"],
            },
        ),
        Tool(
            name="find_genes_in_anatomy",
            description="Find genes expressed in specific anatomical locations (tissues, organs, cell types)",
            inputSchema={
                "type": "object",
                "properties": {
                    "anatomy_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of anatomical location names or UBERON IDs",
                    },
                    "expression_type": {
                        "type": "string",
                        "description": "'present' (expressed) or 'absent' (not expressed)",
                        "default": "present",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum genes per anatomy",
                        "default": 100,
                    },
                },
                "required": ["anatomy_names"],
            },
        ),
        Tool(
            name="find_disease_associated_pathways",
            description="Find pathways associated with specific diseases through gene connections",
            inputSchema={
                "type": "object",
                "properties": {
                    "disease_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of disease names or MONDO IDs",
                    },
                    "min_genes": {
                        "type": "integer",
                        "description": "Minimum genes connecting disease to pathway",
                        "default": 2,
                    },
                },
                "required": ["disease_names"],
            },
        ),
        Tool(
            name="find_drugs_for_pathway",
            description="Find drugs that target genes in specific pathways",
            inputSchema={
                "type": "object",
                "properties": {
                    "pathway_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of pathway names or Reactome IDs",
                    },
                    "limit_per_pathway": {
                        "type": "integer",
                        "description": "Maximum drugs per pathway",
                        "default": 20,
                    },
                },
                "required": ["pathway_names"],
            },
        ),
        Tool(
            name="compare_anatomical_expression",
            description="Compare gene expression across different anatomical locations",
            inputSchema={
                "type": "object",
                "properties": {
                    "anatomy_1": {
                        "type": "string",
                        "description": "First anatomical location",
                    },
                    "anatomy_2": {
                        "type": "string",
                        "description": "Second anatomical location",
                    },
                    "anatomy_3": {
                        "type": "string",
                        "description": "Optional third anatomical location",
                    },
                },
                "required": ["anatomy_1", "anatomy_2"],
            },
        ),
        Tool(
            name="find_common_pathways_across_diseases",
            description="Find pathways shared across multiple diseases (useful for understanding disease mechanisms)",
            inputSchema={
                "type": "object",
                "properties": {
                    "disease_names": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of disease names or MONDO IDs",
                    },
                    "min_diseases": {
                        "type": "integer",
                        "description": "Minimum diseases that must share a pathway",
                        "default": 2,
                    },
                },
                "required": ["disease_names"],
            },
        ),
        Tool(
            name="find_drug_disease_mechanisms",
            description="Find mechanistic connections between drugs and diseases through genes, pathways, and anatomy",
            inputSchema={
                "type": "object",
                "properties": {
                    "drug_name": {
                        "type": "string",
                        "description": "Drug name or DrugBank ID",
                    },
                    "disease_name": {
                        "type": "string",
                        "description": "Disease name or MONDO ID",
                    },
                    "include_anatomy": {
                        "type": "boolean",
                        "description": "Include anatomical context",
                        "default": True,
                    },
                    "include_pathways": {
                        "type": "boolean",
                        "description": "Include pathway mechanisms",
                        "default": True,
                    },
                },
                "required": ["drug_name", "disease_name"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent | ImageContent]:
    """Handle tool calls for PrimeKG queries."""
    try:
        # Existing tools
        if name == "search_nodes":
            result = primekg_client.search_nodes(
                query=arguments["query"],
                node_type=arguments.get("node_type"),
                limit=arguments.get("limit", 10),
            )
        elif name == "get_node_relationships":
            result = primekg_client.get_node_relationships(
                node_id=arguments["node_id"],
                relationship_type=arguments.get("relationship_type"),
                limit=arguments.get("limit", 50),
            )
        elif name == "find_drug_targets":
            result = primekg_client.find_drug_targets(
                drug_name=arguments["drug_name"]
            )
        elif name == "find_disease_genes":
            result = primekg_client.find_disease_genes(
                disease_name=arguments["disease_name"],
                limit=arguments.get("limit", 50),
            )
        elif name == "find_drug_disease_paths":
            result = primekg_client.find_drug_disease_paths(
                drug_name=arguments["drug_name"],
                disease_name=arguments["disease_name"],
                max_path_length=arguments.get("max_path_length", 3),
            )
        elif name == "get_node_details":
            result = primekg_client.get_node_details(
                node_id=arguments["node_id"]
            )
        
        # New GeneLab integration tools
        elif name == "find_common_nodes":
            result = primekg_client.find_common_nodes(
                node_identifiers=arguments["node_identifiers"],
            )
        elif name == "find_genes_in_both_graphs":
            result = primekg_client.find_genes_in_both_graphs(
                gene_names=arguments["gene_names"],
                limit=arguments.get("limit", 50),
            )
        elif name == "enrich_genelab_genes_with_primekg":
            result = primekg_client.enrich_genelab_genes_with_primekg(
                gene_names=arguments["gene_names"],
                include_drugs=arguments.get("include_drugs", True),
                include_diseases=arguments.get("include_diseases", True),
                include_pathways=arguments.get("include_pathways", True),
                include_anatomy=arguments.get("include_anatomy", True),
                include_go_terms=arguments.get("include_go_terms", True),
            )
        elif name == "enrich_genelab_entities_with_primekg":
            result = primekg_client.enrich_genelab_entities_with_primekg(
                entities=arguments["entities"],
                relationship_depth=arguments.get("relationship_depth", 1),
            )
        elif name == "find_drug_targets_for_gene_list":
            result = primekg_client.find_drug_targets_for_gene_list(
                gene_names=arguments["gene_names"],
                limit_per_gene=arguments.get("limit_per_gene", 10),
            )
        elif name == "find_shared_pathways":
            result = primekg_client.find_shared_pathways(
                gene_names=arguments["gene_names"],
                min_genes=arguments.get("min_genes", 2),
            )
        elif name == "find_disease_associations":
            result = primekg_client.find_disease_associations(
                gene_names=arguments["gene_names"],
                min_genes=arguments.get("min_genes", 1),
            )
        
        # Visualization tools
        elif name == "create_gene_network_plot":
            result = primekg_client.create_gene_network_plot(
                gene_names=arguments["gene_names"],
                include_relationships=arguments.get("include_relationships", ["protein_protein"]),
                max_neighbors=arguments.get("max_neighbors", 10),
                figsize=(arguments.get("figsize_width", 12), arguments.get("figsize_height", 10)),
            )
            # Return image content if visualization created
            if isinstance(result, dict) and "image_path" in result:
                with open(result["image_path"], "rb") as f:
                    image_data = f.read()
                return [
                    ImageContent(type="image", data=image_data, mimeType="image/png"),
                    TextContent(type="text", text=result.get("summary", "Network plot created"))
                ]
        elif name == "create_drug_target_heatmap":
            result = primekg_client.create_drug_target_heatmap(
                gene_names=arguments["gene_names"],
                drug_names=arguments.get("drug_names"),
                figsize=(arguments.get("figsize_width", 12), arguments.get("figsize_height", 8)),
            )
            if isinstance(result, dict) and "image_path" in result:
                with open(result["image_path"], "rb") as f:
                    image_data = f.read()
                return [
                    ImageContent(type="image", data=image_data, mimeType="image/png"),
                    TextContent(type="text", text=result.get("summary", "Heatmap created"))
                ]
        elif name == "create_pathway_enrichment_plot":
            result = primekg_client.create_pathway_enrichment_plot(
                gene_names=arguments["gene_names"],
                top_n=arguments.get("top_n", 20),
                figsize=(arguments.get("figsize_width", 10), arguments.get("figsize_height", 8)),
            )
            if isinstance(result, dict) and "image_path" in result:
                with open(result["image_path"], "rb") as f:
                    image_data = f.read()
                return [
                    ImageContent(type="image", data=image_data, mimeType="image/png"),
                    TextContent(type="text", text=result.get("summary", "Pathway enrichment plot created"))
                ]
        elif name == "create_disease_gene_network":
            result = primekg_client.create_disease_gene_network(
                gene_names=arguments["gene_names"],
                figsize=(arguments.get("figsize_width", 14), arguments.get("figsize_height", 10)),
            )
            if isinstance(result, dict) and "image_path" in result:
                with open(result["image_path"], "rb") as f:
                    image_data = f.read()
                return [
                    ImageContent(type="image", data=image_data, mimeType="image/png"),
                    TextContent(type="text", text=result.get("summary", "Disease-gene network created"))
                ]
        
        # Analysis tools
        elif name == "compare_gene_sets":
            result = primekg_client.compare_gene_sets(
                gene_set_1=arguments["gene_set_1"],
                gene_set_2=arguments["gene_set_2"],
                gene_set_1_name=arguments.get("gene_set_1_name", "Set 1"),
                gene_set_2_name=arguments.get("gene_set_2_name", "Set 2"),
            )
        elif name == "find_gene_ontology_enrichment":
            result = primekg_client.find_gene_ontology_enrichment(
                gene_names=arguments["gene_names"],
                ontology_type=arguments.get("ontology_type", "all"),
                min_genes=arguments.get("min_genes", 2),
            )
        elif name == "find_protein_protein_interactions":
            result = primekg_client.find_protein_protein_interactions(
                gene_names=arguments["gene_names"],
                include_indirect=arguments.get("include_indirect", False),
            )
        elif name == "find_anatomical_expression":
            result = primekg_client.find_anatomical_expression(
                gene_names=arguments["gene_names"],
                presence_type=arguments.get("presence_type", "present"),
            )
        elif name == "find_genes_in_anatomy":
            result = primekg_client.find_genes_in_anatomy(
                anatomy_names=arguments["anatomy_names"],
                expression_type=arguments.get("expression_type", "present"),
                limit=arguments.get("limit", 100),
            )
        elif name == "find_disease_associated_pathways":
            result = primekg_client.find_disease_associated_pathways(
                disease_names=arguments["disease_names"],
                min_genes=arguments.get("min_genes", 2),
            )
        elif name == "find_drugs_for_pathway":
            result = primekg_client.find_drugs_for_pathway(
                pathway_names=arguments["pathway_names"],
                limit_per_pathway=arguments.get("limit_per_pathway", 20),
            )
        elif name == "compare_anatomical_expression":
            result = primekg_client.compare_anatomical_expression(
                anatomy_1=arguments["anatomy_1"],
                anatomy_2=arguments["anatomy_2"],
                anatomy_3=arguments.get("anatomy_3"),
            )
        elif name == "find_common_pathways_across_diseases":
            result = primekg_client.find_common_pathways_across_diseases(
                disease_names=arguments["disease_names"],
                min_diseases=arguments.get("min_diseases", 2),
            )
        elif name == "find_drug_disease_mechanisms":
            result = primekg_client.find_drug_disease_mechanisms(
                drug_name=arguments["drug_name"],
                disease_name=arguments["disease_name"],
                include_anatomy=arguments.get("include_anatomy", True),
                include_pathways=arguments.get("include_pathways", True),
            )
        else:
            raise ValueError(f"Unknown tool: {name}")

        # Return text content for non-visualization results
        if isinstance(result, (list, dict, str)):
            return [TextContent(type="text", text=str(result))]
        else:
            return [TextContent(type="text", text=json.dumps(result, indent=2))]

    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mcp-primekg",
                server_version="0.2.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
