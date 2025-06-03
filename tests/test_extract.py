import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.extract import scrape_product


class TestScrapeProduct(unittest.TestCase):
    
    def setUp(self):
        """Setup untuk setiap test case"""
        self.test_url = "https://fashion-studio.dicoding.dev/"
        
        # Mock HTML response dengan struktur yang sesuai
        self.mock_html = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Test Product 1</h3>
                    <div class="price-container">$50.00</div>
                    <p>Rating: 4.5</p>
                    <p>Colors: 3</p>
                    <p>Size: M, L, XL</p>
                    <p>Gender: Unisex</p>
                </div>
                <div class="collection-card">
                    <h3 class="product-title">Test Product 2</h3>
                    <div class="price-container">$75.00</div>
                    <p>Rating: 4.2</p>
                    <p>Colors: 2</p>
                    <p>Size: S, M</p>
                    <p>Gender: Women</p>
                </div>
            </body>
        </html>
        """
    
    @patch('utils.extract.requests.get')
    def test_scrape_product_success(self, mock_get):
        """Test scraping produk berhasil"""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = self.mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Execute
        result = scrape_product(self.test_url)
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'Test Product 1')
        self.assertEqual(result[0]['price'], '$50.00')
        self.assertEqual(result[0]['rating'], 'Rating: 4.5')
        self.assertEqual(result[1]['title'], 'Test Product 2')
        mock_get.assert_called_once_with(self.test_url, timeout=10)
    
    @patch('utils.extract.requests.get')
    def test_scrape_product_no_cards_found(self, mock_get):
        """Test ketika tidak ada cards ditemukan"""
        # Setup mock response tanpa collection-card
        mock_html_empty = "<html><body><div>No products</div></body></html>"
        mock_response = Mock()
        mock_response.text = mock_html_empty
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Execute dengan capture print output
        with patch('builtins.print') as mock_print:
            result = scrape_product(self.test_url)
        
        # Assert
        self.assertEqual(len(result), 0)
        mock_print.assert_called()
    
    @patch('utils.extract.requests.get')
    def test_scrape_product_missing_elements(self, mock_get):
        """Test ketika beberapa elemen tidak ada"""
        mock_html_partial = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Incomplete Product</h3>
                    <!-- Missing price, rating, etc -->
                </div>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = mock_html_partial
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Execute
        result = scrape_product(self.test_url)
        
        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Incomplete Product')
        self.assertEqual(result[0]['price'], 'Price Not Available')
        self.assertEqual(result[0]['rating'], 'No Rating')
        self.assertEqual(result[0]['colors'], 'No Color Info')
    
    @patch('utils.extract.requests.get')
    def test_scrape_product_request_exception(self, mock_get):
        """Test ketika terjadi RequestException"""
        # Setup mock to raise RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        # Execute & Assert
        with self.assertRaises(Exception) as context:
            scrape_product(self.test_url)
        
        self.assertIn("Gagal mengakses", str(context.exception))
        self.assertIn("Network error", str(context.exception))
    
    @patch('utils.extract.requests.get')
    def test_scrape_product_http_error(self, mock_get):
        """Test ketika terjadi HTTP error"""
        # Setup mock response dengan HTTP error
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        # Execute & Assert
        with self.assertRaises(Exception) as context:
            scrape_product(self.test_url)
        
        self.assertIn("Gagal mengakses", str(context.exception))
    
    @patch('utils.extract.requests.get')
    @patch('utils.extract.BeautifulSoup')
    def test_scrape_product_parsing_error(self, mock_soup, mock_get):
        """Test ketika terjadi error saat parsing HTML"""
        # Setup mock response
        mock_response = Mock()
        mock_response.text = self.mock_html
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Setup BeautifulSoup mock to raise exception
        mock_soup.side_effect = Exception("Parsing error")
        
        # Execute & Assert
        with self.assertRaises(Exception) as context:
            scrape_product(self.test_url)
        
        self.assertIn("Kesalahan saat parsing HTML", str(context.exception))
    
    @patch('utils.extract.requests.get')
    def test_scrape_product_timeout(self, mock_get):
        """Test ketika terjadi timeout"""
        # Setup mock to raise Timeout
        mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
        
        # Execute & Assert
        with self.assertRaises(Exception) as context:
            scrape_product(self.test_url)
        
        self.assertIn("Gagal mengakses", str(context.exception))
        self.assertIn("Request timeout", str(context.exception))


if __name__ == '__main__':
    unittest.main()