# -*- coding: utf-8 -*-
"""
    GoSki Fuseki Client API
    Interacts with a Fuseki SPARQL endpoint to upload RDF and query ski class data.
"""
import json
from fastapi import FastAPI, Query  # type: ignore
from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE  # type: ignore
import os
import time
import requests

app = FastAPI()

FUSEKI_ENDPOINT = "http://fuseki:3030/dataset/sparql"
FUSEKI_HEALTH = "http://fuseki:3030/dataset"

def wait_for_fuseki(timeout=100):
    start = time.time()
    while True:
        try:
            r = requests.get(FUSEKI_HEALTH)
            if r.status_code == 200:
                print("✅ Fuseki is ready!")
                break
        except:
            pass
        if time.time() - start > timeout:
            raise TimeoutError("❌ Timeout waiting for Fuseki")
        print("⏳ Waiting for Fuseki...")
        time.sleep(3)

def upload_rdf_file(file_path="/app/data/goski-kg_merged.ttl"):
    fuseki_data_endpoint = "http://fuseki:3030/dataset/data"

    if not os.path.isfile(file_path):
        print(f"⚠️ RDF file not found: {file_path}")
        return

    with open(file_path, "rb") as f:
        headers = {"Content-Type": "text/turtle"}
        response = requests.post(fuseki_data_endpoint, data=f, headers=headers)

    if response.status_code == 200:
        print(f"✅ RDF file '{file_path}' uploaded to Fuseki.")
    else:
        print(f"❌ RDF upload failed: {response.status_code} {response.text}")

def run_sparql(query: str, query_type: str = "SELECT"):
    sparql = SPARQLWrapper(FUSEKI_ENDPOINT)
    sparql.setQuery(query)

    if query_type.upper() in ["SELECT", "ASK"]:
        sparql.setReturnFormat(JSON)
    elif query_type.upper() in ["CONSTRUCT", "DESCRIBE"]:
        sparql.setReturnFormat(TURTLE)
    else:
        raise ValueError("Unsupported query type")

    return sparql.query().convert()

@app.get("/api/test-sparql")
def test_sparql():
    """
    Execute a test query: List 10 clients with their emails.
    """
    query = """
        PREFIX ski: <http://example.org/ski#>

        SELECT ?person ?firstName ?lastName ?email
        WHERE {
            ?person a ski:Person ;
                    ski:firstName ?firstName ;
                    ski:lastName ?lastName ;
                    ski:email ?email .
        }
        LIMIT 10
    """
    try:
        results = run_sparql(query, "SELECT")
        output_path = "/app/files/outputs/test_sparql_result.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/query/{query_name}")
def run_named_query(query_name: str, limit: int = Query(None)):
    query_path = f"/app/files/sparql_queries/{query_name}.rq"
    output_path = f"/app/files/outputs/{query_name}.json"

    if not os.path.isfile(query_path):
        return {"error": f"Query file not found: {query_path}"}

    try:
        with open(query_path, "r") as f:
            query = f.read()

        if limit:
            query += f"\nLIMIT {limit}"

        results = run_sparql(query, "SELECT")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)

        return {
            "message": f"Query '{query_name}' executed successfully.",
            "limit": limit,
            "saved_to": output_path,
            "results": results
        }
    except Exception as e:
        return {"error": str(e)}

# === On container startup ===
wait_for_fuseki()
upload_rdf_file("/app/files/output/goski-kg_merged.ttl")
