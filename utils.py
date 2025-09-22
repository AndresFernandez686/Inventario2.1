#Utilidades generales (conversiones de datos y helpers)
import pandas as pd

def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")

# Puedes agregar aquí más utilidades generales 
