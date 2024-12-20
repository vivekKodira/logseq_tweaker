import unittest
from folder_reader import read_files_in_folder
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

class TestFolderReader(unittest.TestCase):
    
    @patch('folder_reader.Path')
    def test_read_files_in_folder_valid_directory(self, mock_path):
        mock_file1 = MagicMock()
        mock_file2 = MagicMock()
        mock_file1.name = 'file1.txt'
        mock_file2.name = 'file2.txt'
        
        mock_path.return_value.is_dir.return_value = True
        mock_path.return_value.iterdir.return_value = [mock_file1, mock_file2]
        mock_file1.is_file.return_value = True
        mock_file2.is_file.return_value = True

        with patch('builtins.open', mock_open(read_data='file content')):
            result = read_files_in_folder('/path/to/valid/folder')
            self.assertEqual(result, {'file1.txt': 'file content', 'file2.txt': 'file content'})

    @patch('folder_reader.Path')
    def test_read_files_in_folder_invalid_directory(self, mock_path):
        mock_path.return_value.is_dir.return_value = False
        with self.assertRaises(ValueError):
            read_files_in_folder('/path/to/invalid/folder')

    @patch('folder_reader.Path')
    def test_read_files_in_folder_empty_directory(self, mock_path):
        mock_path.return_value.is_dir.return_value = True
        mock_path.return_value.iterdir.return_value = []
        result = read_files_in_folder('/path/to/empty/folder')
        self.assertEqual(result, {})

    @patch('folder_reader.Path')
    def test_read_files_in_folder_with_read_error(self, mock_path):
        mock_path.return_value.is_dir.return_value = True
        mock_path.return_value.iterdir.return_value = [
            mock_path.return_value / 'file1.txt'
        ]
        mock_path.return_value.is_file.side_effect = lambda: True

        with patch('builtins.open', mock_open(read_data='file content')) as mock_file:
            mock_file.side_effect = Exception("Read error")
            result = read_files_in_folder('/path/to/folder/with/read/error')
            self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()