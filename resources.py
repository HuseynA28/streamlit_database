from sqlalchemy import text
from database import get_engine, TABLE_NAME
import pandas as pd


def build_query(filters: dict) -> tuple[str, dict]:
    """Build a parameterised SQL query from the filter dict."""
    conditions = []
    params = {}

    field_map = {
        "organization_name": "Organization_Name",
        "treasury_account_code": "Treasury_Account_Code",
        "functional_classification_code": "Functional_Classification_Code",
        "supplier_name": "Supplier_Name",
        "supplier_tin": "Supplier_TIN",
        "supplier_bank_account": "Supplier_Bank_Account",
        "product_name": "Product_Name",
        "category": "Category",
        "tin": "TIN",
    }

    for key, col in field_map.items():
        value = filters.get(key, "").strip()
        if value:
            conditions.append(f"LOWER({col}) LIKE :{key}")
            params[key] = f"%{value.lower()}%"

    # Amount range
    amount_min = filters.get("amount_min")
    amount_max = filters.get("amount_max")
    if amount_min is not None and amount_min > 0:
        conditions.append("Amount >= :amount_min")
        params["amount_min"] = amount_min
    if amount_max is not None and amount_max > 0:
        conditions.append("Amount <= :amount_max")
        params["amount_max"] = amount_max

    # Date range
    date_from = filters.get("date_from")
    date_to = filters.get("date_to")
    if date_from:
        conditions.append("Date >= :date_from")
        params["date_from"] = str(date_from)
    if date_to:
        conditions.append("Date <= :date_to")
        params["date_to"] = str(date_to)

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    limit = filters.get("limit_record", 50)
    limit_clause = "" if limit == 0 else f"LIMIT {int(limit)}"

    sql = f"SELECT * FROM {TABLE_NAME} {where_clause} ORDER BY Date DESC {limit_clause}"
    return sql, params


def query_operations(filters: dict) -> pd.DataFrame:
    engine = get_engine()
    sql, params = build_query(filters)
    with engine.connect() as conn:
        result = conn.execute(text(sql), params)
        rows = result.fetchall()
        columns = result.keys()
    df = pd.DataFrame(rows, columns=list(columns))
    if not df.empty and "id" in df.columns:
        df = df.drop(columns=["id"])
    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"total_records": 0, "total_amount": 0, "avg_amount": 0, "unique_orgs": 0}
    return {
        "total_records": len(df),
        "total_amount": df["Amount"].sum() if "Amount" in df.columns else 0,
        "avg_amount": df["Amount"].mean() if "Amount" in df.columns else 0,
        "unique_orgs": df["Organization_Name"].nunique() if "Organization_Name" in df.columns else 0,
    }