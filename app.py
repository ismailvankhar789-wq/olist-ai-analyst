from pathlib import Path
import re

import pandas as pd
import pyodbc
from sqlalchemy import create_engine
import streamlit as st
from dotenv import load_dotenv
from google import genai


# 1. Load the API key from the local .env file
load_dotenv(Path(__file__).resolve().parent / ".env")


# 2. Create the Gemini client once
@st.cache_resource
def get_client():
    return genai.Client()


# 3. Configure the Streamlit page
st.set_page_config(
    page_title="Olist AI Analyst",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Olist AI Analyst")
st.subheader("AI-assisted Text-to-SQL")
st.write(
    "Ask a business question about Olist to generate SQL, "
    "view results, explore a chart, and discover insights."
)


# 4. Load the database schema
project_folder = Path(__file__).resolve().parent
schema_path = project_folder / "gold_schema.txt"

if not schema_path.exists():
    st.error("gold_schema.txt was not found in the project folder.")
    st.stop()

schema = schema_path.read_text(encoding="utf-8")


# 5. Connect to your local SQL Server
@st.cache_resource
def get_db_connection():
    connection_string = (
        "mssql+pyodbc://@ISMAIL\\SQLEXPRESS/olistDB"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&trusted_connection=yes"
        "&TrustServerCertificate=yes"
    )

    return create_engine(connection_string)

# 6. Basic checks before executing generated SQL
def validate_sql(sql):
    # Remove optional Markdown fences
    sql = sql.strip()
    sql = re.sub(r"^```(?:sql)?\s*", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\s*```$", "", sql)

    # Allow one trailing semicolon, but not multiple statements
    sql = sql.rstrip().removesuffix(";").strip()

    if not re.match(r"^(SELECT|WITH)\b", sql, flags=re.IGNORECASE):
        raise ValueError("Only SELECT queries and read-only CTE queries are allowed.")

    # Reject multiple statements and common write/administrative commands
    if ";" in sql:
        raise ValueError("Only one SQL statement is allowed.")

    blocked = re.compile(
        r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|CREATE|TRUNCATE|"
        r"EXEC|EXECUTE|GRANT|REVOKE|DENY|BACKUP|RESTORE|"
        r"INTO|OPENROWSET|OPENDATASOURCE|DBCC|SHUTDOWN)\b",
        flags=re.IGNORECASE,
    )

    if blocked.search(sql):
        raise ValueError("The query contains a prohibited SQL command.")

    return sql


# 7. Ask Gemini to generate SQL
question = st.text_area(
    "Your business question",
    placeholder="e.g. Which product categories generate the highest revenue?",
)

if st.button("Generate SQL and analyse", type="primary"):
    if not question.strip():
        st.warning("Please enter a business question.")

    else:
        prompt = f"""
You are a SQL Server analytics assistant.

Use only these tables and columns:
{schema}

Business question:
{question}

Generate one read-only SQL Server SELECT query.
A WITH clause is permitted only for a read-only CTE.
Use the GOLD views where appropriate.
Do not use INSERT, UPDATE, DELETE, DDL, stored procedures,
temporary tables, or multiple statements.
Return only SQL, without Markdown fences.
"""

        try:
            with st.spinner("Generating SQL..."):
                response = get_client().models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )

            sql = (response.text or "").strip()

            if not sql:
                st.warning("The model returned an empty response.")
                st.stop()

            sql = validate_sql(sql)

            st.subheader("Generated SQL")
            st.code(sql, language="sql")
            st.caption(
                "Review the SQL. This demo executes the query against "
                "your configured local database."
            )

            # 8. Execute the query and fetch results
            with st.spinner("Running query against SQL Server..."):
                with get_db_connection().connect() as connection:
                    results = pd.read_sql_query(sql, connection)

            if results.empty:
                st.info("The query ran successfully but returned no rows.")
                st.stop()

            st.subheader("Query Results")
            st.dataframe(results, use_container_width=True)

            # 9. Choose a simple chart automatically
            st.subheader("Visualisation")

            numeric_columns = results.select_dtypes(
                include="number"
            ).columns.tolist()

            categorical_columns = [
                column
                for column in results.columns
                if column not in numeric_columns
            ]

            if numeric_columns and len(results.columns) >= 2:
                x_column = results.columns[0]
                y_column = next(
                    (column for column in numeric_columns
                     if column != x_column),
                    None,
                )

                if y_column is None and numeric_columns:
                    y_column = numeric_columns[0]

                if y_column and x_column != y_column:
                    chart_data = results[[x_column, y_column]].copy()
                    chart_data = chart_data.set_index(x_column)

                    if len(results) > 1:
                        st.line_chart(chart_data)
                    else:
                        st.bar_chart(chart_data)
                else:
                    st.info(
                        "A chart could not be selected automatically "
                        "for these columns."
                    )
            else:
                st.info(
                    "These results are best viewed as a table; "
                    "there is no suitable numeric column for a chart."
                )

            # 10. Ask Gemini to explain the actual returned results
            st.subheader("Business Insights")

            sample = results.head(20).to_string(index=False)

            insight_prompt = f"""
You are a business analyst explaining Olist data.

Original question:
{question}

SQL query used:
{sql}

Actual query results (up to 20 rows):
{sample}

Explain the main findings using only the supplied results.
Do not invent figures, causes, trends, or business facts.
If the results are insufficient to answer the question fully,
say so. Mention notable values and practical implications.
Keep the answer concise and distinguish observations from assumptions.
"""

            with st.spinner("Interpreting the results..."):
                insight_response = get_client().models.generate_content(
                    model="gemini-3.6-flash",
                    contents=insight_prompt,
                )

            insights = (insight_response.text or "").strip()

            if insights:
                st.markdown(insights)
            else:
                st.info("No written insights were returned.")

        except ValueError as error:
            st.error(f"Query rejected: {error}")

        except Exception as error:
            st.error(
                "The analysis failed. Check the SQL Server connection, "
                "API key, model availability, and generated query."
            )
            st.caption(f"Technical details: {error}")