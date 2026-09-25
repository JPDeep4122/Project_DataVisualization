from config import RAW_DATA_DIR
import pandas as pd

def load_netflix_titles():
    return pd.read_csv(RAW_DATA_DIR / "netflix_titles.csv")

def load_titles():
    return pd.read_csv(RAW_DATA_DIR / "titles.csv")

def load_credits():
    return pd.read_csv(RAW_DATA_DIR / "credits.csv")

def load_all_data():
    return {
        "netflix_titles": load_netflix_titles(),
        "titles": load_titles(),
        "credits": load_credits()
    }

if __name__ == "__main__":
    print("Test load_netflix_titles()")
    print(load_netflix_titles())
    print("-"*100)

    print("Test load_titles()")
    print(load_titles())
    print("-"*100)

    print("Test load_credits()")
    print(load_credits())
    print("-"*100)

    print("Test load_all_data()")
    print(load_all_data())