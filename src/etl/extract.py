# + tags=["parameters"]
# declare a list tasks whose products you want to use as inputs
upstream = None


# +
import requests 
import pandas as pd
import json
import duckdb

# +
def extract_data(url):
    """Extract data from URL and return a dataframe"""
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(json.loads(response.content))
    else:
        raise Exception(f"Error retrieving data from {url}")

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

    # Extract data from URL
    url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
    df = extract_data(url)
    
    # Save to duckdb
    db_path = "data.duckdb"
    table_name = "nycitydata"
    save_to_duckdb(df, table_name, db_path)

