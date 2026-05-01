import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# =========================
# Reproducibility
# =========================

np.random.seed(42)
random.seed(42)

# =========================
# Material profiles
# =========================

materials = {
    "Steel": {
        "base_price": 950,
        "std": 90,
        "quantity_range": (50, 600),
        "delivery_range": (5, 16),
        "unit": "per_tonne"
    },
    "Concrete": {
        "base_price": 180,
        "std": 25,
        "quantity_range": (100, 1500),
        "delivery_range": (3, 12),
        "unit": "per_cubic_meter"
    },
    "Wood": {
        "base_price": 75,
        "std": 15,
        "quantity_range": (100, 1000),
        "delivery_range": (4, 14),
        "unit": "per_board_unit"
    },
    "Aluminum": {
        "base_price": 1600,
        "std": 180,
        "quantity_range": (20, 400),
        "delivery_range": (7, 22),
        "unit": "per_tonne"
    },
    "Copper": {
        "base_price": 8200,
        "std": 700,
        "quantity_range": (10, 200),
        "delivery_range": (7, 25),
        "unit": "per_tonne"
    }
}

# =========================
# More realistic uneven distribution
# =========================
# Common materials appear more often.
# Overall target:
# 750 Normal rows
# 250 Anomaly rows
# 1000 Total rows

material_row_counts = {
    "Steel": {"normal": 225, "anomaly": 75},
    "Concrete": {"normal": 188, "anomaly": 62},
    "Wood": {"normal": 150, "anomaly": 50},
    "Aluminum": {"normal": 112, "anomaly": 38},
    "Copper": {"normal": 75, "anomaly": 25}
}

# =========================
# Supplier pricing behavior
# =========================

suppliers = {
    "ABC Suppliers": 0.98,
    "XYZ Materials": 1.02,
    "BuildCo": 1.08,
    "Prime Industrial": 1.00,
    "NorthSteel": 0.95,
    "RapidSupply": 1.12,
    "Maple Materials": 1.03,
    "BudgetSource": 0.90
}

# =========================
# Regional market effect
# =========================

regions = {
    "Ontario": 1.00,
    "Quebec": 0.98,
    "New York": 1.04,
    "Michigan": 1.02
}

file_types = ["PDF", "CSV", "Excel"]

start_date = datetime(2025, 1, 1)
rows = []
quote_number = 1

# =========================
# Helper functions
# =========================

def random_quote_date():
    days_offset = random.randint(0, 420)
    return start_date + timedelta(days=days_offset)


def seasonal_factor(date):
    # Small seasonal price variation
    if date.month in [1, 2, 3]:
        return 0.98
    elif date.month in [4, 5, 6]:
        return 1.00
    elif date.month in [7, 8, 9]:
        return 1.03
    else:
        return 1.05


def quantity_discount(quantity, max_quantity):
    # Larger orders get small discount
    if quantity > max_quantity * 0.75:
        return random.uniform(0.93, 0.98)
    elif quantity > max_quantity * 0.50:
        return random.uniform(0.96, 1.00)
    return random.uniform(0.99, 1.03)


def add_row(
    supplier_name,
    material_name,
    unit_price,
    quantity,
    delivery_days,
    region,
    quote_date,
    file_type,
    risk_status,
    risk_reason
):
    global quote_number

    total_price = round(unit_price * quantity, 2)

    rows.append({
        "quoteId": f"Q{quote_number:05d}",
        "supplierName": supplier_name,
        "materialName": material_name,
        "unitPrice": round(unit_price, 2),
        "quantity": int(quantity),
        "totalPrice": total_price,
        "deliveryDays": int(delivery_days),
        "region": region,
        "quoteDate": quote_date.strftime("%Y-%m-%d"),
        "fileType": file_type,
        "riskStatus": risk_status,
        "riskReason": risk_reason
    })

    quote_number += 1

# =========================
# Generate normal records
# =========================

for material_name, counts in material_row_counts.items():
    config = materials[material_name]

    for _ in range(counts["normal"]):
        supplier_name = random.choice(list(suppliers.keys()))
        region = random.choice(list(regions.keys()))
        quote_date = random_quote_date()
        file_type = random.choice(file_types)

        quantity = random.randint(*config["quantity_range"])
        max_quantity = config["quantity_range"][1]

        unit_price = np.random.normal(config["base_price"], config["std"])
        unit_price *= suppliers[supplier_name]
        unit_price *= regions[region]
        unit_price *= seasonal_factor(quote_date)
        unit_price *= quantity_discount(quantity, max_quantity)

        unit_price = max(unit_price, 1)
        delivery_days = random.randint(*config["delivery_range"])

        add_row(
            supplier_name=supplier_name,
            material_name=material_name,
            unit_price=unit_price,
            quantity=quantity,
            delivery_days=delivery_days,
            region=region,
            quote_date=quote_date,
            file_type=file_type,
            risk_status="Normal",
            risk_reason="Quote is within expected range"
        )

# =========================
# Generate anomaly records
# =========================

for material_name, counts in material_row_counts.items():
    config = materials[material_name]

    for _ in range(counts["anomaly"]):
        supplier_name = random.choice(list(suppliers.keys()))
        region = random.choice(list(regions.keys()))
        quote_date = random_quote_date()
        file_type = random.choice(file_types)
        quantity = random.randint(*config["quantity_range"])

        anomaly_type = random.choice([
            "very_high_price",
            "very_low_price",
            "long_delivery",
            "high_price_and_slow_delivery",
            "large_order_high_price"
        ])

        if anomaly_type == "very_high_price":
            unit_price = config["base_price"] * random.uniform(1.45, 2.25)
            delivery_days = random.randint(*config["delivery_range"])
            risk_reason = "Unit price is much higher than expected"

        elif anomaly_type == "very_low_price":
            unit_price = config["base_price"] * random.uniform(0.25, 0.50)
            delivery_days = random.randint(*config["delivery_range"])
            risk_reason = "Unit price is unusually low"

        elif anomaly_type == "long_delivery":
            unit_price = np.random.normal(config["base_price"], config["std"])
            delivery_days = random.randint(31, 65)
            risk_reason = "Delivery time is unusually long"

        elif anomaly_type == "high_price_and_slow_delivery":
            unit_price = config["base_price"] * random.uniform(1.35, 1.95)
            delivery_days = random.randint(30, 60)
            risk_reason = "High price and slow delivery"

        else:
            # Large order should normally receive a discount,
            # but this anomaly keeps unit price unexpectedly high.
            quantity = random.randint(
                int(config["quantity_range"][1] * 0.75),
                config["quantity_range"][1]
            )
            unit_price = config["base_price"] * random.uniform(1.20, 1.60)
            delivery_days = random.randint(*config["delivery_range"])
            risk_reason = "Large order has unexpectedly high unit price"

        unit_price = max(unit_price, 1)

        add_row(
            supplier_name=supplier_name,
            material_name=material_name,
            unit_price=unit_price,
            quantity=quantity,
            delivery_days=delivery_days,
            region=region,
            quote_date=quote_date,
            file_type=file_type,
            risk_status="Anomaly",
            risk_reason=risk_reason
        )

# =========================
# Create DataFrame
# =========================

df = pd.DataFrame(rows)

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save dataset
output_file = "supplier_quotes_synthetic_realistic.csv"
df.to_csv(output_file, index=False)

# =========================
# Summary output
# =========================

print("Dataset created successfully.")
print(f"File saved as: {output_file}")
print(f"Total rows: {len(df)}")
print(f"Total columns: {df.shape[1]}")

print("\nRisk status distribution:")
print(df["riskStatus"].value_counts())

print("\nMaterial distribution:")
print(df["materialName"].value_counts())

print("\nMaterial distribution by risk status:")
print(pd.crosstab(df["materialName"], df["riskStatus"]))

print("\nMissing values by column:")
print(df.isnull().sum())

print("\nPreview:")
print(df.head(10))