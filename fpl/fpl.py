"""
The FPL module.

Fantasy Premier League API:
* /bootstrap-static
* /bootstrap-dynamic
* /elements
* /element-summary/{player_id}
* /entry/{user_id}
* /entry/{user_id}/cup
* /entry/{user_id}/event/{event_id}/picks
* /entry/{user_id}/history
* /entry/{user_id}/transfers
* /events
* /event/{event_id}/live
* /fixtures/?event={event_id}
* /game-settings
* /leagues-classic-standings/{league_id}
* /leagues-classic-standings/{league_id}
* /leagues-entries-and-h2h-matches/league/{league_id}
* /leagues-h2h-standings/{league_id}
* /my-team/{user_id}
* /teams
* /transfers
"""
import asyncio
import json
import os
import requests

from collections import namedtuple, defaultdict
from itertools import chain

from .constants import API_URLS
from .dictionaries.api_keywords import *
from .models.leagues import ClassicLeague, H2HLeague
from .models.fixture import Fixture
from .models.gameweek import Gameweek
from .models.player import Player, PlayerSummary, PlayerType
from .models.team import Team
from .models.user import User
from .utils import (average, fetch, get_current_user, logged_in, position_converter, scale, team_converter)

Phase = namedtuple('Phase', ['id', 'name', 'start_event', 'stop_event'])
PlayerStats = namedtuple('StatsElement', ['label', 'name'])
PointsExtrema = namedtuple('PointsExtrema', ['min', 'max'])
TeamAverage = namedtuple('TeamAverage', ['home', 'away'])

# FixtureTotalPoints = namedtuple('FixtureTotalPoints')


class GameSettings:
    def __init__(self, game_settings):
        self.cup_qualifying_method = game_settings.get(CUP_QUALIFYING_METHOD)
        self.cup_start_event_id = game_settings.get(CUP_START_EVENT_ID)
        self.cup_stop_event_id = game_settings.get(CUP_STOP_EVENT_ID)
        self.cup_type = game_settings.get(CUP_TYPE)
        self.league_h2h_tiebreak_stats = game_settings.get(LEAGUE_H2H_TIEBREAK_STATS)
        self.league_join_private_max = game_settings.get(LEAGUE_JOIN_PRIVATE_MAX)
        self.league_join_public_max = game_settings.get(LEAGUE_JOIN_PUBLIC_MAX)
        self.league_ko_first_instead_of_random = game_settings.get(LEAGUE_KO_FIRST_INSTEAD_OF_RANDOM)
        self.league_max_ko_rounds_private_h2h = game_settings.get(LEAGUE_MAX_KO_ROUNDS_PRIVATE_H2H)
        self.league_max_size_private_h2h = game_settings.get(LEAGUE_MAX_SIZE_PRIVATE_H2H)
        self.league_max_size_public_classic = game_settings.get(LEAGUE_MAX_SIZE_PUBLIC_CLASSIC)
        self.league_max_size_public_h2h = game_settings.get(LEAGUE_MAX_SIZE_PUBLIC_H2H)
        self.league_points_h2h_draw = game_settings.get(LEAGUE_POINTS_H2H_DRAW)
        self.league_points_h2h_lose = game_settings.get(LEAGUE_POINTS_H2H_LOSE)
        self.league_points_h2h_win = game_settings.get(LEAGUE_POINTS_H2H_WIN)
        self.league_prefix_public = game_settings.get(LEAGUE_PREFIX_PUBLIC)
        self.squad_squadplay = game_settings.get(SQUAD_SQUADPLAY)
        self.squad_squadsize = game_settings.get(SQUAD_SQUADSIZE)
        self.squad_team_limit = game_settings.get(SQUAD_TEAM_LIMIT)
        self.squad_total_spend = game_settings.get(SQUAD_TOTAL_SPEND)
        self.stats_form_days = game_settings.get(STATS_FORM_DAYS)
        self.sys_vice_captain_enabled = game_settings.get(SYS_VICE_CAPTAIN_ENABLED)
        self.timezone = game_settings.get(TIMEZONE)
        self.transfers_sell_on_fee = game_settings.get(TRANSFERS_SELL_ON_FEE)
        self.ui_currency_multiplier = game_settings.get(UI_CURRENCY_MULTIPLIER)
        self.ui_special_shirt_exclusions = game_settings.get(UI_SPECIAL_SHIRT_EXCLUSIONS)
        self.ui_use_special_shirts = game_settings.get(UI_USE_SPECIAL_SHIRTS)

    def __repr__(self):
        return f'GameSettings()'


class FPL:
    """The FPL class."""

    def __init__(self, session):
        self.session = session
        # TODO: use aiohttp instead
        static = requests.get(API_URLS["static"]).json()
        self.teams = {team[ID]: Team(team, self.session) for team in static.get(TEAMS)}
        self.players = {player[ID]: Player(player, self.session) for player in static.get(ELEMENTS)}
        self.total_users = static.get(TOTAL_PLAYERS)
        self.player_stats = [
            PlayerStats(label=statistic[LABEL], name=statistic[NAME])
            for statistic in static.get(ELEMENT_STATS)
        ]
        self.player_types = [PlayerType(player_type) for player_type in static.get(ELEMENT_TYPES)]
        self.settings = GameSettings(static.get(GAME_SETTINGS))
        self.phases = [
            Phase(id=phase[ID], name=phase[NAME], start_event=phase[START_EVENT], stop_event=phase[STOP_EVENT])
            for phase in static.get(PHASES)
        ]

        self.gameweeks = {}
        for event in static.get(EVENTS):
            gameweek = Gameweek(event)
            if gameweek.is_current:
                self.current_gameweek_id = gameweek.id
            self.gameweeks[gameweek.id] = gameweek

    async def get_user(self, user_id=None, return_json=False):
        """Returns the user with the given ``user_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/

        :param user_id: A user's ID.
        :type user_id: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`User` object. Defaults to ``False``.
        :type return_json: bool
        :rtype: :class:`User` or `dict`
        """
        if user_id:
            assert int(user_id) > 0, "User ID must be a positive number."
        else:
            # If no user ID provided get it from current session
            try:
                user = await get_current_user(self.session)
                user_id = user["player"]["entry"]
            except TypeError:
                raise Exception("You must log in before using `get_user` if "
                                "you do not provide a user ID.")

        user = await fetch(self.session, API_URLS[USER].format(user_id))

        if return_json:
            return user
        return User(user, session=self.session)

    async def get_player_summaries(self, *player_ids, return_json=False):
        """Returns a list of summaries of players whose ID are
        in the ``player_ids`` list.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/element-summary/1/

        :param list player_ids: A list of player IDs.
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dict``s, if ``False`` returns a list of  :class:`PlayerSummary`
            objects. Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        if player_ids:
            tasks = [
                asyncio.ensure_future(fetch(self.session, API_URLS[PLAYER].format(player_id)))
                for player_id in player_ids if player_id
            ]
            player_summaries = await asyncio.gather(*tasks)
            if return_json:
                return json.dumps(player_summaries)
            return [PlayerSummary(summary, player_id) for summary, player_id in zip(player_summaries, player_ids)]
        return []

    async def get_fixtures(self, *fixtures_ids, gameweek=0, return_json=False):
        """Returns the fixture with the given ``fixture_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/fixtures/
            https://fantasy.premierleague.com/api/fixtures/?event=1

        :param tuple fixtures_ids: The fixtures IDs. If empty, it will take all of fixtures.
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`Fixture` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`Fixture` or ``dict``
        :raises ValueError: if fixture with ``fixture_id`` not found
        """
        if not fixtures_ids:
            fixtures_ids = range(380)
        if gameweek:
            fixtures = await fetch(self.session, API_URLS[GAMEWEEK_FIXTURES].format(gameweek))
        else:
            fixtures = await fetch(self.session, API_URLS[FIXTURES])
        fixtures_list = []
        for fixture in fixtures:
            if fixture.get(ID) in fixtures_ids:
                fixtures_list.append(fixture)
        if return_json:
            return json.dumps(fixtures_list)
        return [Fixture(fixture) for fixture in fixtures_list]

    async def get_gameweek(self, gameweek_id, include_live=False, return_json=False):
        """Returns the gameweek with the ID ``gameweek_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/bootstrap-static/
            https://fantasy.premierleague.com/api/event/1/live/

        :param int gameweek_id: A gameweek's ID.
        :param bool include_live: (optional) Includes a gameweek's live data
            if ``True``.
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`Gameweek` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`Gameweek` or ``dict``
        """

        static_gameweeks = getattr(self, "events")

        try:
            static_gameweek = next(
                gameweek for gameweek in static_gameweeks.values() if
                gameweek["id"] == gameweek_id)
        except StopIteration:
            raise ValueError(f"Gameweek with ID {gameweek_id} not found")
        if include_live:
            live_gameweek = await fetch(self.session, API_URLS["gameweek_live"].format(gameweek_id))

            # Convert element list to dict
            live_gameweek["elements"] = {
                element["id"]: element for element in live_gameweek["elements"]
            }

            # Include live bonus points
            if not static_gameweek["finished"]:
                fixtures = await self.get_fixtures(gameweek=gameweek_id)
                fixtures = filter(lambda f: not f.finished, fixtures)
                bonus_for_gameweek = []

                for fixture in fixtures:
                    bonus = fixture.bonus(provisional=True)
                    bonus_for_gameweek.extend(bonus["a"] + bonus["h"])

                bonus_for_gameweek = {bonus["element"]: bonus["value"]
                                      for bonus in bonus_for_gameweek}

                for player_id, bonus_points in bonus_for_gameweek.items():
                    if live_gameweek["elements"][player_id]["stats"]["bonus"] == 0:
                        live_gameweek["elements"][player_id]["stats"]["bonus"] += bonus_points
                        live_gameweek["elements"][player_id]["stats"]["total_points"] += bonus_points
            static_gameweek.update(live_gameweek)

        if return_json:
            return static_gameweek

        return Gameweek(static_gameweek)

    async def get_classic_league(self, league_id, return_json=False):
        """Returns the classic league with the given ``league_id``. Requires
        the user to have logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-classic/967/standings/

        :param string league_id: A classic league's ID.
        :type league_id: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`ClassicLeague` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`ClassicLeague` or ``dict``
        """
        if not logged_in(self.session):
            raise Exception("User must be logged in.")

        url = API_URLS["league_classic"].format(league_id)
        league = await fetch(self.session, url)

        if return_json:
            return league

        return ClassicLeague(league, session=self.session)

    async def get_h2h_league(self, league_id, return_json=False):
        """Returns a `H2HLeague` object with the given `league_id`. Requires
        the user to have logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-h2h-matches/league/946125/

        :param league_id: A H2H league's ID.
        :type league_id: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`H2HLeague` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`H2HLeague` or ``dict``
        """
        if not logged_in(self.session):
            raise Exception("User must be logged in.")

        url = API_URLS["league_h2h"].format(league_id)
        league = await fetch(self.session, url)

        if return_json:
            return league

        return H2HLeague(league, session=self.session)

    async def login(self, email=None, password=None):
        """Returns a requests session with FPL login authentication.

        :param string email: Email address for the user's Fantasy Premier
            League account.
        :param string password: Password for the user's Fantasy Premier League
            account.
        """
        if not email and not password:
            email = os.getenv("FPL_EMAIL", None)
            password = os.getenv("FPL_PASSWORD", None)
        if not email or not password:
            raise ValueError("Email and password must be set")

        payload = {
            "login": email,
            "password": password,
            "app": "plfpl-web",
            "redirect_uri": "https://fantasy.premierleague.com/a/login"
        }

        login_url = "https://users.premierleague.com/accounts/login/"
        async with self.session.post(login_url, data=payload) as response:
            state = response.url.query["state"]
            if state == "fail":
                reason = response.url.query["reason"]
                raise ValueError(f"Login not successful, reason: {reason}")

    async def get_team_points_against(self, team_id=1):
        """Returns a dictionary containing the points scored against all teams
        in the Premier League, split by position and location.

        An example:

        .. code-block:: javascript

          {
            "away": {
                "opponent_id": {
                    "forward": 13,
                    "defender": 9,
                    "goalkeeper": 2,
                    "midfielder": 12
                    }
                ...
            },
            "home": {
                "opponent_id": {
                    "forward": 10,
                    "defender": 13,
                    "goalkeeper": 4,
                    "midfielder": 15
                    }
                ...
            }
            ...
          }

        :rtype: defaultdict
        """
        print(team_id)
        points_against = defaultdict(defaultdict)
        fixtures = await self.teams[team_id].get_team_fixtures()
        for location in fixtures.keys():
            for fixture in fixtures[location]:
                opponent_id = fixture.team_home if location == AWAY else fixture.team_away
                fixture_position_points = defaultdict(list)
                players_summaries = await self.get_player_summaries(*getattr(fixture.players, location))
                for player_summary in players_summaries:
                    position = position_converter(self.players[player_summary.player_id].element_type).lower()
                    points = player_summary.played_fixtures[fixture.id].total_points
                    fixture_position_points[position].append(points)
                points_against[location][opponent_id] = fixture_position_points
        return points_against

    def get_team_average_per_location(self, team_points_against):
        """

        """
        all_values = {AWAY: [], HOME: []}
        for location, fixtures in team_points_against.items():
            for fixture in fixtures.values():
                all_values[location].extend(chain(*fixture.values()))
        return {AWAY: average(all_values[AWAY]), HOME: average(all_values[HOME])}

    async def fdr(self):
        """Creates a new Fixture Difficulty Ranking (FDR) based on the number
        of points each team gives up to players in the Fantasy Premier League.
        These numbers are also between 1.0 and 5.0 to give a similar ranking
        system to the official FDR.

        An example:

        .. code-block:: javascript

          {
            "Man City": {
                "all": {
                "H": 4.4524439427082,
                "A": 5
                },
                "goalkeeper": {
                "H": 3.6208195949129,
                "A": 5
                },
                "defender": {
                "H": 3.747999604078,
                "A": 5
                },
                "midfielder": {
                "H": 4.6103045986504,
                "A": 5
                },
                "forward": {
                "H": 5,
                "A": 3.9363219561895
                }
            },
            ...,
            "Arsenal": {
                "all": {
                "H": 3.4414041151234,
                "A": 4.2904529162594
                },
                "goalkeeper": {
                "H": 4.1106924163919,
                "A": 4.3867595818815
                },
                "defender": {
                "H": 3.6720291204673,
                "A": 4.3380917450181
                },
                "midfielder": {
                "H": 3.3537357534825,
                "A": 4.0706443384718
                },
                "forward": {
                "H": 2.5143403441683,
                "A": 4.205298013245
                }
            }
          }

        :rtype: dict
        """

        def get_extrema(teams_averages):
            """Returns the extrema for each position and location.

            :param dict teams_averages: A dict containing the points scored
                against each team in the Premier League.
            :rtype: dict
            """
            return {
                AWAY: PointsExtrema(
                    min=min([team.away for team in teams_averages.values()]),
                    max=max([team.away for team in teams_averages.values()])
                ),
                HOME: PointsExtrema(
                    min=min([team.home for team in teams_averages.values()]),
                    max=max([team.home for team in teams_averages.values()])
                )}

        def calculate_fdr(teams_averages, extrema):
            """Returns a dict containing the FDR for each team, which is
            calculated by scaling the average points conceded per position
            between 1.0 and 5.0 using the given extrema.

            :param dict team_avg_per_position: A dict containing the points scored
                against each team in the Premier League.
            :param dict extrema: A dict containing the extrema for each
                position and location.
            :rtype: dict
            """
            fdr = {}
            for team_id, averages in teams_averages.items():
                fdr[team_converter(team_id)] = {
                    HOME: scale(averages.home, 5.0, 1.0, extrema[HOME].min, extrema[HOME].max),
                    AWAY: scale(averages.away, 5.0, 1.0, extrema[AWAY].min, extrema[AWAY].max)
                }
            return fdr
        teams_averages = {}
        for team_id in range(1, 21):
            team_points_against = await self.get_team_points_against(team_id)
            team_avg_per_position = self.get_team_average_per_location(team_points_against)
            teams_averages[team_id] = TeamAverage(home=team_avg_per_position[HOME], away=team_avg_per_position[AWAY])
        extrema = get_extrema(teams_averages)
        fdr = calculate_fdr(teams_averages, extrema)
        return fdr
