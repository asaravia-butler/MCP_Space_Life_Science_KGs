"""
SPARQL Query Templates for SPOKE-OKN Integration

These queries enable geospatial, social determinants of health (SDoH),
and environmental health analysis.

SPOKE-OKN Endpoint: https://frink.renci.org/registry/kgs/spoke-okn/
"""

# Common prefixes for SPOKE-OKN
PREFIXES = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://purl.org/okn/frink/kg/spoke-okn/schema/>
PREFIX biolink: <https://w3id.org/biolink/vocab/>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
"""

# ===========================================================================
# SECTION 1: DISEASE QUERIES
# ===========================================================================

FIND_DISEASE_PREVALENCE_BY_LOCATION = PREFIXES + """
SELECT DISTINCT ?disease_name ?location_name ?prevalence ?year
WHERE {
  ?stmt rdf:subject ?disease ;
        rdf:predicate schema:PREVALENCE_DpL ;
        rdf:object ?location ;
        schema:value ?prevalence ;
        schema:year ?year .
  
  ?disease rdfs:label ?disease_name .
  ?location rdfs:label ?location_name .
  
  FILTER(CONTAINS(LCASE(?disease_name), LCASE(?disease_query)))
  FILTER(CONTAINS(LCASE(?location_name), LCASE(?location_query)))
}
ORDER BY DESC(?year) ?disease_name
LIMIT ?limit
"""

FIND_DISEASE_MORTALITY_BY_LOCATION = PREFIXES + """
SELECT DISTINCT ?disease_name ?location_name ?mortality_rate ?year
WHERE {
  ?stmt rdf:subject ?disease ;
        rdf:predicate schema:MORTALITY_DmL ;
        rdf:object ?location ;
        schema:mortality_per_100k ?mortality_rate ;
        schema:year ?year .
  
  ?disease rdfs:label ?disease_name .
  ?location rdfs:label ?location_name .
  
  FILTER(CONTAINS(LCASE(?location_name), LCASE(?location_query)))
}
ORDER BY DESC(?mortality_rate)
LIMIT ?limit
"""

FIND_DISEASE_GENE_ASSOCIATIONS = PREFIXES + """
SELECT DISTINCT ?disease_name ?gene_name
WHERE {
  ?disease schema:ASSOCIATES_DaG ?gene .
  ?disease rdfs:label ?disease_name .
  ?gene rdfs:label ?gene_name .
  
  FILTER(?disease_name IN (?disease_list))
}
"""

# ===========================================================================
# SECTION 2: CHEMICAL/COMPOUND QUERIES
# ===========================================================================

FIND_CHEMICALS_IN_LOCATION = PREFIXES + """
SELECT DISTINCT ?chemical_name ?location_name ?value ?unit ?year ?media
WHERE {
  ?stmt rdf:subject ?chemical ;
        rdf:predicate schema:FOUNDIN_CfL ;
        rdf:object ?location ;
        schema:value ?value ;
        schema:unit ?unit ;
        schema:year ?year ;
        schema:media ?media .
  
  ?chemical rdfs:label ?chemical_name .
  ?location rdfs:label ?location_name .
  
  FILTER(CONTAINS(LCASE(?location_name), LCASE(?location_query)))
}
ORDER BY DESC(?year) DESC(?value)
LIMIT ?limit
"""

FIND_DRUG_TREATS_DISEASE = PREFIXES + """
SELECT DISTINCT ?drug_name ?disease_name ?phase ?sources
WHERE {
  ?stmt rdf:subject ?drug ;
        rdf:predicate schema:TREATS_CtD ;
        rdf:object ?disease ;
        schema:phase ?phase ;
        schema:act_sources ?sources .
  
  ?drug rdfs:label ?drug_name .
  ?disease rdfs:label ?disease_name .
  
  FILTER(CONTAINS(LCASE(?disease_name), LCASE(?disease_query)))
}
ORDER BY DESC(?phase)
"""

FIND_DRUG_CONTRAINDICATIONS = PREFIXES + """
SELECT DISTINCT ?drug_name ?disease_name ?sources
WHERE {
  ?stmt rdf:subject ?drug ;
        rdf:predicate schema:CONTRAINDICATES_CcD ;
        rdf:object ?disease ;
        schema:act_sources ?sources .
  
  ?drug rdfs:label ?drug_name .
  ?disease rdfs:label ?disease_name .
  
  FILTER(?drug_name IN (?drug_list))
}
"""

FIND_DRUG_DRUG_INTERACTIONS = PREFIXES + """
SELECT DISTINCT ?drug1_name ?drug2_name ?risk_level
WHERE {
  ?stmt rdf:subject ?drug1 ;
        rdf:predicate schema:INTERACTS_CiC ;
        rdf:object ?drug2 ;
        schema:ddi_risk ?risk_level .
  
  ?drug1 rdfs:label ?drug1_name .
  ?drug2 rdfs:label ?drug2_name .
  
  FILTER(?drug1_name IN (?drug_list))
}
"""

# ===========================================================================
# SECTION 3: SOCIAL DETERMINANTS OF HEALTH (SDoH)
# ===========================================================================

FIND_SDOH_BY_LOCATION = PREFIXES + """
SELECT DISTINCT ?sdoh_name ?location_name ?value ?variable ?year
WHERE {
  ?stmt rdf:subject ?sdoh ;
        rdf:predicate schema:PREVALENCEIN_SpL ;
        rdf:object ?location ;
        schema:value ?value ;
        schema:variable ?variable ;
        schema:year ?year .
  
  ?sdoh rdfs:label ?sdoh_name .
  ?location rdfs:label ?location_name .
  
  FILTER(CONTAINS(LCASE(?location_name), LCASE(?location_query)))
}
ORDER BY DESC(?year) ?sdoh_name
LIMIT ?limit
"""

FIND_SDOH_DISEASE_ASSOCIATIONS = PREFIXES + """
SELECT DISTINCT ?sdoh_name ?disease_name ?cooccurrence ?enrichment ?fisher_test
WHERE {
  ?stmt rdf:subject ?sdoh ;
        rdf:predicate schema:ASSOCIATES_SaD ;
        rdf:object ?disease ;
        schema:cooccur ?cooccurrence ;
        schema:enrichment ?enrichment ;
        schema:fisher ?fisher_test .
  
  ?sdoh rdfs:label ?sdoh_name .
  ?disease rdfs:label ?disease_name .
  
  FILTER(?fisher_test < ?p_value_threshold)
}
ORDER BY ?fisher_test
LIMIT ?limit
"""

# ===========================================================================
# SECTION 4: ENVIRONMENTAL FEATURES
# ===========================================================================

FIND_ENVIRONMENTAL_FEATURES_IN_LOCATION = PREFIXES + """
SELECT DISTINCT ?env_feature_name ?location_name ?value ?unit ?year
WHERE {
  ?stmt rdf:subject ?env_feature ;
        rdf:predicate schema:FOUNDIN_EfL ;
        rdf:object ?location ;
        schema:value ?value ;
        schema:unit ?unit ;
        schema:year ?year .
  
  ?env_feature rdfs:label ?env_feature_name .
  ?location rdfs:label ?location_name .
  
  FILTER(CONTAINS(LCASE(?location_name), LCASE(?location_query)))
}
ORDER BY DESC(?year)
LIMIT ?limit
"""

# ===========================================================================
# SECTION 5: ANTIMICROBIAL RESISTANCE
# ===========================================================================

FIND_ORGANISM_ANTIMICROBIAL_RESISTANCE = PREFIXES + """
SELECT DISTINCT ?organism_name ?chemical_name ?resistant_phenotype 
                ?measurement_value ?location_name
WHERE {
  ?stmt rdf:subject ?organism ;
        rdf:predicate schema:RESPONDS_TO_OrC ;
        rdf:object ?chemical ;
        schema:resistant_phenotype ?resistant_phenotype ;
        schema:measurement_value ?measurement_value .
  
  ?organism rdfs:label ?organism_name .
  ?chemical rdfs:label ?chemical_name .
  
  OPTIONAL {
    ?organism schema:ISOLATEDIN_OiL ?location .
    ?location rdfs:label ?location_name .
  }
  
  FILTER(CONTAINS(LCASE(?organism_name), LCASE(?organism_query)))
  FILTER(CONTAINS(LCASE(?chemical_name), LCASE(?antibiotic_query)))
}
"""

# ===========================================================================
# SECTION 6: GENE-COMPOUND INTERACTIONS
# ===========================================================================

FIND_COMPOUND_UPREGULATES_GENE = PREFIXES + """
SELECT DISTINCT ?compound_name ?gene_name
WHERE {
  ?compound schema:UPREGULATES_CuG ?gene .
  ?compound rdfs:label ?compound_name .
  ?gene rdfs:label ?gene_name .
  
  FILTER(?gene_name IN (?gene_list))
}
"""

FIND_COMPOUND_DOWNREGULATES_GENE = PREFIXES + """
SELECT DISTINCT ?compound_name ?gene_name
WHERE {
  ?compound schema:DOWNREGULATES_CdG ?gene .
  ?compound rdfs:label ?compound_name .
  ?gene rdfs:label ?gene_name .
  
  FILTER(?gene_name IN (?gene_list))
}
"""

FIND_GENE_DISEASE_EXPRESSION = PREFIXES + """
SELECT DISTINCT ?gene_name ?disease_name
WHERE {
  ?gene schema:EXPRESSEDIN_GeiD ?disease .
  ?gene rdfs:label ?gene_name .
  ?disease rdfs:label ?disease_name .
  
  FILTER(?gene_name IN (?gene_list))
}
"""

# ===========================================================================
# SECTION 7: GEOGRAPHIC/LOCATION QUERIES
# ===========================================================================

FIND_LOCATIONS_BY_TYPE = PREFIXES + """
SELECT DISTINCT ?location_name ?state_name ?latitude ?longitude
WHERE {
  ?location a schema:AdministrativeArea ;
            rdfs:label ?location_name ;
            schema:state_name ?state_name .
  
  OPTIONAL {
    ?location schema:latitude ?latitude ;
              schema:longitude ?longitude .
  }
  
  FILTER(CONTAINS(LCASE(?state_name), LCASE(?state_query)))
}
LIMIT ?limit
"""

FIND_LOCATION_HIERARCHY = PREFIXES + """
SELECT DISTINCT ?child_location ?parent_location ?percent_area
WHERE {
  ?stmt rdf:subject ?child ;
        rdf:predicate schema:PARTOF_LpL ;
        rdf:object ?parent ;
        schema:percent_of_place_area_in_zip ?percent_area .
  
  ?child rdfs:label ?child_location .
  ?parent rdfs:label ?parent_location .
  
  FILTER(CONTAINS(LCASE(?parent_location), LCASE(?location_query)))
}
"""

# ===========================================================================
# SECTION 8: DISEASE SIMILARITY
# ===========================================================================

FIND_SIMILAR_DISEASES = PREFIXES + """
SELECT DISTINCT ?disease1_name ?disease2_name ?cooccurrence ?enrichment
WHERE {
  ?stmt rdf:subject ?disease1 ;
        rdf:predicate schema:RESEMBLES_DrD ;
        rdf:object ?disease2 ;
        schema:cooccur ?cooccurrence ;
        schema:enrichment ?enrichment .
  
  ?disease1 rdfs:label ?disease1_name .
  ?disease2 rdfs:label ?disease2_name .
  
  FILTER(?disease1_name IN (?disease_list))
  FILTER(?enrichment > ?enrichment_threshold)
}
ORDER BY DESC(?enrichment)
LIMIT ?limit
"""

# ===========================================================================
# QUERY TEMPLATES WITH PARAMETER SUBSTITUTION
# ===========================================================================

QUERY_TEMPLATES = {
    "disease_prevalence": FIND_DISEASE_PREVALENCE_BY_LOCATION,
    "disease_mortality": FIND_DISEASE_MORTALITY_BY_LOCATION,
    "disease_genes": FIND_DISEASE_GENE_ASSOCIATIONS,
    "chemicals_in_location": FIND_CHEMICALS_IN_LOCATION,
    "drug_treats": FIND_DRUG_TREATS_DISEASE,
    "drug_contraindications": FIND_DRUG_CONTRAINDICATIONS,
    "drug_interactions": FIND_DRUG_DRUG_INTERACTIONS,
    "sdoh_by_location": FIND_SDOH_BY_LOCATION,
    "sdoh_disease": FIND_SDOH_DISEASE_ASSOCIATIONS,
    "environmental_features": FIND_ENVIRONMENTAL_FEATURES_IN_LOCATION,
    "amr": FIND_ORGANISM_ANTIMICROBIAL_RESISTANCE,
    "compound_upregulates": FIND_COMPOUND_UPREGULATES_GENE,
    "compound_downregulates": FIND_COMPOUND_DOWNREGULATES_GENE,
    "gene_expression_disease": FIND_GENE_DISEASE_EXPRESSION,
    "locations": FIND_LOCATIONS_BY_TYPE,
    "location_hierarchy": FIND_LOCATION_HIERARCHY,
    "disease_similarity": FIND_SIMILAR_DISEASES,
}


def substitute_parameters(query_template: str, **kwargs) -> str:
    """
    Substitute parameters in SPARQL query template.
    
    Args:
        query_template: SPARQL query with ?parameter placeholders
        **kwargs: Parameter values to substitute
    
    Returns:
        Query with parameters substituted
    """
    query = query_template
    
    for key, value in kwargs.items():
        placeholder = f"?{key}"
        
        if isinstance(value, list):
            # Convert list to SPARQL syntax: ("item1" "item2")
            list_str = "(" + " ".join([f'"{item}"' for item in value]) + ")"
            query = query.replace(placeholder, list_str)
        elif isinstance(value, str):
            query = query.replace(placeholder, f'"{value}"')
        elif isinstance(value, (int, float)):
            query = query.replace(placeholder, str(value))
    
    return query


# ===========================================================================
# EXAMPLE USAGE
# ===========================================================================

EXAMPLE_QUERIES = {
    "disease_prevalence_california": {
        "template": "disease_prevalence",
        "params": {
            "disease_query": "diabetes",
            "location_query": "California",
            "limit": 10
        }
    },
    "chemical_exposures_florida": {
        "template": "chemicals_in_location",
        "params": {
            "location_query": "Florida",
            "limit": 20
        }
    },
    "sdoh_poverty": {
        "template": "sdoh_disease",
        "params": {
            "p_value_threshold": 0.05,
            "limit": 50
        }
    },
    "amr_ecoli": {
        "template": "amr",
        "params": {
            "organism_query": "Escherichia coli",
            "antibiotic_query": "ciprofloxacin"
        }
    }
}
