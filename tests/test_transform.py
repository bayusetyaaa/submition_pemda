import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.transform import transform_data


class TestTransformData(unittest.TestCase):
    
    def setUp(self):
        """Setup untuk setiap test case"""
        self.sample_data = [
            {
                'title': 'Test Product 1',
                'price': '50.00',
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M, L, XL',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Test Product 2',
                'price': '75.50',
                'rating': 'Rating: 4.2',
                'colors': 'Colors: 2',
                'size': 'Size: S, M',
                'gender': 'Gender: Women'
            }
        ]
    
    def test_transform_data_empty_input(self):
        """Test transform_data dengan input kosong"""
        result = transform_data([])
        
        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue(result.empty)
        expected_columns = ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        self.assertListEqual(list(result.columns), expected_columns)
    
    def test_transform_data_normal_case(self):
        """Test transform_data dengan data normal"""
        result = transform_data(self.sample_data)
        
        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        
        # Check price transformation (multiplied by 16000)
        self.assertEqual(result.iloc[0]['price'], 50.00 * 16000)
        self.assertEqual(result.iloc[1]['price'], 75.50 * 16000)
        
        # Check rating transformation (extracted numbers)
        self.assertEqual(result.iloc[0]['rating'], 4.5)
        self.assertEqual(result.iloc[1]['rating'], 4.2)
        
        # Check colors transformation (extracted numbers)
        self.assertEqual(result.iloc[0]['colors'], 3)
        self.assertEqual(result.iloc[1]['colors'], 2)
        
        # Check size and gender (prefix removed)
        self.assertEqual(result.iloc[0]['size'], 'M, L, XL')
        self.assertEqual(result.iloc[0]['gender'], 'Unisex')
        
        # Check timestamp is added
        self.assertIn('timestamp', result.columns)
        self.assertIsNotNone(result.iloc[0]['timestamp'])
    
    def test_transform_data_unknown_title_removal(self):
        """Test penghapusan produk dengan title 'unknown'"""
        data_with_unknown = [
            {
                'title': 'Unknown Title',
                'price': '50.00',
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Valid Product',
                'price': '75.50',
                'rating': 'Rating: 4.2',
                'colors': 'Colors: 2',
                'size': 'Size: S',
                'gender': 'Gender: Women'
            }
        ]
        
        result = transform_data(data_with_unknown)
        
        # Assert - should only have 1 product (unknown removed)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['title'], 'Valid Product')
    
    def test_transform_data_invalid_price_removal(self):
        """Test penghapusan produk dengan price tidak valid"""
        data_with_invalid_price = [
            {
                'title': 'Product 1',
                'price': '',  # Empty price
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Product 2',
                'price': 'Price Not Available',  # Invalid price
                'rating': 'Rating: 4.2',
                'colors': 'Colors: 2',
                'size': 'Size: S',
                'gender': 'Gender: Women'
            },
            {
                'title': 'Product 3',
                'price': '50.00',  # Valid price
                'rating': 'Rating: 4.0',
                'colors': 'Colors: 1',
                'size': 'Size: L',
                'gender': 'Gender: Men'
            }
        ]
        
        result = transform_data(data_with_invalid_price)
        
        # Assert - should only have 1 product (valid price)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['title'], 'Product 3')
    
    def test_transform_data_invalid_rating_removal(self):
        """Test penghapusan produk dengan rating tidak valid"""
        data_with_invalid_rating = [
            {
                'title': 'Product 1',
                'price': '50.00',
                'rating': 'No Rating',  # Invalid rating
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Product 2',
                'price': '75.50',
                'rating': 'Rating: 4.2',  # Valid rating
                'colors': 'Colors: 2',
                'size': 'Size: S',
                'gender': 'Gender: Women'
            }
        ]
        
        result = transform_data(data_with_invalid_rating)
        
        # Assert - should only have 1 product (valid rating)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['title'], 'Product 2')
    
    def test_transform_data_invalid_colors_removal(self):
        """Test penghapusan produk dengan colors tidak valid"""
        data_with_invalid_colors = [
            {
                'title': 'Product 1',
                'price': '50.00',
                'rating': 'Rating: 4.5',
                'colors': 'No Color Info',  # Invalid colors
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Product 2',
                'price': '75.50',
                'rating': 'Rating: 4.2',
                'colors': 'Colors: 2',  # Valid colors
                'size': 'Size: S',
                'gender': 'Gender: Women'
            }
        ]
        
        result = transform_data(data_with_invalid_colors)
        
        # Assert - should only have 1 product (valid colors)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['title'], 'Product 2')
    
    def test_transform_data_duplicate_removal(self):
        """Test penghapusan duplikat"""
        data_with_duplicates = [
            {
                'title': 'Same Product',
                'price': '50.00',
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Same Product',
                'price': '50.00',
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Different Product',
                'price': '75.50',
                'rating': 'Rating: 4.2',
                'colors': 'Colors: 2',
                'size': 'Size: S',
                'gender': 'Gender: Women'
            }
        ]
        
        result = transform_data(data_with_duplicates)
        
        # Assert - should only have 2 unique products
        self.assertEqual(len(result), 2)
    
    def test_transform_data_price_conversion(self):
        """Test konversi price dengan berbagai format"""
        data_price_formats = [
            {
                'title': 'Product 1',
                'price': '$50.00',  # With dollar sign
                'rating': 'Rating: 4.5',
                'colors': 'Colors: 3',
                'size': 'Size: M',
                'gender': 'Gender: Unisex'
            },
            {
                'title': 'Product 2',
                'price': '75.50 USD',  # With currency
                'rating': 'Rating: 4.2',
                'colors': 'Colors: 2',
                'size': 'Size: S',
                'gender': 'Gender: Women'
            }
        ]
        
        result = transform_data(data_price_formats)
        
        # Assert - prices should be converted correctly
        self.assertEqual(result.iloc[0]['price'], 50.00 * 16000)
        self.assertEqual(result.iloc[1]['price'], 75.50 * 16000)
    
    def test_transform_data_timestamp_format(self):
        """Test format timestamp"""
        result = transform_data(self.sample_data)
        
        # Assert timestamp format
        timestamp_str = result.iloc[0]['timestamp']
        # Should be able to parse the timestamp
        try:
            datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            timestamp_valid = True
        except ValueError:
            timestamp_valid = False
        
        self.assertTrue(timestamp_valid)
    
    def test_transform_data_data_types(self):
        """Test tipe data setelah transformasi"""
        result = transform_data(self.sample_data)
        
        # Assert data types
        self.assertEqual(result['price'].dtype, float)
        self.assertEqual(result['rating'].dtype, float)
        self.assertEqual(result['colors'].dtype, int)
        self.assertEqual(result['title'].dtype, object)
        self.assertEqual(result['size'].dtype, object)
        self.assertEqual(result['gender'].dtype, object)


if __name__ == '__main__':
    unittest.main()