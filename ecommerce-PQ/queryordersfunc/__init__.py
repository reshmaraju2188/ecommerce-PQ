import logging
import azure.functions as func
from shared.db_utils import get_secrets, get_sql_conn_string
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import AzureChatOpenAI

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing order query via LangChain...")
    try:
        user_query = req.params.get("query")
        if not user_query:
            return func.HttpResponse("Please provide ?query=Your question", status_code=400)

        secrets = get_secrets()
        conn_str = get_sql_conn_string(secrets)

        db = SQLDatabase.from_uri(f"mssql+pyodbc:///?odbc_connect={conn_str}")
        llm = AzureChatOpenAI(
            deployment_name="gpt-35-turbo",
            openai_api_key=secrets["openai_key"],
            azure_endpoint=secrets["openai_endpoint"],
            api_version="2024-05-01-preview",
            temperature=0
        )

        db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=True)
        raw_result = db_chain.run(user_query)

        summary_prompt = f"""
        Convert the following database query result into a simple, conversational sentence.

        User question: "{user_query}"
        SQL result: {raw_result}

        Respond concisely.
        """
        natural_response = llm.predict(summary_prompt)

        return func.HttpResponse(natural_response.strip(), status_code=200)

    except Exception as e:
        logging.error(f"Query failed: {str(e)}")
        return func.HttpResponse(f"Query failed: {str(e)}", status_code=500)
