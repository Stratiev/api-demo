import requests
import pandas as pd
from datetime import datetime

def clean_response(res):
    data = res.text.split('\n')
    data = [d.split(',')[1:] for d in data if d != '']
    columns = data[0]
    data = data[1:]
    df = pd.DataFrame(data, columns=columns)
    return df

def prob_from_elo(elo_difference):
    """
    The probability formula is taken from http://www.eloratings.net/about
    """
    return 1/(10**(-elo_difference/400) + 1)

def get_latest_soccer_data():
    now = datetime.now().strftime("%Y-%m-%d")
    api_url = "http://api.clubelo.com"

    url = f"{api_url}/{now}"

    res = requests.get(url)
    if res.status_code == 200:
        df = clean_response(res)
    else:
        raise ValueError(f"Failed to fetch data. Status code {res.status_code}.")
    return df
