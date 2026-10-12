import pandas as pd  # type: ignore[import]   
import re              

INPUT_FILE = "Dataset for Data Analytics.xlsx"
OUTPUT_FILE = "Cleaned_Dataset_for_Data_Analytics.xlsx"


def main():
    print("=" * 70)
    print("STEP 1: LOADING THE RAW DATA")
    print("=" * 70)

    df = pd.read_excel(INPUT_FILE)

    original_row_count = len(df)
    original_missing_total = df.isnull().sum().sum()
    original_duplicate_rows = df.duplicated().sum()
    original_duplicate_ids = df["OrderID"].duplicated().sum()

    print(f"Loaded '{INPUT_FILE}'")
    print(f"Rows: {original_row_count} | Columns: {df.shape[1]}")
    print(f"Column names: {list(df.columns)}")
    print()

    # REMOVE COMPLETELY BLANK ROWS (if any exist)
    
    print("=" * 70)
    print("STEP 2: CHECKING FOR COMPLETELY BLANK ROWS")
    print("=" * 70)
    blank_rows_before = df.isnull().all(axis=1).sum()
    df = df.dropna(how="all")  # drop rows where EVERY column is empty
    print(f"Completely blank rows found and removed: {blank_rows_before}")
    print()

    # REMOVE DUPLICATE ROWS
   
    print("=" * 70)
    print("STEP 3: CHECKING FOR DUPLICATE ROWS")
    print("=" * 70)
    dup_rows_before = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"Exact duplicate rows found and removed: {dup_rows_before}")
    print()

    # REMOVE DUPLICATE ORDER IDs
  
    print("=" * 70)
    print("STEP 4: CHECKING FOR DUPLICATE ORDER IDs")
    print("=" * 70)
    dup_ids_before = df["OrderID"].duplicated().sum()
    df = df.drop_duplicates(subset="OrderID", keep="first")
    print(f"Duplicate OrderID rows found and removed: {dup_ids_before}")
    print()

    # FIX TEXT FORMATTING (spaces + inconsistent capitalization)
    
    print("=" * 70)
    print("STEP 5: CLEANING TEXT COLUMNS (spaces & capitalization)")
    print("=" * 70)

    text_columns = [
        "OrderID", "CustomerID", "Product", "ShippingAddress",
        "PaymentMethod", "OrderStatus", "TrackingNumber",
        "CouponCode", "ReferralSource",
    ]

    whitespace_fixed = 0
    for col in text_columns:
        before = df[col].astype("string")
        after = before.str.strip()
        whitespace_fixed += (before != after).sum()
        df[col] = after

    category_columns = ["Product", "PaymentMethod", "OrderStatus",
                         "ReferralSource", "CouponCode"]
    for col in category_columns:
        df[col] = df[col].str.title()  # e.g. "credit card" -> "Credit Card"

    print(f"Cells with extra leading/trailing spaces removed: {whitespace_fixed}")
    print("Capitalization standardized (Title Case) for: "
          f"{category_columns}")
    print()

    # FIX / VERIFY DATE FORMAT   
    # requires ISO format dates (YYYY-MM-DD).
    print("=" * 70)
    print("STEP 6: CHECKING DATE FORMAT")
    print("=" * 70)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    bad_dates = df["Date"].isnull().sum()
    print(f"Rows with a date Python could not understand: {bad_dates}")
    # Store the date as a clean ISO string YYYY-MM-DD for the final file
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    print("All dates converted to ISO 8601 format (YYYY-MM-DD).")
    print()

    # FIX NUMBER FORMATS / INVALID VALUES
    print("=" * 70)
    print("STEP 7: CHECKING NUMBER COLUMNS")
    print("=" * 70)
    numeric_columns = ["Quantity", "UnitPrice", "ItemsInCart", "TotalPrice"]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["UnitPrice"] = df["UnitPrice"].round(2)
    df["TotalPrice"] = df["TotalPrice"].round(2)

    invalid_quantity = (df["Quantity"] <= 0).sum()
    invalid_price = (df["UnitPrice"] <= 0).sum()
    print(f"Rows with Quantity <= 0: {invalid_quantity}")
    print(f"Rows with UnitPrice <= 0: {invalid_price}")
    print("Money columns (UnitPrice, TotalPrice) rounded to 2 decimal places.")
    print()

    # HANDLE MISSING VALUES
    print("=" * 70)
    print("STEP 8: HANDLING MISSING VALUES")
    print("=" * 70)
    missing_before = df.isnull().sum()
    print("Missing values BEFORE handling (by column):")
    print(missing_before[missing_before > 0])
    print()

    if "CouponCode" in df.columns:
        df["CouponCode"] = df["CouponCode"].fillna("No Coupon")

    for col in numeric_columns:
        if df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"Filled missing '{col}' values with median: {median_val}")

    missing_after = df.isnull().sum().sum()
    print(f"Missing values AFTER handling (total): {missing_after}")
    print()

    # FINAL VERIFICATION CHECKS
    print("=" * 70)
    print("STEP 9: FINAL VERIFICATION")
    print("=" * 70)
    final_row_count = len(df)
    final_missing_total = df.isnull().sum().sum()
    final_duplicate_rows = df.duplicated().sum()
    final_duplicate_ids = df["OrderID"].duplicated().sum()
    final_bad_dates = df["Date"].isnull().sum()

    print(f"Row count   -> before: {original_row_count}  | after: {final_row_count}")
    print(f"Missing vals-> before: {original_missing_total} | after: {final_missing_total}")
    print(f"Dup rows    -> before: {original_duplicate_rows} | after: {final_duplicate_rows}")
    print(f"Dup IDs     -> before: {original_duplicate_ids} | after: {final_duplicate_ids}")
    print(f"Bad dates   -> after:  {final_bad_dates}")
    print()

    assert final_duplicate_ids == 0, "There are still duplicate OrderIDs!"
    assert final_bad_dates == 0, "There are still incorrectly formatted dates!"
    print("VERIFICATION PASSED: 0 duplicate IDs and 0 bad dates.")
    print()

    # SAVE THE CLEANED FILE
    df.to_excel(OUTPUT_FILE, index=False)
    print("=" * 70)
    print(f"CLEANED FILE SAVED AS: {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()