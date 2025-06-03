import os
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def save_data_csv(df, nama_file="products.csv"):
    """Simpan DataFrame ke file CSV."""
    df.to_csv(nama_file, index=False)
    print(f"✅ Data berhasil disimpan ke {nama_file}")
def Save_data_google_sheets(df, spreadsheet_id, range_sheet):
    """Simpan DataFrame ke Google Sheets."""
    if not os.path.exists('API.json'):
        print("❌ File key_api.json tidak ditemukan, lewati upload ke Google Sheets.")
        return

    try:
        creds = Credentials.from_service_account_file('API.json')
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}

        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_sheet,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"✅ Data berhasil disimpan di Google Sheets pada {range_sheet}")

    except Exception as e:
        print(f"❌ Gagal simpan ke Google Sheets: {e}")