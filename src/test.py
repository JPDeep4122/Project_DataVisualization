from normalization import create_fact_monthly_addition
from config import NORMALIZED_DATA_DIR
import pandas as pd

df = create_fact_monthly_addition(pd.read_csv(NORMALIZED_DATA_DIR / "dim_title.csv"))
print(df.head())