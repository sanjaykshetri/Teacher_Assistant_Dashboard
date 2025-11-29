#!/usr/bin/env python3
"""
Excel to CSV Converter
Quickly convert Excel templates to CSV files for the dashboard
"""

import pandas as pd
import os
import sys
from pathlib import Path

def convert_excel_to_csv(excel_file, csv_file=None):
    """Convert an Excel file to CSV"""
    try:
        # Read Excel file
        df = pd.read_excel(excel_file)
        
        # Remove instruction rows if present (row with italicized hints)
        # Typically these are empty or have descriptive text
        if len(df) > 0 and df.iloc[0].astype(str).str.contains('Enter|e.g.|Optional').any():
            df = df.iloc[1:].reset_index(drop=True)
        
        # Determine output filename
        if csv_file is None:
            # Auto-generate CSV filename in data/ folder
            base_name = Path(excel_file).stem.replace('_template', '')
            csv_file = f'data/{base_name}.csv'
        
        # Save to CSV
        df.to_csv(csv_file, index=False)
        
        print(f"✅ Converted: {excel_file}")
        print(f"   → Saved to: {csv_file}")
        print(f"   → {len(df)} rows")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {excel_file}: {e}")
        return False

def main():
    print("="*60)
    print("📊 Excel to CSV Converter")
    print("="*60)
    
    if len(sys.argv) > 1:
        # Convert specific file(s) provided as arguments
        excel_files = sys.argv[1:]
        success_count = 0
        
        for excel_file in excel_files:
            if not os.path.exists(excel_file):
                print(f"❌ File not found: {excel_file}")
                continue
            
            if convert_excel_to_csv(excel_file):
                success_count += 1
        
        print("="*60)
        print(f"✅ Converted {success_count} of {len(excel_files)} files")
        
    else:
        # Interactive mode - search for Excel files
        print("\nSearching for Excel files in data/templates/...")
        
        template_dir = 'data/templates'
        if not os.path.exists(template_dir):
            print(f"❌ Template directory not found: {template_dir}")
            return
        
        excel_files = list(Path(template_dir).glob('*.xlsx'))
        
        if not excel_files:
            print("❌ No Excel files found in data/templates/")
            return
        
        print(f"\nFound {len(excel_files)} template(s):")
        for i, f in enumerate(excel_files, 1):
            print(f"  {i}. {f.name}")
        
        print("\nOptions:")
        print("  - Enter numbers (comma-separated): 1,3,4")
        print("  - Enter 'all' to convert all")
        print("  - Enter 'q' to quit")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("Cancelled.")
            return
        
        if choice == 'all':
            files_to_convert = excel_files
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                files_to_convert = [excel_files[i] for i in indices if 0 <= i < len(excel_files)]
            except (ValueError, IndexError):
                print("❌ Invalid selection")
                return
        
        print()
        success_count = 0
        for excel_file in files_to_convert:
            if convert_excel_to_csv(str(excel_file)):
                success_count += 1
            print()
        
        print("="*60)
        print(f"✅ Converted {success_count} of {len(files_to_convert)} files")
        print("\n💡 Don't forget to run: python utils/data_validator.py")
        print("="*60)

if __name__ == "__main__":
    main()
