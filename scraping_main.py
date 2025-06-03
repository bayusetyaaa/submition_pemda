from utils.transform import transform_data
from utils.load import save_data_csv, Save_data_google_sheets
from utils.extract import scrape_product 
 
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/'
    all_products = scrape_product(BASE_URL)
    for halaman in range(2, 51):
        url_halaman = f"{BASE_URL}page{halaman}"
        print(f"Scraping halaman {halaman}: {url_halaman}")
        try:
            produk = scrape_product(url_halaman)
            all_products.extend(produk)
        except Exception as e:
            print(f"❌ Gagal scraping halaman {halaman}: {e}")

    if not all_products:
        print("❌ Tidak ada produk yang berhasil di-scrape. Program dihentikan.")
        return
 

    data_bersih = transform_data(all_products)
    
    save_data_csv(data_bersih)
    Save_data_google_sheets(
        data_bersih,
        spreadsheet_id='1dVpaL0HkhyklGtbLQfhxhXwzUB7YLg2iICX4YeGZA3I',
        range_sheet='Sheet1!A2'
    )

if __name__ == '__main__':
    main()