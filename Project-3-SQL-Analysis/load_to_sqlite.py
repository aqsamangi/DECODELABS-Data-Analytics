import pandas as pd     # to read the Excel file
import sqlite3          # Python's built-in SQLite library - no install needed

# ---------------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------------
INPUT_FILE = "Cleaned_Dataset_for_Data_Analytics.xlsx"
DATABASE_FILE = "orders.db"
TABLE_NAME = "orders"


def main():
    print("=" * 70)
    print("LOADING EXCEL FILE INTO SQLITE DATABASE")
    print("=" * 70)

    # Step 1: Read the cleaned Excel file into a pandas DataFrame
    df = pd.read_excel(INPUT_FILE)
    print(f"Loaded '{INPUT_FILE}' - {df.shape[0]} rows, {df.shape[1]} columns")

    # Step 2: Connect to (and automatically create) the SQLite database file
    conn = sqlite3.connect(DATABASE_FILE)

    # Step 3: Write the DataFrame into a table inside that database.
    # if_exists="replace" means: if you run this script again, it will
    # safely rebuild the table instead of duplicating rows.
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)

    # Step 4: Quick sanity check - count the rows that made it into SQL
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    row_count = cursor.fetchone()[0]
    print(f"Table '{TABLE_NAME}' created inside '{DATABASE_FILE}' "
          f"with {row_count} rows.")

    conn.close()
    print("=" * 70)
    print(f"DONE. You now have a real SQL database: {DATABASE_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
