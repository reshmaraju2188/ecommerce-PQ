import logging
import uuid
import pyodbc
import azure.functions as func
from urllib.parse import parse_qs
from shared.db_utils import get_secrets, get_sql_conn_string

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing new order request...")
    try:
        raw_body = req.get_body().decode()
        form_data = parse_qs(raw_body)

        name = form_data.get("name", [""])[0]
        email = form_data.get("email", [""])[0]
        address = form_data.get("address", [""])[0]
        product = form_data.get("product", [""])[0]
        quantity = form_data.get("quantity", [""])[0]

        if not all([name, email, address, product, quantity]):
            return func.HttpResponse("Missing required fields.", status_code=400)

        secrets = get_secrets()
        conn_str = get_sql_conn_string(secrets)
        tracking_code = "ORD-" + str(uuid.uuid4())[:8]

        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Orders (CustomerName, Email, Address, ProductName, Quantity, PaymentStatus, TrackingCode)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, name, email, address, product, int(quantity), "Paid", tracking_code)
            conn.commit()

        return func.HttpResponse(f"Order placed successfully! Tracking Code: {tracking_code}", status_code=200)

    except Exception as e:
        logging.error(f"Order failed: {str(e)}")
        return func.HttpResponse(f"Order failed: {str(e)}", status_code=500)
