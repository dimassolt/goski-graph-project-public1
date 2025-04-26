# Mapping - README

This document provides an overview of the mapping process within the pipeline, specifically focusing on the implementation using the provided Python script.
## Folder Structure

- **`input/`**: Contains the RML mapping and ontology files required for the mapping process.
- **`scripts/`**: Includes Python scripts for performing the mapping operations.
- **`output/`**: Stores the generated RDF graphs and merged ontology outputs.

## How to Use

1. Place your RML mapping and ontology files in the `input/` folder.
2. Run the mapping script located in the `scripts/` folder.
3. Check the generated RDF graphs and merged outputs in the `output/` folder.

## Prerequisites

- Python 3.x installed on your system.
- Required Python libraries (see `requirements.txt` if available).

## Running the Mapping Process

1. Navigate to this folder in your terminal.
2. Execute the mapping script:
    ```bash
    python scripts/mapping_script.py --input input/mapping_file.rml --ontology input/ontology_file.owl --output output/
    ```
3. Verify the output files in the `output/` folder.

## Notes

- Ensure the RML mapping and ontology files are correctly formatted.
- Modify the script as needed to accommodate specific mapping requirements.

## Overview

The mapping process involves:
- **RML Conversion**: Transforming RML mapping files into RDF graphs.
- **Ontology Integration**: Merging the generated RDF graph with a specified ontology.

## Steps in the Mapping Process

1. **Input Data Collection**  
    Provide the RML mapping file and the ontology file as inputs.

2. **RML Conversion**  
    - Use the `RMLConverter` to convert the RML mapping file into an RDF graph.
    - The conversion can be executed with multiprocessing for faster computation.

3. **Output Generation**  
    - Store the generated RDF graph in Turtle (`.ttl`) and N3 (`.n3`) formats.
    - Merge the RDF graph with the ontology and store the combined output.

## Configuration

The script accepts the following arguments:
- `input`: Path to the RML mapping file.
- `ontology`: Path to the ontology file.
- `-o`, `--output`: Path to the output file (default is standard output).
- `-m`: Enable multiprocessing for faster computation.

## Tools and Dependencies

The mapping process relies on:
- **pyrml**: For RML to RDF conversion.
- **rdflib**: For RDF graph manipulation.
- **Python Libraries**: `argparse`, `logging`, `os`, `pathlib`, `codecs`.

## Error Handling

- Ensure the input files exist and are correctly formatted.
- Check the logs for any errors during the mapping or merging process.

## Contribution

To contribute:
1. Fork the repository.
2. Modify the mapping script or dependencies.
3. Submit a pull request with a detailed description of your changes.

## Contact

For questions or support, please contact the pipeline maintainer.
