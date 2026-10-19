import pandas as pd
import sqlite3

# 1. File CSV: Le vendite
df_sales = pd.DataFrame({
    "store_id": ["S1", "S2", "S1", "S3", "S2"],
    "product": ["P1", "P2", "P1", "P3", "P2"],
    "date": ["2023-01-01", "2023-01-02", "2023-01-08", "2023-01-10", "2023-01-15"],
    "qty": [10, 5, 7, 2, 8]
})
df_sales.to_csv("sales.csv", index=False)

# 2. File JSONL: Info sui negozi
df_stores = pd.DataFrame({
    "store_id": ["S1", "S2", "S3"],
    "region": ["Nord", "Sud", "Centro"]
})
df_stores.to_json("stores.jsonl", orient="records", lines=True)

# 3. Database SQL: Promozioni
conn = sqlite3.connect("example.db")
df_promo = pd.DataFrame({
    "store_id": ["S1", "S2", "S3"],
    "promo_flag": [1, 0, 1]
})
df_promo.to_sql("promotions", conn, if_exists="replace", index=False)
conn.close()

print("File di prova creati con successo!")


