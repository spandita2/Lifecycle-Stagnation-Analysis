import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)
users = [f'USER_{i:04d}' for i in range(1000)]
data = []
for user in users:
    for _ in range(np.random.randint(1, 11)):
        days_ago = np.random.randint(0, 90)
        date = datetime.now() - timedelta(days=days_ago)
        balance = np.random.randint(0, 500)
        data.append([user, balance, date])

df = pd.DataFrame(data, columns=['user_id', 'current_balance', 'timestamp'])
df.to_csv('user_ledgers.csv', index=False)
print("Step 1 Complete: user_ledgers.csv created.")