from config import RAW_DATA_DIR
import pandas as pd

def load_netflix_titles() -> pd.DataFrame:
    return pd.read_csv(RAW_DATA_DIR / "netflix_titles.csv")

if __name__ == "__main__":
    print("Test load_netflix_titles()")
    print(load_netflix_titles())
    print("-"*100)