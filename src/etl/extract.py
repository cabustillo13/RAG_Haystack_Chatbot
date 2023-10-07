# + tags=["parameters"]
# declare a list tasks whose products you want to use as inputs
upstream = None


# +
import pandas as pd
import duckdb
import kaggle

# +
def extract_data(kaggle_dataset_id):
    """Extract data from Kaggle ID dataset and return a dataframe"""
    
    try:
        # Connect to Kaggle to download the database
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(kaggle_dataset_id, path='./', unzip=True)
        # Convert it into a dataframe
        df = pd.read_csv("netflix_titles.csv")
        return df
    except:
        raise Exception(f"Error retrieving data from {kaggle_dataset_id}")

# +
# write a function that saves a dataframe to duckdb
def save_to_duckdb(df, table_name, db_path):
    """Save dataframe to duckdb"""
    conn = duckdb.connect(db_path)
    conn.register('df', df)
    conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
    conn.close()

# +

if __name__ == "__main__":

    # Extract data from Kaggle ID dataset: https://www.kaggle.com/datasets/shivamb/netflix-shows
    kaggle_dataset_id = "shivamb/netflix-shows"
    df = extract_data(kaggle_dataset_id)
    
    # Save to duckdb
    db_path = "data.duckdb"
    table_name = "netflix_shows"
    save_to_duckdb(df, table_name, db_path)
