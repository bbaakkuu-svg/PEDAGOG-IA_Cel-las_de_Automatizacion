import pandas as pd
import os

excel_path = r"c:\Users\LENOVO\Desktop\REPOSITORIOS\PEDAGOG-IA_Cel-las_de_Automatizacion\celula-auditor-rubricas\Registro_Evaluaciones_PedagogIA.xlsx"

if os.path.exists(excel_path):
    try:
        df = pd.read_excel(excel_path)
        print("Columns found:", df.columns.tolist())
        print("First 5 rows:")
        print(df.head())
    except Exception as e:
        print(f"Error: {e}")
else:
    print("File not found")
