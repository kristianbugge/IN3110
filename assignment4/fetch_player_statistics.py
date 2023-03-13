import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.
    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds
    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # assert len(teams) == 8
    all_players = {}
    # Gets the player for every team and stores in dict (get_players)
    for team in teams:
        players = get_players(team['url'])
        all_players[team["name"]] = players

    # get player statistics for each player,
    # using get_player_stats

    for team, players in all_players.items():
        #print(team)
        for player in all_players[team]:
            player_stats = get_player_stats(player["url"], team)
            player.update(player_stats)
            #print(player)


    # at this point, we should have a dict of the form:
    # {
    #     "team name": [
    #         {
    #             "name": "player name",
    #             "url": "https://player_url",
    #             # added by get_player_stats
    #             "points": 5,
    #             "assists": 1.2,
    #             # ...,
    #         },
    #     ]
    # }

    #Select top 3 for each team by points:
    best_ppg = all_players
    best_apg = all_players
    best_rpg = all_players
    top_stat = [
    "points",
    "assists",
    "rebounds"
    ]
#sort after best players
    for stat in top_stat:
        if stat == "points":
            for team, players in best_ppg.items():
                best_ppg[team].sort(reverse = True, key=sortPPG)
        if stat == "assists":
            for team, players in best_apg.items():
                best_apg[team].sort(reverse = True, key=sortAPG)

        if stat == "rebounds":
            for team, players in best_rpg.items():
                best_rpg[team].sort(reverse = True, key=sortRPG)

#shorten the lists to 3 players
#for some reason this gives me the wrong plaeyrs, not sure why?
#the orders are correct after sorting, but wrong after shortening the lists
    desired_size = 3
    for team1, players in best_ppg.items():
        n = len(best_ppg[team1])
        for i in range(0, n - desired_size):
            best_ppg[team1].pop()

    for team2, players in best_apg.items():
        n = len(best_apg[team2])
        for i in range(0, n - desired_size):
            best_apg[team2].pop()

    for team3, players in best_rpg.items():
        n = len(best_rpg[team3])
        for i in range(0, n - desired_size):
            best_rpg[team3].pop()


    plot_best(best_ppg, "points")
    plot_best(best_apg, "assists")
    plot_best(best_rpg, "rebounds")


def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plots a single stat for the top 3 players from every team.
    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:
            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }
            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.
        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    colors = {
    "Phoenix": 'b',
    "Dallas": 'g',
    "Golden State": 'r',
    "Memphis": 'c',
    "Milwaukee": 'm',
    "Miami": 'y',
    "Boston": 'b',
    "Philadelphia": 'tan',
    }
    stats_dir = "NBA_player_statistics"
    print("Plotting...")
    plt.clf()
    all_names = []
    #because shorting list did not give desired result we try this instead
    i = 0

    for team, players in best.items():
        color = colors[team]
        points = []
        names = []
        for player in best[team]:
            names.append(player["name"])
            points.append(player[stat])
        all_names.extend(names)

        x = range(i, i + len(names))
        i += len(names)

        bars = plt.bar(x, points, color = color, label = team)

    plt.xticks(range(len(all_names)), all_names, rotation = 90)
    plt.legend(bbox_to_anchor = (1.05, 0.6))

    if stat == "points":
        plt.title("Points per game")
    elif stat == "assits":
        plt.title("Assists per game")
    else:
        plt.title("Rebounds per game")
    isExist = os.path.exists(stats_dir)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(stats_dir)
    plt.tight_layout()
    plt.savefig(stats_dir + "/" + stat + ".png")
    print("Finished plotting")

def get_teams(url: str) -> list:
    """Extracts all the teams that were in the semi finals in nba
    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure
        # print([c.get_text(strip=True) for c in cols])

        # TODO:
        # 1. if First Round column, record team link from `a` tag
        # 2. if semifinal column, record team name

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Gets all the players from a team that were in the roster for semi finals
    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    # Get the table
    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table_head = soup.find(id = "Roster")
    table = table_head.find_next("table", {"class": "sortable"})

    players = []
    # Loop over every row and get the names from roster
    rows = table.find_all("tr")
    rows = rows[1:]
    for row in rows:
        # Get the columns
        cols = row.find_all("td")
        cell = cols[2]
        url = cell.find('a')["href"]
        name = cell.getText().strip("\n")
        # find name links (a tags)
        # and add to players a dict with
        # {'name':, 'url':}
        players.append({'name': name, 'url': base_url + url})

    # return list of players

    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Gets the player stats for a player in a given team
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    #print(f"Fetching stats for player in {player_url}")

    stats = {
    "points": 0.0,
    "assists": 0.0,
    "rebounds": 0.0
    }

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")
    nba_header = soup.find(id = "NBA")
    #making sure we find the regular season scoring table:
    try:
        season_header = nba_header.find_next(id = "Regular_season")
        table = season_header.find_next("table")
    except:
        try:
            table = nba_header.find_next("table")
        except:
            print(f"Could not retrieve stats on {player_url}")
            return stats
    table_headers = table.find_all("th")
    table_i = {}
    i = 0
    for head in table_headers:
        text = head.get_text(strip = True)
        table_i[text] = i
        i += 1

    out_row = None
    rows = table.find_all("tr")
    year = r"2021–22"
    team_pattern = f"{team}"
    for row in rows:
        text = row.get_text(strip = True)
        #Finding correct row
        match = re.search(year, text)
        if match:
            match2 = re.search(team_pattern, text)
            #check team
            if match2:
                out_row = row
    if out_row:
        out_row = out_row.find_all("td")
    else:
        return stats

    #getting the columns of scores that we want
    ppgc = out_row[table_i.get('PPG')]
    apgc = out_row[table_i.get('APG')]
    rpgc = out_row[table_i.get('RPG')]

    ppg = ppgc.get_text(strip = True)
    apg = apgc.get_text(strip = True)
    rpg = rpgc.get_text(strip = True)

    try:
        stats["points"] = float(ppg)
    except:
        stats["points"] = 0.0
    try:
        stats["assists"] = float(apg)
    except:
        stats["assists"]  = 0.0
    try:
        stats["rebounds"] = float(rpg)
    except:
        stats["rebounds"] = 0.0

    return stats

#helper functions to help sort lists of players by scores

def sortPPG(e):
    return e['points']

def sortAPG(e):
    return e['assists']

def sortRPG(e):
    return e['rebounds']

# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
