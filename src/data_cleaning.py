from pathlib import Path
import pandas as pd

def get_project_root() -> Path:
    """Find the project root directory."""
    # If running from src/, root is parent
    current_file = Path(__file__).resolve()
    for parent in [current_file.parent, current_file.parent.parent]:
        if (parent / "data").exists():
            return parent
    return Path.cwd()

def clean_uac_data(raw_path=None, processed_path=None) -> pd.DataFrame:
    """
    Cleans the raw HHS Unaccompanied Alien Children (UAC) Program dataset:
    1. Handles dynamic file paths so FileNotFoundError never occurs.
    2. Drops empty/blank rows (NaNs from trailing lines).
    3. Standardizes column names to clean snake_case.
    4. Strips commas from numeric fields and converts them to integers.
    5. Parses string dates into datetime objects and sorts chronologically.
    6. Adds daily flow and calendar metrics.
    7. Saves clean dataset to data/processed.
    """
    project_root = get_project_root()

    if raw_path is None:
        # Search candidate paths to avoid FileNotFoundError
        candidates = [
            project_root / "data" / "raw" / "HHS_Unaccompanied_Alien_Children_Program.csv",
            Path.cwd() / "data" / "raw" / "HHS_Unaccompanied_Alien_Children_Program.csv",
            Path.cwd() / "HHS_Unaccompanied_Alien_Children_Program.csv",
            Path.home() / "Downloads" / "HHS_Unaccompanied_Alien_Children_Program.csv"
        ]
        for candidate in candidates:
            if candidate.exists():
                raw_path = candidate
                break
        if raw_path is None:
            raw_path = candidates[0]

    raw_path = Path(raw_path)
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Could not locate the raw dataset at '{raw_path}'.\n"
            f"Please place 'HHS_Unaccompanied_Alien_Children_Program.csv' in '{project_root / 'data' / 'raw'}'."
        )

    if processed_path is None:
        processed_path = project_root / "data" / "processed" / "uac_care_cleaned.csv"
    else:
        processed_path = Path(processed_path)

    print(f"Loading raw data from: {raw_path}")
    df = pd.read_csv(raw_path)

    # 1. Drop completely empty rows
    df = df.dropna(how="all").copy()

    # 2. Rename columns to clean, standardized snake_case
    column_mapping = {
        "Date": "date",
        "Children apprehended and placed in CBP custody*": "cbp_apprehended",
        "Children in CBP custody": "cbp_in_custody",
        "Children transferred out of CBP custody": "cbp_transferred_out",
        "Children in HHS Care": "hhs_in_care",
        "Children discharged from HHS Care": "hhs_discharged"
    }
    
    df.columns = df.columns.str.strip()
    df = df.rename(columns=column_mapping)

    # 3. Clean numeric fields (handling comma-separated numbers like '2,484')
    numeric_cols = ["cbp_apprehended", "cbp_in_custody", "cbp_transferred_out", "hhs_in_care", "hhs_discharged"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # 4. Parse Date and sort chronologically (oldest -> newest)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    # 5. Feature Engineering
    df["hhs_net_daily_change"] = df["cbp_transferred_out"] - df["hhs_discharged"]
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.day_name()

    # 6. Save to processed directory
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(processed_path, index=False)
    print(f"Cleaned dataset successfully saved to: {processed_path} ({len(df)} records).")

    return df

if __name__ == "__main__":
    clean_uac_data()
