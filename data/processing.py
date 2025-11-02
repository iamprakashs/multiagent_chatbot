import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import os


class DataProcessor:
    """Process and prepare data for ingestion into vector database"""
    
    def __init__(self, input_dir: str = ".", output_dir: str = "data"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def combine_text_columns(self, df: pd.DataFrame, text_columns: List[str], separator: str = " | ") -> pd.Series:
        """Combine multiple columns into a single text column"""
        combined_text = df[text_columns[0]].astype(str)
        for col in text_columns[1:]:
            combined_text = combined_text + separator + df[col].astype(str)
        return combined_text
    
    def prepare_property_data(self, csv_file: str = "property_data.csv", max_rows: int = 1000) -> pd.DataFrame:
        """Process property data and create text content for embedding (in-memory only)"""
        input_file = self.input_dir / csv_file
        
        if not input_file.exists():
            raise FileNotFoundError(f"File {input_file} not found")
        
        print(f"Loading first {max_rows} rows from {csv_file}...")
        df = pd.read_csv(input_file, nrows=max_rows)
        
        text_columns = [col for col in df.columns if df[col].dtype == 'object']
        available_columns = [col for col in text_columns if col in df.columns]
        
        if not available_columns:
            raise ValueError(f"None of the expected columns found: {text_columns}")
        
        df['text_content'] = self.combine_text_columns(df, available_columns)
        
        print(f"Processed {len(df)} records in memory")
        print(f"Text columns used: {available_columns}")
        
        return df
    
    def clean_text_data(self, text: str) -> str:
        """Clean and normalize text data"""
        if pd.isna(text):
            return ""
        
        text = str(text).strip()
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())
        
        return text
    
    def validate_processed_data(self, file_path: str) -> Dict[str, Any]:
        """Validate the processed data file"""
        df = pd.read_csv(file_path)
        
        validation_report = {
            'total_records': len(df),
            'has_text_content': 'text_content' in df.columns,
            'empty_text_records': df['text_content'].isna().sum() if 'text_content' in df.columns else 0,
            'columns': list(df.columns),
            'sample_text': df['text_content'].iloc[0] if 'text_content' in df.columns and len(df) > 0 else None
        }
        
        return validation_report