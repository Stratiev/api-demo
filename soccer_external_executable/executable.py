import pandas as pd
import sys

def prob_from_elo(elo):
    """
    The probability formula is taken from http://www.eloratings.net/about
    """
    return 1/(10**(-elo/400) + 1)

if len(sys.argv) != 3:
    raise ValueError("Expected 2 command line arguments.")

club_1 = sys.argv[1]
club_2 = sys.argv[2]

df = pd.read_csv("club_elo.csv")

team_1_elo = df[df['Club'].str.lower() == club_1.lower()]['Elo'].iloc[0]
team_2_elo = df[df['Club'].str.lower() == club_2.lower()]['Elo'].iloc[0]

if team_1_elo == team_2_elo:
    print(f"{club_1} is equally likely to win as {club_2}.")
elif team_1_elo > team_2_elo:
    p = prob_from_elo(team_1_elo - team_2_elo)
    print(f"{club_1} has probability {p:.3f} of winning against {club_2}.")
elif team_2_elo > team_1_elo:
    p = prob_from_elo(team_2_elo - team_1_elo)
    print(f"{club_2} has probability {p:.3f} of winning against {club_1}.")

