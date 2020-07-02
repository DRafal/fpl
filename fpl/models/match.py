from ..dictionaries.api_keywords import *

class H2HMatch:
    def __init__(self, match_data):
        self.entry_1_draw = match_data.get(ENTRY_1_DRAW)
        self.entry_1_entry = match_data.get(ENTRY_1_ENTRY)
        self.entry_1_loss = match_data.get(ENTRY_1_LOSS)
        self.entry_1_name = match_data.get(ENTRY_1_NAME)
        self.entry_1_player_name = match_data.get(ENTRY_1_PLAYER_NAME)
        self.entry_1_points = match_data.get(ENTRY_1_POINTS)
        self.entry_1_total = match_data.get(ENTRY_1_TOTAL)
        self.entry_1_win = match_data.get(ENTRY_1_WIN)
        self.entry_2_draw = match_data.get(ENTRY_2_DRAW)
        self.entry_2_entry = match_data.get(ENTRY_2_ENTRY)
        self.entry_2_loss = match_data.get(ENTRY_2_LOSS)
        self.entry_2_name = match_data.get(ENTRY_2_NAME)
        self.entry_2_player_name = match_data.get(ENTRY_2_PLAYER_NAME)
        self.entry_2_points = match_data.get(ENTRY_2_POINTS)
        self.entry_2_total = match_data.get(ENTRY_2_TOTAL)
        self.entry_2_win = match_data.get(ENTRY_2_WIN)
        self.event = match_data.get(EVENT)
        self.id = match_data.get(ID)
        self.is_knockout = match_data.get(IS_KNOCKOUT)
        self.seed_value = match_data.get(SEED_VALUE)
        self.tiebreak = match_data.get(TIEBREAK)
        self.winner = match_data.get(WINNER)

    def __repr__(self):
        return (f'UserCupMatch(Gameweek={self.event}:'
                f' "{self.entry_1_name}" [{self.entry_1_player_name}]'
                f' versus'
                f' "{self.entry_2_name}" [{self.entry_2_player_name}])')