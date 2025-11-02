import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import os


class DataLoader:
    """Load and manage data files for vector database ingestion"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.supported_formats = ['.csv', '.xlsx', '.xls']
    
    def list_data_files(self) -> List[str]:
        """List all supported data files in the data directory"""
        files = []
        for ext in self.supported_formats:
            files.extend([str(f) for f in self.data_dir.glob(f"*{ext}")])
        return files
    
    def load_csv(self, file_path: str, encoding: str = 'utf-8', max_rows: int = None) -> pd.DataFrame:
        """Load CSV file with error handling and optional row limit"""
        try:
            df = pd.read_csv(file_path, encoding=encoding, nrows=max_rows)
            print(f"Successfully loaded {len(df)} records from {file_path}")
            return df
        except UnicodeDecodeError:
            print(f"UTF-8 encoding failed, trying latin-1 for {file_path}")
            df = pd.read_csv(file_path, encoding='latin-1', nrows=max_rows)
            print(f"Successfully loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            raise
    
    def load_excel(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """Load Excel file with error handling"""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Successfully loaded {len(df)} records from {file_path}")
            return df
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            raise
    
    def load_file(self, file_path: str, max_rows: int = None) -> pd.DataFrame:
        """Load file based on extension with optional row limit"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} not found")
        
        if file_path.suffix.lower() == '.csv':
            return self.load_csv(str(file_path), max_rows=max_rows)
        elif file_path.suffix.lower() in ['.xlsx', '.xls']:
            return self.load_excel(str(file_path))
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get information about a data file"""
        df = self.load_file(file_path)
        
        info = {
            'file_path': str(file_path),
            'file_size_mb': round(Path(file_path).stat().st_size / (1024 * 1024), 2),
            'total_records': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'memory_usage_mb': round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
            'null_counts': df.isnull().sum().to_dict(),
            'sample_data': df.head(3).to_dict('records')
        }
        
        return info
    
    def convert_to_documents(self, df: pd.DataFrame, text_column: str = 'text_content') -> List[Dict[str, Any]]:
        """Convert DataFrame to list of documents for vector database"""
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in DataFrame")
        
        documents = []
        for idx, row in df.iterrows():
            doc = {
                'text': str(row[text_column]),
                'id': idx,
                'metadata': {}
            }
            
            for col in df.columns:
                if col != text_column:
                    doc['metadata'][col] = row[col]
            
            documents.append(doc)
        
        return documents
    
    def preview_data(self, file_path: str, num_rows: int = 5) -> None:
        """Preview data from file"""
        df = self.load_file(file_path)
        
        print(f"\nFile: {file_path}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\nFirst few rows:")
        print(df.head(num_rows).to_string())
        
        if 'text_content' in df.columns:
            print(f"\nSample text content:")
            print(f"'{df['text_content'].iloc[0][:200]}...'")
    
    def search_files_by_pattern(self, pattern: str) -> List[str]:
        """Search for files matching a pattern"""
        matching_files = []
        for ext in self.supported_formats:
            matching_files.extend([str(f) for f in self.data_dir.glob(f"*{pattern}*{ext}")])
        return matching_files