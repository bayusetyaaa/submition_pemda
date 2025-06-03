import os
import pandas as pd

def save_data_csv(df, nama_file="products.csv"):
    """Simpan DataFrame ke file CSV."""
    df.to_csv(nama_file, index=False)
    print(f"✅ Data berhasil disimpan ke {nama_file}")
