from espn_api.football import League
import tkinter as tk
from tkinter import simpledialog, messagebox

def analyze(league, team):
    current_week = league.current_week



def main():
    league_id = input("Please input ESPN Fantasy League ID: ")
    league_year = input("Fantasy League Year: ")
    espn_s2 = input("Paste espn_s2 Cookie: ")
    SWID = input("Paste user SWID (including curly braces): ")

    my_league = League(league_id=int(league_id), year=int(league_year), espn_s2=espn_s2, swid=SWID)
    print("League Found!")
    name = input("Please input the name of the team you want to analyze (case-sensitive): ")

    team_names = [team.team_name for team in my_league.teams]
    stripped_names = [name.strip() for name in team_names]
    try:
        team_index = stripped_names.index(name)
    except ValueError:
        print("ERROR: entered team name not found in league")

    analyze(my_league, my_league.teams[team_index])

