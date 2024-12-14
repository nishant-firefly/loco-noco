import os
import pandas as pd
from src.config.test_config import EXCEL_FILE_PATH

class DataLoader:
    def __init__(self, file_path=None):
        self.file_path = file_path or EXCEL_FILE_PATH

    def load_data(self, sheet_name):
        try:
            return pd.read_excel(self.file_path, sheet_name=sheet_name)
        except Exception as e:
            raise RuntimeError(f"Error loading data from {self.file_path}: {e}")






# import os
# import sys
# import pandas as pd


# # Add project root to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# from src.config.test_config import EXCEL_FILE_PATH


# class DataLoader:
#     def __init__(self, file_path=None):
#         """
#         Initialize the DataLoader with a file path.
#         :param file_path: Path to the Excel file (optional, defaults to EXCEL_FILE_PATH).
#         """
#         self.file_path = file_path or EXCEL_FILE_PATH

#     def load_data(self, sheet_name):
#         """
#         Load data from a specific sheet in the Excel file.
#         :param sheet_name: Name of the sheet to load.
#         :return: Pandas DataFrame containing the sheet data.
#         """
#         try:
#             return pd.read_excel(self.file_path, sheet_name=sheet_name)
#         except Exception as e:
#             raise RuntimeError(f"Error loading data from {self.file_path}: {e}")
