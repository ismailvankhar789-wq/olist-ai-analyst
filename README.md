# ⚡ Olist AI Analyst — AI-Powered Text-to-SQL Analytics

An AI-powered analytics application that converts natural-language business questions into SQL queries, executes them against an exported **DuckDB** database, and presents query results and business insights through an interactive Streamlit interface.

Built using Python, Google Gemini API, DuckDB, and Streamlit, with data sourced from the Gold layer of an Olist e-commerce data warehouse.

## Overview

Olist AI Analyst bridges the gap between business questions and data analysis. Users can ask questions in plain English, generate SQL with Google Gemini, inspect the generated query, and explore the results without manually writing SQL.

The application uses Gold-layer schema metadata to guide query generation and DuckDB to execute analytical queries against the exported dataset.

## Key Features

- **Natural-language querying:** Ask business questions without writing SQL manually.
- **AI-powered SQL generation:** Generate DuckDB-compatible SQL using Google Gemini.
- **Read-only query execution:** Execute analytical queries against the exported database.
- **Interactive results:** Display query results in a tabular format.
- **Data visualization:** Explore results through charts.
- **AI-generated insights:** Turn query results into business-oriented findings.
- **Cloud deployment:** Access the Streamlit application through a web browser.

## How It Works

1. **Ask a business question** — Enter a question in natural language.
2. **Provide schema context** — The application supplies the Gold-layer table and column metadata to Gemini.
3. **Generate SQL** — Gemini generates a DuckDB-compatible, read-only SQL query.
4. **Execute the query** — The application runs the query against the exported DuckDB database.
5. **Explore the results** — Review the results and visualize relevant data.
6. **Generate insights** — Use AI to interpret the results and identify business takeaways.

## Tech Stack

- **Python** — Application logic and data processing
- **Google Gemini API** — AI-assisted SQL generation and insight generation
- **Streamlit** — Interactive web application
- **DuckDB** — Analytical database engine
- **Pandas** — Data handling and result processing
- **Microsoft SQL Server** — Original data warehouse and Gold-layer source
- **Git & GitHub** — Version control and project documentation

## Project Structure

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `export_to_duckdb.py` | Exports Gold-layer data from SQL Server to DuckDB |
| `check_duckdb.py` | Checks the exported DuckDB database and its tables |
| `gold_schema.txt` | Gold-layer schema metadata used to guide SQL generation |
| `.env` | Stores local environment variables and API credentials |
| `.gitignore` | Excludes secrets and unnecessary files |

## Setup and Usage

1. Install Python and Git.
2. Clone the repository and open the project directory.
3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your Gemini API key using a local `.env` file or Streamlit Community Cloud Secrets, as appropriate.
5. Ensure the exported `olist.duckdb` database is available in the expected project directory.
6. Start the application:

   ```bash
   python -m streamlit run app.py
   ```

7. Open the local URL displayed in the terminal and start asking business questions.

## Data Architecture

The project uses a layered analytics workflow:

- **Silver layer:** Cleaned and prepared source data in SQL Server.
- **Gold layer:** Analytics-ready views designed for business reporting.
- **DuckDB:** An exported analytical dataset used by the application.
- **Streamlit:** The user-facing interface for querying and exploring data.

This approach separates data preparation from application execution, allowing the deployed app to analyze the exported dataset without requiring a live connection to the local SQL Server instance.

## Security and Limitations

- API keys and credentials should never be committed to GitHub.
- The `.env` file should remain excluded through `.gitignore`.
- Generated SQL is restricted to read-only analytical queries.
- AI-generated SQL and insights should be reviewed for correctness.
- The application analyzes the exported dataset, so results reflect the data available in that export.

## Future Improvements

- Add query caching and performance optimization.
- Improve SQL validation and error handling.
- Expand chart selection and dashboard capabilities.
- Add more business-focused analytical workflows.
- Automate dataset refreshes.

---

**Project focus:** Generative AI · Text-to-SQL · Business Analytics · DuckDB · Streamlit · Python · Data Warehousing · Data Visualization
