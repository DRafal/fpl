from collections import namedtuple, defaultdict
from itertools import chain

from ..dictionaries.api_keywords import *
from ..utils import team_converter
from .player import Player

FixturePlayers = namedtuple('FixturePlayers', ['home', 'away'])
PlayerEvent = namedtuple('PlayerEvent', ['player_id', 'value', 'team'])

EMPTY_FIXTURE_PLAYERS = FixturePlayers(home=[], away=[])


# noinspection PyUnresolvedReferences
class Fixture:
    """A class representing fixtures in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         fixture = await fpl.get_fixture(1)
      ...     print(fixture)
      ...
      >>> asyncio.run(main())
      Arsenal vs. Man City - 10 Aug 19:00
    """

    def __init__(self, fixture_information):
        self.code = fixture_information.get(CODE)
        self.event = fixture_information.get(EVENT)
        self.finished = fixture_information.get(FINISHED)
        self.finished_provisional = fixture_information.get(FINISHED_PROVISIONAL)
        self.id = fixture_information.get(ID)
        self.kickoff_time = fixture_information.get(KICKOFF_TIME)
        self.minutes = fixture_information.get(MINUTES)
        self.provisional_start_time = fixture_information.get(PROVISIONAL_START_TIME)
        self.started = fixture_information.get(STARTED)
        self.team_away = fixture_information.get(TEAM_AWAY)
        self.team_away_difficulty = fixture_information.get(TEAM_AWAY_DIFFICULTY)
        self.team_away_score = fixture_information.get(TEAM_AWAY_SCORE)
        self.team_home = fixture_information.get(TEAM_HOME)
        self.team_home_difficulty = fixture_information.get(TEAM_HOME_DIFFICULTY)
        self.team_home_score = fixture_information.get(TEAM_HOME_SCORE)
        self.stats = {}
        for factor in fixture_information[STATS]:
            home_players = [PlayerEvent(
                player_id=player[ELEMENT],
                value=player[VALUE],
                team=self.team_home
            ) for player in factor[H]]
            away_players = [PlayerEvent(
                player_id=player[ELEMENT],
                value=player[VALUE],
                team=self.team_away
            ) for player in factor[A]]
            self.stats[factor[IDENTIFIER]] = FixturePlayers(home=home_players, away=away_players)

    def __repr__(self):
        return (f'Fixture({team_converter(self.team_home)} vs. '
                f'{team_converter(self.team_away)} - '
                f'{self.kickoff_time})')

    def __str__(self):
        return (f"{team_converter(self.team_home)} vs. "
                f"{team_converter(self.team_away)} - "
                f"{self.kickoff_time}")

    @property
    def goalscorers(self):
        """Returns all players who scored in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(GOALS_SCORED, EMPTY_FIXTURE_PLAYERS)

    @property
    def assisters(self):
        """Returns all players who made an assist in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(ASSISTS, EMPTY_FIXTURE_PLAYERS)

    @property
    def own_goalscorers(self):
        """Returns all players who scored an own goal in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(OWN_GOALS, EMPTY_FIXTURE_PLAYERS)

    @property
    def yellow_cards(self):
        """Returns all players who received a yellow card in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(YELLOW_CARDS, EMPTY_FIXTURE_PLAYERS)

    @property
    def red_cards(self):
        """Returns all players who received a red card in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(RED_CARDS, EMPTY_FIXTURE_PLAYERS)

    @property
    def penalty_saves(self):
        """Returns all players who saved a penalty in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(PENALTIES_SAVED, EMPTY_FIXTURE_PLAYERS)

    @property
    def penalty_misses(self):
        """Returns all players who missed a penalty in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(PENALTIES_MISSED, EMPTY_FIXTURE_PLAYERS)

    @property
    def saves(self):
        """Returns all players who made a save in the fixture.

        :rtype: namedtuple
        """
        return self.stats.get(SAVES, EMPTY_FIXTURE_PLAYERS)

    @property
    def bps(self):
        """Returns the bonus points of each player.
        :rtype: namedtuple
        """
        return self.stats.get(BPS, EMPTY_FIXTURE_PLAYERS)

    @property
    def players(self):
        """Returns ids of all players involved in the match
        :rtype: namedtuple
        """
        return FixturePlayers(
            home=[player.player_id for player in self.bps.home],
            away=[player.player_id for player in self.bps.away]
        )

    def bonus(self, provisional=False):
        """Returns all players who received bonus points in the fixture.

        :rtype: namedtuple
        """
        if self.finished:
            return self.stats[BONUS]
        elif self.started and provisional:
            players = chain(self.stats[BPS].home, self.stats[BPS].away)
            players_points = defaultdict(list)
            for player in players:
                players_points[player.value].append(player)

            points = sorted([point for point in players_points], reverse=True)

            home_players = []
            away_players = []

            points_to_bonus = 3
            for point in points:
                bonus_players = players_points[point]
                for player in bonus_players:
                    _player = PlayerEvent(player_id=player.player_id, value=points_to_bonus, team=player.team)
                    if _player.team == self.team_home:
                        home_players.append(_player)
                    else:
                        away_players.append(_player)
                points_to_bonus -= len(bonus_players)
                if points_to_bonus <= 0:
                    break

            return FixturePlayers(home=home_players, away=away_players)
        return EMPTY_FIXTURE_PLAYERS


def add_player(location, information):
    """Appends player to the location list."""
    player = Player(information[ELEMENT])
    goals = information[VALUE]
    location.append({PLAYER: player, GOALS: goals})
