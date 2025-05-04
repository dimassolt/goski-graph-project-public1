# GoSki Knowledge Graph Project (Public Version)

🚀 **GoSki Knowledge Graph Dashboard**  
A data-driven project for managing and visualizing cross-country skiing appointments, clients, and revenue using Semantic Web technologies.

---

## ⚙️ Streamlit Public with Auth

**username**: demo
**password**: abc123

---

## 📚 About the Project

This project builds a **knowledge graph** from GoSki appointment data,
serves it using an **Apache Jena Fuseki** server,  
and visualizes insights using a **secure Streamlit dashboard**.

P.s data is facked, but trends are kept which allows to build a relevant hypotesis and conduct analysis. 

---

## ✨ Features

- 🔗 **ETL Mapping**: Converts structured CSV appointment data into RDF triples using RML.
- 🛢 **Knowledge Graph**: Hosted via **Apache Jena Fuseki** for SPARQL querying.
- 📊 **Interactive Dashboard**: Visualizes daily activities, revenue, client stats, and lesson patterns.
- 🔐 **Authentication**: Password-protected dashboard using hashed passwords with `streamlit-authenticator`.
- 🐳 **Dockerized**: Fully containerized setup for easy deployment.
- ☁️ **Cloud-ready**: Optimized for hosting on Streamlit Community Cloud and similar platforms.

---

## 🛠 Technology Stack

- **Python** (Pandas, Streamlit, Requests, Plotly)
- **Apache Jena Fuseki** (SPARQL endpoint)
- **Docker** (multi-container setup)
- **RDF / SPARQL** (Semantic Web standards)
- **Streamlit Authenticator** (for secure login)

---

## 📂 Project Structure

GOSKI-GRAPH-PROJECT-PUBLIC/
- 1.1.mapping/ — ETL scripts to map CSV to RDF
- 2.1.fuseki_client/ — Fuseki SPARQL client API
- 2.2.dashboard/ — Secure Streamlit dashboard
- files/ — Datasources, ontologies, SPARQL queries
  - datasources/ — Source CSV files
  - mappings/ — RML and Turtle mapping files
  - ontologies/ — OWL/Turtle ontology files
  - sparql_queries/ — SPARQL query files
  - outputs/ — Query outputs (JSON)
- compose.yaml — Docker Compose setup
- README.md — Project documentation

---

## ⚙️ Run Using Docker

1. **Clone the repo**:

'''
bash
git clone https://github.com/dimassolt/goski-graph-project-public1.git
cd goski-graph-project-public1
'''

2. **Build and run Docker containers**:

'''
bash
docker compose up --build
'''

3. **Access the Dashboard**:

Local URL: http://localhost:8501

4. **Login credentials**:

Managed securely with hashed passwords (see config.yaml).

---

## 🔒 Security Note
Passwords are hashed using bcrypt.

Streamlit Authenticator manages login sessions and cookies.

Fuseki and backend services are restricted to the internal Docker network for security.

---

## 📈 Example Visualizations
Daily appointment trends

Top-paying clients by revenue

Popular lesson times (weekday & hour)

Revenue over time (area charts & calendar heatmaps)

---

## 🧑‍💻 Author
Dmitrii Soltaganov

---

## 📜 License
Distributed under the MIT License.
See the LICENSE file for details.
