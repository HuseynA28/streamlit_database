import os
import random
from datetime import datetime, timedelta
from sqlalchemy import (
    create_engine, Column, String, Float, Date, Integer, MetaData, Table, text
)

# Reads from env var so Docker volume path works; falls back to local file
DB_PATH = os.environ.get("DB_PATH", "customer.db")
TABLE_NAME = "OPERATION"

def get_engine():
    return create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})

def create_table(engine):
    meta = MetaData()
    Table(
        TABLE_NAME, meta,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("Organization_Name", String),
        Column("TIN", String),
        Column("Treasury_Account_Code", String),
        Column("Economic_Classification_Code", String),
        Column("Functional_Classification_Code", String),
        Column("Administrative_Classification_Code", String),
        Column("Category", String),
        Column("Amount", Float),
        Column("Date", Date),
        Column("Supplier_Name", String),
        Column("Supplier_TIN", String),
        Column("Supplier_Bank_Account", String),
        Column("Product_Name", String),
    )
    meta.create_all(engine)
    return meta

def insert_dummy_data(engine):
    organizations = [
        "Ministry of Finance", "Ministry of Health", "Ministry of Education",
        "Ministry of Transport", "Ministry of Agriculture", "Ministry of Defense",
        "Ministry of Justice", "Ministry of Interior", "Ministry of Trade",
        "Ministry of Energy",
    ]
    categories = ["Capital", "Recurrent", "Development", "Emergency", "Social"]
    products = [
        "Office Supplies", "Medical Equipment", "Road Construction",
        "IT Infrastructure", "Agricultural Tools", "Security Equipment",
        "Legal Services", "Training Services", "Energy Equipment", "Consulting",
    ]
    suppliers = [
        ("Alpha Supplies Ltd", "SUP-001", "ET-100-001"),
        ("Beta Construction Co", "SUP-002", "ET-100-002"),
        ("Gamma Tech Solutions", "SUP-003", "ET-100-003"),
        ("Delta Medical Equip", "SUP-004", "ET-100-004"),
        ("Epsilon Logistics", "SUP-005", "ET-100-005"),
        ("Zeta Engineering", "SUP-006", "ET-100-006"),
        ("Eta Services Group", "SUP-007", "ET-100-007"),
        ("Theta Consulting", "SUP-008", "ET-100-008"),
    ]

    rows = []
    base_date = datetime(2024, 1, 1)
    for i in range(1, 201):
        org = random.choice(organizations)
        supplier = random.choice(suppliers)
        product = random.choice(products)
        category = random.choice(categories)
        amount = round(random.uniform(5_000, 2_000_000), 2)
        date = (base_date + timedelta(days=random.randint(0, 500))).date()
        rows.append({
            "Organization_Name": org,
            "TIN": f"TIN-{i:04d}",
            "Treasury_Account_Code": f"TAC-{random.randint(1000, 9999)}",
            "Economic_Classification_Code": f"ECC-{random.randint(100, 999)}",
            "Functional_Classification_Code": f"FCC-{random.randint(100, 999)}",
            "Administrative_Classification_Code": f"ACC-{random.randint(100, 999)}",
            "Category": category,
            "Amount": amount,
            "Date": date,
            "Supplier_Name": supplier[0],
            "Supplier_TIN": supplier[1],
            "Supplier_Bank_Account": supplier[2],
            "Product_Name": product,
        })

    with engine.begin() as conn:
        conn.execute(
            text(f"""
                INSERT INTO {TABLE_NAME} (
                    Organization_Name, TIN, Treasury_Account_Code,
                    Economic_Classification_Code, Functional_Classification_Code,
                    Administrative_Classification_Code, Category, Amount, Date,
                    Supplier_Name, Supplier_TIN, Supplier_Bank_Account, Product_Name
                ) VALUES (
                    :Organization_Name, :TIN, :Treasury_Account_Code,
                    :Economic_Classification_Code, :Functional_Classification_Code,
                    :Administrative_Classification_Code, :Category, :Amount, :Date,
                    :Supplier_Name, :Supplier_TIN, :Supplier_Bank_Account, :Product_Name
                )
            """),
            rows,
        )

def init_db():
    engine = get_engine()
    create_table(engine)
    # Insert dummy data only if the table is empty
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}")).scalar()
    if count == 0:
        insert_dummy_data(engine)
    return engine