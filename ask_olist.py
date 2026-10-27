from pathlib import Path
from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).resolve().parent / ".env")

client = genai.Client()
# Read the schema exported from SQL Server
schema_path = Path(r"C:\Users\ismai\OneDrive\Documents\python_learning\olist-ai-analyst\gold_schema.txt")
schema = schema_path.read_text(encoding="utf-8")

# Ask a business question
question = input("Ask a question about Olist: ")

prompt = f"""
You are a SQL Server analytics assistant.

Use only the tables and columns listed in this schema:
{schema}

Business question:
{question}

Write one read-only SQL Server SELECT query that answers the question.
Use the GOLD views wherever appropriate.
Return only the SQL query, without Markdown fences.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

print("\nGenerated SQL:\n")
print(response.text)
