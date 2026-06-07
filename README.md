# streamlit_database# 🏦 Operations Query Dashboard

A Streamlit web application for querying and exploring government operation records stored in a SQLite database. Runs locally or inside Docker.

---

## 📁 Project Structure

```
streamlit_database/
├── main.py               # Streamlit UI — search form, metrics, dataframe
├── database.py           # DB setup, table creation, dummy data insertion
├── resources.py          # Query builder and summary stats logic
├── requirements.txt      # Python dependencies
├── Dockerfile            # Container image definition
├── docker-compose.yml    # Docker Compose service config
├── .dockerignore         # Files excluded from the Docker build
└── README.md             # This file
```

---

## 🗄️ Database Schema

Table name: `OPERATION`

| Column                           | Type    | Description                        |
|----------------------------------|---------|------------------------------------|
| Organization_Name                | String  | Name of the government organization|
| TIN                              | String  | Taxpayer Identification Number     |
| Treasury_Account_Code            | String  | Treasury account reference code    |
| Economic_Classification_Code     | String  | Economic classification code       |
| Functional_Classification_Code   | String  | Functional classification code     |
| Administrative_Classification_Code | String | Administrative classification code|
| Category                         | String  | Capital / Recurrent / Development  |
| Amount                           | Float   | Transaction amount                 |
| Date                             | Date    | Transaction date                   |
| Supplier_Name                    | String  | Name of the supplier               |
| Supplier_TIN                     | String  | Supplier TIN                       |
| Supplier_Bank_Account            | String  | Supplier bank account number       |
| Product_Name                     | String  | Name of the product or service     |

> On first launch, **200 dummy records** are automatically inserted if the table is empty.

---

## 🚀 Running with Docker (Recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- WSL 2 integration enabled (Windows users) — Docker Desktop → Settings → Resources → WSL Integration

### Start the app

```bash
docker compose up --build
```

Then open your browser at: **http://localhost:8501**

### Stop the app

```bash
docker compose down
```

### Run in the background

```bash
docker compose up --build -d
```

### View logs

```bash
docker compose logs -f
```

---

## 💻 Running Locally (Without Docker)

### Prerequisites
- Python 3.10+

### Install dependencies

```bash
pip install -r requirements.txt
```

### Start the app

```bash
streamlit run main.py
```

Then open your browser at: **http://localhost:8501**

---

## 🔍 Search Filters

The sidebar provides the following filters — all fields are optional and can be combined:

| Filter                         | Type         | Description                          |
|-------------------------------|--------------|--------------------------------------|
| Organization Name              | Text (partial match) | Filter by organization name  |
| TIN                            | Text (partial match) | Filter by TIN                |
| Treasury Account Code          | Text (partial match) | Filter by account code       |
| Functional Classification Code | Text (partial match) | Filter by functional code    |
| Category                       | Dropdown     | Capital, Recurrent, Development, etc.|
| Supplier Name                  | Text (partial match) | Filter by supplier name      |
| Supplier TIN                   | Text (partial match) | Filter by supplier TIN       |
| Supplier Bank Account          | Text (partial match) | Filter by bank account       |
| Product Name                   | Text (partial match) | Filter by product/service    |
| Amount Min / Max               | Number       | Filter by amount range               |
| Date From / To                 | Date picker  | Filter by transaction date range     |
| Max Records                    | Number       | Limit results (0 = return all)       |

---

## 📊 Dashboard Features

- **Summary metrics** — total records, total amount, average amount, unique organizations
- **Sortable dataframe** — click any column header to sort
- **CSV export** — download filtered results with one click
- **Persistent database** — SQLite file stored in a Docker named volume (`db_data`), survives container restarts and rebuilds

---

## ⚙️ Environment Variables

| Variable  | Default        | Description                          |
|-----------|----------------|--------------------------------------|
| `DB_PATH` | `customer.db`  | Path to the SQLite database file     |

When running with Docker, `DB_PATH` is automatically set to `/data/customer.db` (inside the named volume).

---

## 🛠️ Tech Stack

| Tool          | Purpose                        |
|---------------|--------------------------------|
| Streamlit     | Web UI framework               |
| SQLAlchemy    | Database ORM / query engine    |
| SQLite        | Lightweight embedded database  |
| Pandas        | DataFrame display and export   |
| Docker        | Containerisation               |