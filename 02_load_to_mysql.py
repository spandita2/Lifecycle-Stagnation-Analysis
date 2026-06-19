import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Force load the .env file
load_dotenv(dotenv_path='.env', override=True)

db_user = os.getenv("MYSQL_USER")
db_pass = os.getenv("MYSQL_PASSWORD")

if not db_user or not db_pass:
    print("CRITICAL ERROR: Credentials not found in .env file.")
    exit()

# Connect to MySQL and load data
engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_pass}@localhost/pocket_analytics")
df = pd.read_csv('user_ledgers.csv')
def validate_data(dataframe):
    # 1. Check for missing User IDs
    if dataframe['user_id'].isnull().any():
        raise ValueError("DATA QUALITY ALERT: Null User IDs detected. Pipeline stopped.")
    
    # 2. Check for impossible balances
    if (dataframe['current_balance'] < 0).any():
        raise ValueError("DATA QUALITY ALERT: Negative balances detected. Pipeline stopped.")
        
    print("Step 2a: Data Quality Gate PASSED. Proceeding to load.")

validate_data(df)
df.to_sql('user_ledgers', con=engine, if_exists='replace', index=False)

logging.info("Data successfully loaded into MySQL.")