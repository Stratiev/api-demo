import sys
from utils import clean_response, prob_from_elo, get_latest_soccer_data


if len(sys.argv) != 3:
    raise ValueError("Expected 2 command line arguments.")


df = get_latest_soccer_data()
clubs = df['Club'].str.lower().unique().tolist()

club_1 = sys.argv[1]
club_2 = sys.argv[2]

if not club_1.lower() in clubs:
    raise ValueError(f"{club_1} not in the list of available club names.")
if not club_2.lower() in clubs:
    raise ValueError(f"{club_2} not in the list of available club names.")
    


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
