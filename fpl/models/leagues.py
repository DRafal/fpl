from collections import defaultdict

from .match import H2HMatch
from ..constants import API_URLS
from ..dictionaries.api_keywords import *
from ..utils import fetch, logged_in


class UserStandingsClassicEntry:
    def __init__(self, user_info):
        self.entry = user_info.get(ENTRY)
        self.entry_name = user_info.get(ENTRY_NAME)
        self.event_total = user_info.get(EVENT_TOTAL)
        self.id = user_info.get(ID)
        self.last_rank = user_info.get(LAST_RANK)
        self.player_name = user_info.get(PLAYER_NAME)
        self.rank = user_info.get(RANK)
        self.rank_sort = user_info.get(RANK_SORT)
        self.total = user_info.get(TOTAL)

    def __repr__(self):
        return f'UserStandingsClassicEntry(player_name="{self.player_name}", total={self.total})'


class UserStandingsH2HEntry:
    def __init__(self, user_info):
        self.division = user_info.get(DIVISION)
        self.entry = user_info.get(ENTRY)
        self.entry_name = user_info.get(ENTRY_NAME)
        self.id = user_info.get(ID)
        self.last_rank = user_info.get(LAST_RANK)
        self.matches_drawn = user_info.get(MATCHES_DRAWN)
        self.matches_lost = user_info.get(MATCHES_LOST)
        self.matches_played = user_info.get(MATCHES_PLAYED)
        self.matches_won = user_info.get(MATCHES_WON)
        self.player_name = user_info.get(PLAYER_NAME)
        self.points_for = user_info.get(POINTS_FOR)
        self.rank = user_info.get(RANK)
        self.rank_sort = user_info.get(RANK_SORT)
        self.total = user_info.get(TOTAL)

    def __repr__(self):
        return f'UserStandingsClassicEntry(player_name={self.player_name}, total={self.total})'


class UserNewEntry:
    def __init__(self, user_info):
        self.entry = user_info.get(ENTRY)
        self.entry_name = user_info.get(ENTRY_NAME)
        self.joined_time = user_info.get(JOINED_TIME)
        self.player_first_name = user_info.get(PLAYER_FIRST_NAME)
        self.player_last_name = user_info.get(PLAYER_LAST_NAME)

    def __repr__(self):
        return f'UserNewClassicEntry(player="{self.player_first_name} {self.player_last_name}", team_name="{self.team_name}")'


class League:
    """
    A parent class representing a league in the Fantasy Premier League.
    """

    def __init__(self, league_information, session):
        self._session = session
        self.admin_entry = league_information.get(LEAGUE).get(ADMIN_ENTRY)
        self.closed = league_information.get(LEAGUE).get(CLOSED)
        self.code_privacy = league_information.get(LEAGUE).get(CODE_PRIVACY)
        self.created = league_information.get(LEAGUE).get(CREATED)
        self.id = league_information.get(LEAGUE).get(ID)
        self.league_type = league_information.get(LEAGUE).get(LEAGUE_TYPE)
        self.max_entries = league_information.get(LEAGUE).get(MAX_ENTRIES)
        self.name = league_information.get(LEAGUE).get(NAME)
        self.rank = league_information.get(LEAGUE).get(RANK)
        self.scoring = league_information.get(LEAGUE).get(SCORING)
        self.start_event = league_information.get(LEAGUE).get(START_EVENT)

    def __str__(self):
        return f'{self.name} - {self.id}'

    async def get_specific_standing(self, page=1, phase_id=1):
        url = '{}?page_new_entries=1&page_standings={}&phase={}'.format(
            API_URLS["league_classic"].format(self.id),
            page,
            phase_id
        )
        league_page = await fetch(self._session, url)
        standings_page = league_page[STANDINGS]
        return [self.user_standing_type(entry) for entry in standings_page[RESULTS]]

    async def get_all_standings(self):
        """Returns the league's standings for all of the phases.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-classic/967/standings/?page_new_entries=1&page_standings=1&phase=1

        :rtype: defaultdict
        """
        phases = (
            OVERALL,
            AUGUST,
            SEPTEMBER,
            OCTOBER,
            NOVEMBER,
            DECEMBER,
            JANUARY,
            FEBRUARY,
            MARCH,
            APRIL,
            MAY,
            JUNE,
            JULY
        )
        standings = defaultdict(list)
        for phase_id, phase_name in enumerate(phases, 1):
            page = 1
            has_next = True
            while has_next:
                standings_page = await self.get_specific_standing(page, phase_id)
                has_next = standings_page[HAS_NEXT]
                standings[phase_name].extend(standings_page)
                page += 1

        return standings

    async def get_new_entries(self):
        """Returns the new entries of league.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-classic/967/standings/?page_new_entries=1&page_standings=1&phase=1

        rtype: list
        """
        new_entries = []
        page = 1
        has_next = True
        while has_next:
            url = '{}?page_new_entries={}&page_standings=1&phase=1'.format(
                API_URLS["league_classic"].format(self.id),
                page
            )
            league_page = await fetch(self._session, url)
            new_entries_page = league_page[NEW_ENTRIES]
            has_next = new_entries_page[HAS_NEXT]
            new_entries.extend([self.user_new_entry_type(entry) for entry in new_entries_page[RESULTS]])
            page += 1

        return new_entries


class ClassicLeague(League):
    """A class representing a classic league in the Fantasy Premier League.

        Basic usage::

          >>> from fpl import FPL
          >>> import aiohttp
          >>> import asyncio
          >>>
          >>> async def main():
          ...     async with aiohttp.ClientSession() as session:
          ...         fpl = FPL(session)
          ...         await fpl.login()
          ...         classic_league = await fpl.get_classic_league(1137)
          ...     print(classic_league)
          ...
          >>> asyncio.run(main())
          Official /r/FantasyPL Classic League - 1137
    """

    def __init__(self, league_information, session):
        super().__init__(league_information, session)
        self.user_standing_type = UserStandingsClassicEntry
        self.user_new_entry_type = UserNewEntry


class H2HLeague(League):
    """
    A class representing a H2H league in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         await fpl.login()
      ...         h2h_league = await fpl.get_h2h_league(760869)
      ...     print(h2h_league)
      ...
      >>> asyncio.run(main())
      League 760869 - 760869
    """

    def __init__(self, league_information, session):
        super().__init__(league_information, session)
        self.user_standing_type = UserStandingsH2HEntry
        self.user_new_entry_type = UserNewEntry


    async def get_fixtures(self, gameweek=None):
        """Returns a list of fixtures / results of the H2H league.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-h2h-matches/league/946125/?page=1

        :param gameweek: (optional) The gameweek of the fixtures / results.
        :type gameweek: string or int
        :param page: (optional) The fixtures / results page.
        :type page: string or int
        :rtype: list
        """
        if not self._session:
            return []

        if not logged_in(self._session):
            raise Exception(
                "Not authorised to get H2H fixtures. Log in first."
            )

        url_query = f"event={gameweek}&" if gameweek else ""
        has_next = True
        matches = []
        page = 1

        while has_next:
            fixtures = await fetch(
                self._session, API_URLS[LEAGUE_H2H_FIXTURES].format(
                    self.id, url_query, page
                )
            )
            matches.extend([H2HMatch(fixture) for fixture in fixtures[RESULTS]])
            has_next = fixtures[HAS_NEXT]
            page += 1

        return matches
