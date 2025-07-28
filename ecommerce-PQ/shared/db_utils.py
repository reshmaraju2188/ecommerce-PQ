import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secrets():
    kv_url = os.getenv("KEYVAULT_URI", "https://ecommercekeyv.vault.azure.net/")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=kv_url, credential=credential)
    return {
        "sql_user": client.get_secret("sqlusr").value,
        "sql_pass": client.get_secret("sqlpasswrd").value,
        "openai_key": client.get_secret("openai-key").value,
        "openai_endpoint": client.get_secret("openai-endpoint").value,
    }

def get_sql_conn_string(secrets):
    sql_server = os.getenv("SQL_SRV", "eautos.database.windows.net")
    sql_database = os.getenv("SQL_DB", "ecommerceDB")
    return f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={sql_server};DATABASE={sql_database};UID={secrets['sql_user']};PWD={secrets['sql_pass']};Encrypt=yes;TrustServerCertificate=no"
