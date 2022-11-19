import pandas as pd
import requests
import json
from datetime import datetime

def clean_response(res):
    data = res.text.split('\n')
    data = [d.split(',')[1:] for d in data if d != '']
    columns = data[0]
    data = data[1:]
    df = pd.DataFrame(data, columns=columns)
    return df


now = datetime.now().strftime("%Y-%m-%d")
api_url = "http://api.clubelo.com"

url = f"{api_url}/{now}"

res = requests.get(url)
if res.status_code == 200:
    df = clean_response(res)
    df.to_csv("club_elo.csv", index=False)
# Raise some exception...
