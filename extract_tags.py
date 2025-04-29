# extract_tags.py

import pandas as pd
from datetime import datetime

# Mapping for companies to Pharma categories
COMPANY_CATEGORY_MAP = {
    "Pfizer": "Big Pharma",
    "Novartis": "Big Pharma",
    "Roche": "Big Pharma",
    "Moderna": "Biotech",
    "Amgen": "Biotech",
    "Regeneron": "Biotech",
    "Acme Pharmaceuticals": "Mid Pharma",
    "MediHealth": "Mid Pharma",
}

DEFAULT_CATEGORY = "Other"

from datetime import datetime

def to_date(row, prefix):
    try:
        year = int(row[f"{prefix}_year"])
        month = int(row.get(f"{prefix}_month", 1)) or 1
        return datetime(year, month, 1)
    except:
        return None

def compute_years_of_experience(positions_df):
    positions_df["start_dt"] = positions_df.apply(lambda row: to_date(row, "start"), axis=1)
    valid_starts = positions_df["start_dt"].dropna()
    if valid_starts.empty:
        return 0
    earliest_start = min(valid_starts)
    today = datetime.today()
    return max(0, today.year - earliest_start.year - ((today.month, today.day) < (earliest_start.month, earliest_start.day)))

def compute_pharma_distribution(positions_df):
    positions_df["start_dt"] = positions_df.apply(lambda row: to_date(row, "start"), axis=1)
    positions_df["end_dt"] = positions_df.apply(lambda row: to_date(row, "end") or datetime.today(), axis=1)
    positions_df["months_spent"] = (positions_df["end_dt"] - positions_df["start_dt"]).dt.days / 30.44

    category_months = {"Big Pharma": 0, "Mid Pharma": 0, "Biotech": 0, "Other": 0}
    for _, row in positions_df.iterrows():
        company = row["company_name"]
        months = row.get("months_spent", 0)
        category = COMPANY_CATEGORY_MAP.get(company, DEFAULT_CATEGORY)
        category_months[category] += months

    total = sum(category_months.values())
    if total == 0:
        return {k: 0.0 for k in category_months}
    return {k: round((v / total) * 100, 1) for k, v in category_months.items()}

    positions_df["start_dt"] = positions_df.apply(lambda row: to_date(row, "start"), axis=1)
    positions_df["end_dt"] = positions_df.apply(lambda row: to_date(row, "end") or datetime.today(), axis=1)
    positions_df["months_spent"] = (positions_df["end_dt"] - positions_df["start_dt"]).dt.days / 30.44

    category_months = {"Big Pharma": 0, "Mid Pharma": 0, "Biotech": 0, "Other": 0}
    for _, row in positions_df.iterrows():
        company = row["company_name"]
        months = row.get("months_spent", 0)
        category = COMPANY_CATEGORY_MAP.get(company, DEFAULT_CATEGORY)
        category_months[category] += months

    total = sum(category_months.values())
    if total == 0:
        return {k: 0.0 for k in category_months}
    return {k: round((v / total) * 100, 1) for k, v in category_months.items()}