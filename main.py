#program assumes standard league rules are implemented 
from espn_api.football import League
from flask import Flask, render_template, request

app = Flask(__name__)

BYE_WEEKS = {
    "BAL": 7, "BUF": 7, "CIN": 10, "CLE": 9, "DEN": 12, "HOU": 6, 
    "KC": 10, "LAC": 12, "LV": 8, "NE": 14, "NYJ": 9, "PIT": 5, 
    "TEN": 10, "IND": 11, "MIA": 12, "JAX": 8, "DAL": 10, 
    "NYG": 14, "PHI": 9, "WSH": 12, "CHI": 5, "DET": 8, "GB": 5, 
    "MIN": 6, "ATL": 5, "CAR": 14, "NO": 11, "TB": 9, "ARI": 8, 
    "LAR": 8, "SF": 14, "SEA": 8 
}

def message(team, current_week):
    owner = team.owners[0]
    owner_name = owner.get("lastName", "!")
    return f"Welcome Coach {owner_name}! Here is your team data for week {current_week}."

def analyze(league, team, current_week):
    eligible_players = []
    ineligible_players = []
    roster = []
    warnings = []
    bench = []

    for player in team.roster:
        week_stats = player.stats.get(current_week, {})
        projected = week_stats.get("projected_points", 0)  # default 0 if missing
        player.weekly_projection = projected

        if BYE_WEEKS.get(player.proTeam) == current_week:
            ineligible_players.append(player + "on bye: Week" + current_week)
            bench.append(player)
            continue

        if player.injuryStatus not in ["ACTIVE", "NORMAL"]:
            if player.injuryStatus == "QUESTIONABLE":
                 ineligible_players.append(f"{player.name} has injury status: {player.injuryStatus}. "
                                           "Reconsider adding to roster later in week and monitor injury status!")
            else:
                ineligible_players.append(f"{player.name} has injury status: {player.injuryStatus}. ")
            bench.append(player)
            continue

        eligible_players.append(player)

    eligible_players.sort(key=lambda p: p.weekly_projection, reverse=True)

    spots = {
        "QB": 1,
        "RB": 2,
        "WR": 2,
        "TE": 1,
        "K": 1,
        "D/ST": 1,
        "FLEX": 1
    }

    for player in eligible_players:
        pos = player.position
        if pos in spots and spots[pos] > 0:
            spots[player.position] -= 1
            roster.append(player)
        elif pos in ["RB", "WR", "TE"] and spots["FLEX"] > 0:
            spots["FLEX"] -= 1
            roster.append(player)
        else:
            bench.append(player)

    for slot, remaining in spots.items():
        if remaining > 0:
            warnings.append(f"⚠️ Missing {remaining} {slot} spot(s)")

    return roster, warnings, bench, ineligible_players



@app.route("/", methods=["GET", "POST"])
def index():
    error = ""
    roster = []
    warnings = []
    bench = []
    ineligible = []
    welcome = ""

    if request.method == "POST":
        league_id = int(request.form["league_id"])
        espn_s2 = request.form["espn_s2"]
        swid = request.form["swid"]

        my_league = League(league_id=int(league_id), year=2025, espn_s2=espn_s2, swid=swid)

        name = request.form["team_name"]

        team_names = [team.team_name for team in my_league.teams]
        stripped_names = [name.strip() for name in team_names]
        try:
            team_index = stripped_names.index(name)
            my_team = my_league.teams[team_index]
            current_week = my_league.current_week
            welcome = message(my_team, current_week)
            roster, warnings, bench, ineligible = analyze(my_league, my_team, current_week)
        except ValueError:
            error = "ERROR: entered team name not found in league"
    return render_template("index.html", welcome=welcome, error=error, roster=roster, warnings=warnings, bench=bench, ineligible=ineligible)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
