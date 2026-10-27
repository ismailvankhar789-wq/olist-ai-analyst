# Olist AI Analyst — AI-Assisted Text-to-SQL

An AI-powered analytics tool that translates natural-language business questions into SQL queries using **Python, Google Gemini API, and Microsoft SQL Server**. Built on the Gold layer of an Olist e-commerce data warehouse.

## Overview

Olist AI Analyst helps bridge the gap between business questions and SQL analysis. It uses database schema metadata to guide Gemini in generating SQL queries that can be reviewed and executed in SQL Server Management Studio (SSMS).

## How It Works

1. **Ask a question** — Enter a business question in natural language.
2. **Provide schema context** — The tool uses Gold-layer table and column metadata to guide query generation.
3. **Generate SQL** — Gemini generates a SQL query based on the question and available schema.
4. **Analyse the data** — Review and execute the generated query in SSMS to obtain results.

## Tech Stack

- **Python** — Application logic and database connectivity
- **Google Gemini API** — AI-assisted SQL generation
- **Microsoft SQL Server** — Olist data warehouse
- **pyodbc** — Python-to-SQL Server connectivity
- **python-dotenv** — Environment variable management
- **Git & GitHub** — Version control

## Project Structure

| File | Purpose |
|---|---|
| `ask_olist.py` | Generates SQL from business questions using Gemini |
| `test_sql_connection.py` | Tests SQL Server connectivity |
| `inspect_warehouse.py` | Inspects warehouse tables and columns |
| `export_schema.py` | Exports Gold-layer schema metadata |
| `gold_schema.txt` | Schema context used for SQL generation |
| `.gitignore` | Excludes secrets and unnecessary files |

## Setup

1. Install Python and Microsoft SQL Server with access to the Olist database.
2. Install the required Python packages:

   ```bash
   pip install google-genai python-dotenv pyodbc
   ```

3. Create a `.env` file in the project directory:

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

4. Configure the SQL Server connection in the Python script for your environment.
5. Run the application:

   ```bash
   python ask_olist.py
   ```

**Security:** Keep API keys and credentials private. The `.env` file is excluded through `.gitignore`.

## Current Scope

The tool generates SQL for human review and execution in SSMS. Automatic query execution and result interpretation are not currently implemented.

## Future Improvements

- Execute validated SQL queries directly from Python.
- Display query results in a user-friendly interface.
- Add SQL validation and error handling.
- Present analytical findings and business insights automatically.

---

**Project focus:** Natural-language processing · Text-to-SQL · Data analytics · SQL Server · Generative AI
