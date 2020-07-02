from collections import defaultdict
from typing import List

from ..constants import API_URLS
from ..dictionaries.api_keywords import *
from ..utils import fetch
from .player import Player
from .fixture import Fixture


class Team:
    """A class representing a real team in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         team = await fpl.get_team(14)
      ...     print(team)
      ...
      >>> asyncio.run(main())
      Man Utd
    """

    def __init__(self, team_information, session):
        self._session = session
        self.code = team_information.get(CODE)
        self.draw = team_information.get(DRAW)
        self.form = team_information.get(FORM)
        self.id = team_information.get(ID)
        self.loss = team_information.get(LOSS)
        self.name = team_information.get(NAME)
        self.played = team_information.get(PLAYED)
        self.points = team_information.get(POINTS)
        self.position = team_information.get(POSITION)
        self.pulse_id = team_information.get(PULSE_ID)
        self.short_name = team_information.get(SHORT_NAME)
        self.strength = team_information.get(STRENGTH)
        self.strength_attack_away = team_information.get(STRENGTH_ATTACK_AWAY)
        self.strength_attack_home = team_information.get(STRENGTH_ATTACK_HOME)
        self.strength_defence_away = team_information.get(STRENGTH_DEFENCE_AWAY)
        self.strength_defence_home = team_information.get(STRENGTH_DEFENCE_HOME)
        self.strength_overall_away = team_information.get(STRENGTH_OVERALL_AWAY)
        self.strength_overall_home = team_information.get(STRENGTH_OVERALL_HOME)
        self.team_division = team_information.get(TEAM_DIVISION)
        self.unavailable = team_information.get(UNAVAILABLE)
        self.win = team_information.get(WIN)

    def __repr__(self):
        return f'Team(id={self.id}, name={self.name}, code={self.code})'

    def __str__(self):
        return self.name

    async def get_players(self, return_json=False) -> List[Player]:
        """Returns a list containing the players who play for the team. Does
        not include the player's summary.

        :param return_json: (optional) Boolean. If ``True`` returns a list of
            dicts, if ``False`` returns a list of Player objects. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: list
        """
        players = await fetch(self._session, API_URLS[STATIC])
        players = players[ELEMENTS]
        team_players = [player for player in players if player[TEAM] == self.id]
        if return_json:
            return team_players
        return [Player(player, self._session) for player in team_players]

    async def get_team_fixtures(self, return_json=False):
        """Returns a list containing the team's fixtures.

        :param return_json: (optional) Boolean. If ``True`` returns a list of
            dicts, if ``False`` returns a list of TeamFixture objects.
            Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        fixtures = await fetch(self._session, API_URLS[FIXTURES])
        team_fixtures = defaultdict(list)
        for fixture in fixtures:
            if self.id == fixture.get(TEAM_HOME):
                team_fixtures[HOME].append(Fixture(fixture))
            elif self.id == fixture.get(TEAM_AWAY):
                team_fixtures[AWAY].append(Fixture(fixture))
        return team_fixtures
