# Knowledge Graph Dashboard - README

This document provides an overview of the GoSki Knowledge Graph Dashboard, a Streamlit application designed to visualize data from a GoSki Knowledge Graph.

## Folder Structure

- **`/app/files/sparql_queries/`**: Contains SPARQL query files used by the application.
- **`/app/files/output/`**: Stores the output files, including query results.

**Daily Appointments**:
  - Bar chart visualizing the number of appointments per day.
  - Automatically parses and formats dates for accurate representation.
  - Interactive chart with hover details and zoom functionality.

- **Top Clients by Revenue**:
  - Bar chart displaying the top-paying clients.
  - Adjustable slider to customize the number of clients shown.
  - Sorts clients by total revenue in descending order.

- **Popular Time Slots**:
  - Bar chart showing the distribution of appointments across different hours of the day.
  - Filters and sorts data for better time slot analysis.

- **Revenue Over Time**:
  - Area chart and calendar heatmap visualizing daily revenue trends.
  - Toggle between different views for better insights.
  - Filters for specific months and detailed revenue breakdown by course type.

## Prerequisites

- Python 3.10 installed on your system.
- Required Python libraries (see `environment.yml`):
  - `pandas`
  - `requests`
  - `streamlit`
  - `plotly`

## How to Use

1. **Setup Environment**:
    - Create a conda environment using the provided `environment.yml` file:
      ```bash
      conda env create -f environment.yml
      conda activate vw_dashboard_env
      ```

2. **Run the Application**:
    - Start the Streamlit application:
      ```bash
      streamlit run app.py
      ```

3. **Access the Dashboard**:
    - Open the dashboard in your browser at `http://localhost:8501`.

## Configuration

- **API Base URL**: Update the `API_BASE` variable in the script if the Fuseki server URL changes.
- **SPARQL Query Directory**: Ensure SPARQL query files are placed in the `sparql_queries/` folder.

## Error Handling

- Ensure the Fuseki server is running and accessible.
- Verify that the SPARQL query files exist and are correctly formatted.
- Check the Streamlit logs for any errors during query execution.

## Contribution

To contribute:
1. Fork the repository.
2. Add or modify features in the Streamlit application.
3. Submit a pull request with a detailed description of your changes.

## Contact

For questions or support, please contact the project maintainer.  