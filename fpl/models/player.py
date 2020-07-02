from ..constants import API_URLS
from ..dictionaries.api_keywords import *
from ..utils import fetch, position_converter, team_converter


class PlayerType:
    def __init__(self, type_info):
        self.element_count = type_info.get(ELEMENT_COUNT)
        self.id = type_info.get(ID)
        self.plural_name = type_info.get(PLURAL_NAME)
        self.plural_name_short = type_info.get(PLURAL_NAME_SHORT)
        self.singular_name = type_info.get(SINGULAR_NAME)
        self.singular_name_short = type_info.get(SINGULAR_NAME_SHORT)
        self.squad_max_play = type_info.get(SQUAD_MAX_PLAY)
        self.squad_min_play = type_info.get(SQUAD_MIN_PLAY)
        self.squad_select = type_info.get(SQUAD_SELECT)
        self.sub_positions_locked = type_info.get(SUB_POSITIONS_LOCKED)
        self.ui_shirt_specific = type_info.get(UI_SHIRT_SPECIFIC)

    def __repr__(self):
        return f'PlayerType(name={self.singular_name}, squad_select={self.squad_select})'


class Player:
    """A class representing a player in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         player = await fpl.get_player(302)
      ...     print(player)
      ...
      >>> asyncio.run(main())
      Pogba - Midfielder - Man Utd
    """

    def __init__(self, player_information, session, player_summary=None):
        self._session = session
        self.assists = player_information.get(ASSISTS)
        self.bonus = player_information.get(BONUS)
        self.bps = player_information.get(BPS)
        self.chance_of_playing_next_round = player_information.get(CHANCE_OF_PLAYING_NEXT_ROUND)
        self.chance_of_playing_this_round = player_information.get(CHANCE_OF_PLAYING_THIS_ROUND)
        self.clean_sheets = player_information.get(CLEAN_SHEETS)
        self.code = player_information.get(CODE)
        self.cost_change_event = player_information.get(COST_CHANGE_EVENT)
        self.cost_change_event_fall = player_information.get(COST_CHANGE_EVENT_FALL)
        self.cost_change_start = player_information.get(COST_CHANGE_START)
        self.cost_change_start_fall = player_information.get(COST_CHANGE_START_FALL)
        self.creativity = player_information.get(CREATIVITY)
        self.creativity_rank = player_information.get(CREATIVITY_RANK)
        self.creativity_rank_type = player_information.get(CREATIVITY_RANK_TYPE)
        self.dreamteam_count = player_information.get(DREAMTEAM_COUNT)
        self.element_type = player_information.get(ELEMENT_TYPE)
        self.ep_next = player_information.get(EP_NEXT)
        self.ep_this = player_information.get(EP_THIS)
        self.event_points = player_information.get(EVENT_POINTS)
        self.first_name = player_information.get(FIRST_NAME)
        self.form = player_information.get(FORM)
        self.goals_conceded = player_information.get(GOALS_CONCEDED)
        self.goals_scored = player_information.get(GOALS_SCORED)
        self.ict_index = player_information.get(ICT_INDEX)
        self.ict_index_rank = player_information.get(ICT_INDEX_RANK)
        self.ict_index_rank_type = player_information.get(ICT_INDEX_RANK_TYPE)
        self.id = player_information.get(ID)
        self.in_dreamteam = player_information.get(IN_DREAMTEAM)
        self.influence = player_information.get(INFLUENCE)
        self.influence_rank = player_information.get(INFLUENCE_RANK)
        self.influence_rank_type = player_information.get(INFLUENCE_RANK_TYPE)
        self.minutes = float(player_information.get(MINUTES))
        self.news = player_information.get(NEWS)
        self.news_added = player_information.get(NEWS_ADDED)
        self.now_cost = player_information.get(NOW_COST, 0)
        self.own_goals = player_information.get(OWN_GOALS)
        self.penalties_missed = player_information.get(PENALTIES_MISSED)
        self.penalties_saved = player_information.get(PENALTIES_SAVED)
        self.photo = player_information.get(PHOTO)
        self.points_per_game = player_information.get(POINTS_PER_GAME)
        self.red_cards = player_information.get(RED_CARDS)
        self.saves = player_information.get(SAVES)
        self.second_name = player_information.get(SECOND_NAME)
        self.selected_by_percent = player_information.get(SELECTED_BY_PERCENT)
        self.special = player_information.get(SPECIAL)
        self.squad_number = player_information.get(SQUAD_NUMBER)
        self.status = player_information.get(STATUS)
        self.team = player_information.get(TEAM)
        self.team_code = player_information.get(TEAM_CODE)
        self.threat = player_information.get(THREAT)
        self.threat_rank = player_information.get(THREAT_RANK)
        self.threat_rank_type = player_information.get(THREAT_RANK_TYPE)
        self.total_points = player_information.get(TOTAL_POINTS)
        self.transfers_in = player_information.get(TRANSFERS_IN)
        self.transfers_in_event = player_information.get(TRANSFERS_IN_EVENT)
        self.transfers_out = player_information.get(TRANSFERS_OUT)
        self.transfers_out_event = player_information.get(TRANSFERS_OUT_EVENT)
        self.value_form = player_information.get(VALUE_FORM)
        self.value_season = player_information.get(VALUE_SEASON)
        self.web_name = player_information.get(WEB_NAME)
        self.yellow_cards = player_information.get(YELLOW_CARDS)
        self.player_summary = player_summary

    def __repr__(self):
        return f'Player(name="{self.first_name} {self.second_name}", id={self.id})'

    @property
    async def games_played(self):
        """The number of games where the player has played at least 1 minute.

        :rtype: int
        """
        if hasattr(self, HISTORY):
            fixtures = self.history
        else:
            player_summary = await fetch(
                self._session, API_URLS[PLAYER].format(self.id))
            fixtures = player_summary[HISTORY]

        return sum([1 for fixture in fixtures if fixture[MINUTES] > 0])

    @property
    def pp90(self):
        """Points per 90 minutes.

        :rtype: float
        """
        if self.minutes != 0.0:
            return (self.total_points or 0.0) / self.minutes * 90.0
        return 0.0

    @property
    async def vapm(self):
        """Value added per million
        An explanation of VAPM can be found here:
            https://www.reddit.com/r/FantasyPL/comments/6r60fu/exploring_a_key_metric_value_added_per_1m/

        :rtype: float
        """
        games_played = await self.games_played

        if not games_played == 0 or not self.now_cost:
            return 0.0

        return ((self.total_points or 0.0) / games_played - 2) / (self.now_cost / 10)

    def __str__(self):
        return (f"{self.web_name} - "
                f"{position_converter(self.element_type)} - "
                f"{team_converter(self.team)}")


class HistoricSeason:
    def __init__(self, season_info):
        self.assists = season_info[ASSISTS]
        self.bonus = season_info[BONUS]
        self.bps = season_info[BPS]
        self.clean_sheets = season_info[CLEAN_SHEETS]
        self.creativity = season_info[CREATIVITY]
        self.element_code = season_info[ELEMENT_CODE]
        self.end_cost = season_info[END_COST]
        self.goals_conceded = season_info[GOALS_CONCEDED]
        self.goals_scored = season_info[GOALS_SCORED]
        self.ict_index = season_info[ICT_INDEX]
        self.influence = season_info[INFLUENCE]
        self.minutes = season_info[MINUTES]
        self.own_goals = season_info[OWN_GOALS]
        self.penalties_missed = season_info[PENALTIES_MISSED]
        self.penalties_saved = season_info[PENALTIES_SAVED]
        self.red_cards = season_info[RED_CARDS]
        self.saves = season_info[SAVES]
        self.season_name = season_info[SEASON_NAME]
        self.start_cost = season_info[START_COST]
        self.threat = season_info[THREAT]
        self.total_points = season_info[TOTAL_POINTS]
        self.yellow_cards = season_info[YELLOW_CARDS]

    def __repr__(self):
        return f'HistoricSeason(season="{self.season_name}", total_points={self.total_points})'


class PlayedFixture:
    def __init__(self, fixture_info):
        self.assists = fixture_info[ASSISTS]
        self.bonus = fixture_info[BONUS]
        self.bps = fixture_info[BPS]
        self.clean_sheets = fixture_info[CLEAN_SHEETS]
        self.creativity = fixture_info[CREATIVITY]
        self.element = fixture_info[ELEMENT]
        self.fixture = fixture_info[FIXTURE]
        self.goals_conceded = fixture_info[GOALS_CONCEDED]
        self.goals_scored = fixture_info[GOALS_SCORED]
        self.ict_index = fixture_info[ICT_INDEX]
        self.influence = fixture_info[INFLUENCE]
        self.kickoff_time = fixture_info[KICKOFF_TIME]
        self.minutes = fixture_info[MINUTES]
        self.opponent_team = fixture_info[OPPONENT_TEAM]
        self.own_goals = fixture_info[OWN_GOALS]
        self.penalties_missed = fixture_info[PENALTIES_MISSED]
        self.penalties_saved = fixture_info[PENALTIES_SAVED]
        self.red_cards = fixture_info[RED_CARDS]
        self.round = fixture_info[ROUND]
        self.saves = fixture_info[SAVES]
        self.selected = fixture_info[SELECTED]
        self.team_away_score = fixture_info[TEAM_AWAY_SCORE]
        self.team_home_score = fixture_info[TEAM_HOME_SCORE]
        self.threat = fixture_info[THREAT]
        self.total_points = fixture_info[TOTAL_POINTS]
        self.transfers_balance = fixture_info[TRANSFERS_BALANCE]
        self.transfers_in = fixture_info[TRANSFERS_IN]
        self.transfers_out = fixture_info[TRANSFERS_OUT]
        self.value = fixture_info[VALUE]
        self.was_home = fixture_info[WAS_HOME]
        self.yellow_cards = fixture_info[YELLOW_CARDS]

    def __repr__(self):
        return f'PlayedFixture(vs "{team_converter(self.opponent_team)}", total_points={self.total_points})'


class FutureFixture:
    def __init__(self, fixture_info):
        self.code = fixture_info[CODE]
        self.difficulty = fixture_info[DIFFICULTY]
        self.event = fixture_info[EVENT]
        self.event_name = fixture_info[EVENT_NAME]
        self.finished = fixture_info[FINISHED]
        self.id = fixture_info[ID]
        self.is_home = fixture_info[IS_HOME]
        self.kickoff_time = fixture_info[KICKOFF_TIME]
        self.minutes = fixture_info[MINUTES]
        self.provisional_start_time = fixture_info[PROVISIONAL_START_TIME]
        self.team_away = fixture_info[TEAM_AWAY]
        self.team_away_score = fixture_info[TEAM_AWAY_SCORE]
        self.team_home = fixture_info[TEAM_HOME]
        self.team_home_score = fixture_info[TEAM_HOME_SCORE]

    def __repr__(self):
        return f'FutureFixture(vs {team_converter((self.team_away if self.is_home else self.team_home))})'


class PlayerSummary:
    """A class representing a player in the Fantasy Premier League's summary.
    """

    def __init__(self, player_summary, player_id):
        self.player_id = player_id
        self.played_fixtures = {fixture.get(FIXTURE): PlayedFixture(fixture) for fixture in player_summary[HISTORY]}
        self.future_fixtures = {fixture.get(FIXTURE): FutureFixture(fixture) for fixture in player_summary[FIXTURES]}
        self.historic_seasons = [HistoricSeason(season) for season in player_summary[HISTORY_PAST]]

    def __repr__(self):
        return f'PlayerSummary(id={self.player_id})'
