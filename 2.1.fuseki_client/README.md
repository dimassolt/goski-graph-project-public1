# Fuseki Client API - README

This document provides an overview of the Fuseki Client API, a FastAPI application designed to interact with a Fuseki SPARQL endpoint.

## Folder Structure

- **`/app/files/sparql_queries/`**: Contains SPARQL query files used by the application.
- **`/app/files/output/`**: Uploade RDF file from mapping process.
- **`/app/files/outputs/`**: Stores the output files, including query results and uploaded RDF files.

## How to Use

1. Ensure the Fuseki server is running and accessible at the configured endpoint.
2. Place your SPARQL query files in the `sparql_queries/` folder.
3. Use the provided API endpoints to execute queries or upload RDF files.

## Prerequisites

- Python 3.x installed on your system.
- Required Python libraries (see `requirements.txt`):
    - `fastapi`
    - `uvicorn`
    - `SPARQLWrapper`
    - `requests`
    - `rdflib`
- A running Fuseki server.

## Running the Application

1. Build and run the application in a Docker container:
        ```bash
        docker build -t fuseki-client .
        docker run -p 8000:8000 fuseki-client
        ```
2. Access the API endpoints:
        - Test SPARQL query: `GET /api/test-sparql`
        - Execute a named query: `GET /api/query/{query_name}`

## API Endpoints

### `/api/test-sparql`
- Executes a predefined SPARQL query to retrieve supplier information.
- Saves the results to `output/test_sparql_result.json`.

### `/api/query/{query_name}`
- Executes a named SPARQL query from the `sparql_queries/` folder.
- Accepts an optional `limit` parameter to restrict the number of results.
- Saves the results to `output/{query_name}.json`.

## Configuration

- **Fuseki Endpoint**: Update the `FUSEKI_ENDPOINT` and `FUSEKI_HEALTH` variables in the script if the Fuseki server URL changes.
- **RDF File Path**: Modify the default RDF file path in the `upload_rdf_file` function if needed.

## Error Handling

- Ensure the Fuseki server is running and accessible.
- Verify that the SPARQL query files exist and are correctly formatted.
- Check the logs for any errors during query execution or RDF upload.

## Contribution

To contribute:
1. Fork the repository.
2. Add or modify features in the FastAPI application.
3. Submit a pull request with a detailed description of your changes.

## Contact

For questions or support, please contact the project maintainer.