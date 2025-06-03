import unittest
import pandas as pd
import os
import tempfile
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.load import save_data_csv
from unittest.mock import patch, MagicMock


class TestSaveDataCSV(unittest.TestCase):
    
    def setUp(self):
        """Setup untuk setiap test case"""
        # Create sample DataFrame
        self.sample_df = pd.DataFrame({
            'title': ['Product 1', 'Product 2', 'Product 3'],
            'price': [50.0, 75.5, 100.0],
            'rating': [4.5, 4.2, 4.8],
            'colors': [3, 2, 1],
            'size': ['M, L, XL', 'S, M', 'L'],
            'gender': ['Unisex', 'Women', 'Men'],
            'timestamp': ['2024-01-01 10:00:00', '2024-01-01 10:01:00', '2024-01-01 10:02:00']
        })
        
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Cleanup setelah setiap test case"""
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_save_data_csv_default_filename(self):
        """Test save_data_csv dengan filename default"""
        temp_file = os.path.join(self.temp_dir, "products.csv")
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            with patch('builtins.print') as mock_print:
                save_data_csv(self.sample_df)
            
            # Assert file was created
            self.assertTrue(os.path.exists("products.csv"))
            
            # Assert print was called
            mock_print.assert_called_once_with("✅ Data berhasil disimpan ke products.csv")
            
            # Assert file content
            loaded_df = pd.read_csv("products.csv")
            pd.testing.assert_frame_equal(loaded_df, self.sample_df)
            
        finally:
            os.chdir(original_cwd)
    
    def test_save_data_csv_custom_filename(self):
        """Test save_data_csv dengan filename custom"""
        custom_filename = os.path.join(self.temp_dir, "custom_products.csv")
        
        with patch('builtins.print') as mock_print:
            save_data_csv(self.sample_df, custom_filename)
        
        # Assert file was created
        self.assertTrue(os.path.exists(custom_filename))
        
        # Assert print was called with correct message
        mock_print.assert_called_once_with(f"✅ Data berhasil disimpan ke {custom_filename}")
        
        # Assert file content
        loaded_df = pd.read_csv(custom_filename)
        pd.testing.assert_frame_equal(loaded_df, self.sample_df)
    
    def test_save_data_csv_empty_dataframe(self):
        """Test save_data_csv dengan DataFrame kosong"""
        empty_df = pd.DataFrame()
        temp_file = os.path.join(self.temp_dir, "empty.csv")
        
        with patch('builtins.print') as mock_print:
            save_data_csv(empty_df, temp_file)
        
        # Assert file was created
        self.assertTrue(os.path.exists(temp_file))
        
        # Assert print was called
        mock_print.assert_called_once_with(f"✅ Data berhasil disimpan ke {temp_file}")
        
        # Check file content manually (pandas can't read completely empty CSV)
        with open(temp_file, 'r') as f:
            content = f.read().strip()
        
        # File should be empty or contain only newlines for empty DataFrame
        self.assertEqual(content, "")
    
    def test_save_data_csv_empty_with_columns(self):
        """Test save_data_csv dengan DataFrame yang memiliki columns tapi tidak ada data"""
        empty_with_cols_df = pd.DataFrame(columns=['title', 'price', 'rating'])
        temp_file = os.path.join(self.temp_dir, "empty_with_cols.csv")
        
        with patch('builtins.print') as mock_print:
            save_data_csv(empty_with_cols_df, temp_file)
        
        # Assert file was created
        self.assertTrue(os.path.exists(temp_file))
        
        # Assert print was called
        mock_print.assert_called_once_with(f"✅ Data berhasil disimpan ke {temp_file}")
        
        # Assert file content (should have headers)
        loaded_df = pd.read_csv(temp_file)
        self.assertTrue(loaded_df.empty)  # No data rows
        self.assertListEqual(list(loaded_df.columns), ['title', 'price', 'rating'])  # But has columns
    
    def test_save_data_csv_single_row(self):
        """Test save_data_csv dengan satu baris data"""
        single_row_df = pd.DataFrame({
            'title': ['Single Product'],
            'price': [99.99],
            'rating': [5.0]
        })
        temp_file = os.path.join(self.temp_dir, "single.csv")
        
        with patch('builtins.print') as mock_print:
            save_data_csv(single_row_df, temp_file)
        
        # Assert file was created
        self.assertTrue(os.path.exists(temp_file))
        
        # Assert file content
        loaded_df = pd.read_csv(temp_file)
        pd.testing.assert_frame_equal(loaded_df, single_row_df)
    
    def test_save_data_csv_with_special_characters(self):
        """Test save_data_csv dengan karakter special"""
        special_df = pd.DataFrame({
            'title': ['Product with "quotes"', 'Product with ,comma', 'Product with \nnewline'],
            'description': ['Description, with comma', 'Description "with quotes"', 'Description\nwith newline'],
            'price': [10.0, 20.0, 30.0]
        })
        temp_file = os.path.join(self.temp_dir, "special.csv")
        
        with patch('builtins.print') as mock_print:
            save_data_csv(special_df, temp_file)
        
        # Assert file was created
        self.assertTrue(os.path.exists(temp_file))
        
        # Assert file content (pandas should handle special characters properly)
        loaded_df = pd.read_csv(temp_file)
        pd.testing.assert_frame_equal(loaded_df, special_df)
    
    def test_save_data_csv_overwrite_existing(self):
        """Test save_data_csv menimpa file yang sudah ada"""
        temp_file = os.path.join(self.temp_dir, "overwrite.csv")
        
        # Create initial file
        initial_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        initial_df.to_csv(temp_file, index=False)
        
        # Save new data
        with patch('builtins.print') as mock_print:
            save_data_csv(self.sample_df, temp_file)
        
        # Assert file was overwritten
        loaded_df = pd.read_csv(temp_file)
        pd.testing.assert_frame_equal(loaded_df, self.sample_df)
        
        # Should not contain initial data
        self.assertNotIn('col1', loaded_df.columns)
        self.assertNotIn('col2', loaded_df.columns)
    
    def test_save_data_csv_with_index(self):
        """Test bahwa index tidak disimpan (sesuai dengan parameter index=False)"""
        temp_file = os.path.join(self.temp_dir, "no_index.csv")
        
        # Create DataFrame with custom index
        df_with_index = self.sample_df.copy()
        df_with_index.index = ['A', 'B', 'C']
        
        save_data_csv(df_with_index, temp_file)
        
        # Read file and check
        with open(temp_file, 'r') as f:
            content = f.read()
        
        # Assert that custom index values are not in the file
        self.assertNotIn(',A,', content)
        self.assertNotIn(',B,', content)
        self.assertNotIn(',C,', content)
        
        # Assert first line starts with column names, not index
        first_line = content.split('\n')[0]
        self.assertTrue(first_line.startswith('title,'))
    
    @patch('pandas.DataFrame.to_csv')
    def test_save_data_csv_pandas_error(self, mock_to_csv):
        """Test ketika terjadi error saat pandas menyimpan CSV"""
        # Setup mock to raise exception
        mock_to_csv.side_effect = Exception("Disk full")
        temp_file = os.path.join(self.temp_dir, "error.csv")
        
        # Execute & Assert
        with self.assertRaises(Exception) as context:
            save_data_csv(self.sample_df, temp_file)
        
        self.assertIn("Disk full", str(context.exception))
    
    def test_save_data_csv_invalid_path(self):
        """Test save_data_csv dengan path yang tidak valid"""
        invalid_path = "/invalid/path/that/does/not/exist/file.csv"
        
        # Execute & Assert
        with self.assertRaises(Exception):
            save_data_csv(self.sample_df, invalid_path)
    
    def test_save_data_csv_filename_with_extension(self):
        """Test dengan berbagai ekstensi filename"""
        # Test dengan ekstensi .csv
        csv_file = os.path.join(self.temp_dir, "test.csv")
        save_data_csv(self.sample_df, csv_file)
        self.assertTrue(os.path.exists(csv_file))
        
        # Test dengan ekstensi lain (tetap akan tersimpan)
        txt_file = os.path.join(self.temp_dir, "test.txt")
        save_data_csv(self.sample_df, txt_file)
        self.assertTrue(os.path.exists(txt_file))
        
        # Test tanpa ekstensi
        no_ext_file = os.path.join(self.temp_dir, "test_no_ext")
        save_data_csv(self.sample_df, no_ext_file)
        self.assertTrue(os.path.exists(no_ext_file))


if __name__ == '__main__':
    unittest.main()