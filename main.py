from espn_api.football import League
from flask import Flask, render_template, request

app = Flask(__name__)

def analyze(league, team):
    current_week = league.current_week


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    if request.method == "POST":
        league_id = int(request.form["league_id"])
        league_year = int(request.form["league_year"])
        espn_s2 = request.form["espn_s2"]
        swid = request.form["swid"]

        my_league = League(league_id=int(league_id), year=int(league_year), espn_s2=espn_s2, swid=swid)

        name = request.form["team_name"]

        team_names = [team.team_name for team in my_league.teams]
        stripped_names = [name.strip() for name in team_names]
        try:
            team_index = stripped_names.index(name)
            team = my_league.teams[team_index]
            result = f"Team '{team.team_name}' found!"
        except ValueError:
            error = "ERROR: entered team name not found in league"
    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
