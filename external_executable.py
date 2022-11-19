import requests
import sys
import pandas as pd
from datetime import datetime


def clean_response(res):
    data = res.text.split('\n')
    data = [d.split(',')[1:] for d in data if d != '']
    columns = data[0]
    data = data[1:]
    df = pd.DataFrame(data, columns=columns)
    return df


def prob_from_elo(elo):
    """
    The probability formula is taken from http://www.eloratings.net/about
    """
    return 1/(10**(-elo/400) + 1)

if len(sys.argv) != 3:
    raise ValueError("Expected 2 command line arguments.")

club_1 = sys.argv[1]
club_2 = sys.argv[2]

now = datetime.now().strftime("%Y-%m-%d")
api_url = "http://api.clubelo.com"

url = f"{api_url}/{now}"

res = requests.get(url)
if res.status_code == 200:
    df = clean_response(res)
# else Raise some exception...

team_1_elo = float(df[df['Club'].str.lower() == club_1.lower()]['Elo'].iloc[0])
team_2_elo = float(df[df['Club'].str.lower() == club_2.lower()]['Elo'].iloc[0])

if team_1_elo == team_2_elo:
    print(f"{club_1} is equally likely to win as {club_2}.")
elif team_1_elo > team_2_elo:
    p = prob_from_elo(team_1_elo - team_2_elo)
    print(f"{club_1} has probability {p:.3f} of winning against {club_2}.")
elif team_2_elo > team_1_elo:
    p = prob_from_elo(team_2_elo - team_1_elo)
    print(f"{club_2} has probability {p:.3f} of winning against {club_1}.")

