import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Force load the .env file
load_dotenv(dotenv_path='.env', override=True)

db_user = os.getenv("MYSQL_USER")
db_pass = os.getenv("MYSQL_PASSWORD")

# Connect to MySQL
engine = create_engine(f"mysql+mysqlconnector://{db_user}:{db_pass}@localhost/pocket_analytics")

# Execute the segmentation logic
query = """
SELECT 
    user_id,
    MAX(timestamp) as last_interaction,
    SUM(current_balance) as total_stored_value,
    DATEDIFF(NOW(), MAX(timestamp)) as days_since_last_use,
    CASE 
        WHEN DATEDIFF(NOW(), MAX(timestamp)) > 30 THEN 'High-Risk Stagnant'
        WHEN DATEDIFF(NOW(), MAX(timestamp)) > 14 THEN 'At-Risk'
        ELSE 'Healthy Idle'
    END as status,
    -- THE UPGRADE: Rank users by how much money is sitting idle
    RANK() OVER(ORDER BY SUM(current_balance) DESC) as financial_risk_rank
FROM user_ledgers
GROUP BY user_id
HAVING total_stored_value > 0
ORDER BY financial_risk_rank ASC;
"""

df_result = pd.read_sql_query(query, engine)
df_result.to_csv('final_segmentation.csv', index=False)

print("Step 3: Analysis complete. Results saved to final_segmentation.csv")