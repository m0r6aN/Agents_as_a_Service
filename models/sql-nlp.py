from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from core.actions.sqlite_actions import validate_sql
from db import get_schema

app = FastAPI()

# Load the multitabqa-base-sql model
model_name = "vaishali/multitabqa-base-sql"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

class TextInput(BaseModel):
    text: str

# Model inference function
def small_language_model(text: str) -> str:
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model.generate(**inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Avoid Dynamic Query Construction
# ---------------------------------
# Even though we’re generating SQL queries dynamically, don’t construct them by directly concatenating strings from user input, 
# because this opens the door to injection attacks. Ensure the model-generated SQL uses placeholders for any user-specific values, 
# and always pass those values as separate parameters.
@app.post("/generate_sql/")
def generate_sql(input: TextInput):
    print("SQL NLP API called with input:", input.text)
    schema = get_schema()  
    schema_str = ""

    for table, columns in schema.items():
        schema_str += f"Table: {table}\n" + "\n".join([f"- {col}" for col in columns]) + "\n\n"

    # Combine schema and user query into the prompt
    prompt = schema_str + "Query: " + input.text

    # Step 1: Use the model to generate the SQL query
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        # Step 2: Validate and execute the generated SQL query
        validate_sql(sql_query)
        # results = run_sql(sql_query)  # Your function to run the SQL query on your DB
    except ValueError as e:
        return {"error": str(e)}

    # Step 3: Return the SQL query and results
    return {
        "sql": sql_query,
        #"results": results  # This could be returned as CSV, JSON, etc.
    }
