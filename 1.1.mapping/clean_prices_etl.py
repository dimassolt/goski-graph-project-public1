import pandas as pd
import re

def clean_price(value):
    """
    Normalize messy currency strings to decimal format (e.g. 1349.00)
    Handles:
    - "1349" → "1349.00"
    - "1826,65" → "1826.65"
    - "1,349.00" → "1349.00"
    """
    if pd.isna(value):
        return "0.00"

    val = str(value).strip().replace(" ", "")

    # 1. "1,349.00" → "1349.00"
    if "," in val and "." in val:
        val = val.replace(",", "")
    # 2. "1826,65" → "1826.65"
    elif "," in val and not "." in val:
        val = val.replace(",", ".")

    # Remove anything except digits and dot
    val = re.sub(r"[^0-9.]", "", val)

    try:
        return f"{float(val):.2f}"
    except:
        return "0.00"

# === ETL PROCESS ===
INPUT_PATH = "datasources/scheduleFaked.csv"
OUTPUT_PATH = "datasources/schedule_cleaned.csv"

df = pd.read_csv(INPUT_PATH)

# Clean price columns
df["Appointment Price"] = df["Appointment Price"].apply(clean_price)
df["Amount Paid Online"] = df["Amount Paid Online"].apply(clean_price)

# Save cleaned file
df.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Cleaned CSV saved to {OUTPUT_PATH}")
