import pandas as pd
import numpy as np
import math

defPositions = {"NT", "DT", 'OLB', "ILB", "DE", "CB", "SS", "FS"}
inLine = {"TE", "G", "C", "T"}
players_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/players_db.csv')
players_global_np = players_global.values
pbp_global = pd.read_csv("/Users/abhivaradarajan/Downloads/Data_Bowl/pbp_2022.csv")
plays_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/db_plays.csv')
plays_global = plays_global[plays_global['passResult'] != 'C']
plays_global = plays_global[plays_global['passResult'] != 'I']
plays_global = plays_global[plays_global['passResult'] != 'R']
plays_global = plays_global[plays_global['passResult'] != 'S']
plays_global = plays_global[plays_global['passResult'] != 'IN']
plays_global_np = plays_global.values
week1_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_1.csv')
week1_global_np = week1_global.values
w1_games = set()
w1_rows, w1_cols = week1_global_np.shape
for row in range(w1_rows):
    gameID = week1_global_np[row, 0]
    if gameID not in w1_games:
        w1_games.add(gameID)
week2_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_2.csv')
week2_global_np = week2_global.values
w2_games = set()
w2_rows, w2_cols = week2_global_np.shape
for row in range(w2_rows):
    gameID = week2_global_np[row, 0]
    if gameID not in w2_games:
        w2_games.add(gameID)
week3_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_3.csv')
week3_global_np = week3_global.values
w3_games = set()
w3_rows, w3_cols = week3_global_np.shape
for row in range(w3_rows):
    gameID = week3_global_np[row, 0]
    if gameID not in w3_games:
        w3_games.add(gameID)
week3_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_3.csv')
week3_global_np = week3_global.values
w3_games = set()
w3_rows, w3_cols = week3_global_np.shape
for row in range(w3_rows):
    gameID = week3_global_np[row, 0]
    if gameID not in w3_games:
        w3_games.add(gameID)
week4_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_4.csv')
week4_global_np = week4_global.values
w4_games = set()
w4_rows, w4_cols = week4_global_np.shape
for row in range(w4_rows):
    gameID = week4_global_np[row, 0]
    if gameID not in w4_games:
        w4_games.add(gameID)
week5_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_5.csv')
week5_global_np = week5_global.values
w5_games = set()
w5_rows, w5_cols = week5_global_np.shape
for row in range(w5_rows):
    gameID = week5_global_np[row, 0]
    if gameID not in w5_games:
        w5_games.add(gameID)
week6_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_6.csv')
week6_global_np = week6_global.values
w6_games = set()
w6_rows, w6_cols = week6_global_np.shape
for row in range(w6_rows):
    gameID = week6_global_np[row, 0]
    if gameID not in w6_games:
        w6_games.add(gameID)
week7_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_7.csv')
week7_global_np = week7_global.values
w7_games = set()
w7_rows, w7_cols = week7_global_np.shape
for row in range(w7_rows):
    gameID = week7_global_np[row, 0]
    if gameID not in w7_games:
        w7_games.add(gameID)
week8_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_8.csv')
week8_global_np = week8_global.values
w8_games = set()
w8_rows, w8_cols = week8_global_np.shape
for row in range(w8_rows):
    gameID = week8_global_np[row, 0]
    if gameID not in w8_games:
        w8_games.add(gameID)
week9_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_9.csv')
week9_global_np = week9_global.values
w9_games = set()
w9_rows, w9_cols = week9_global_np.shape
for row in range(w9_rows):
    gameID = week9_global_np[row, 0]
    if gameID not in w9_games:
        w9_games.add(gameID)




class Play: 
    def __init__(self, game_id, play_id):
        self.players = []
        self.O_team = None
        self.D_team = None
        self.team_side = None
        self.game_id = game_id
        self.play_id = play_id
        self.ball = None
        self.LOS = None
        self.center = None
        self.transverse = None
        self.dir = None
        self.is_flipped = False
        self.pullers = []
        self.is_counter = False
        self.TE_EMLOS = False
        self.fit = None
        self.yards_gained = None
    def __repr__(self):
        return f"play between {self.O_team} and {self.D_team}, game_id: {self.game_id}, play_id: {self.play_id}"
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        if isinstance(other, Play):
            return other.game_id == self.game_id and other.play_id == self.play_id
        else:
            return False
    def get_transverse(self):
        self.transverse = self.ball.y_vals[0]
    def get_LOS(self):
        self.LOS = self.ball.x_vals[0]
    def get_center(self):
        for player in self.players:
            if player.position not in defPositions:
                if abs(self.ball.y_vals[0] - player.y_vals[0]) <= 0.5 and abs(self.ball.x_vals[0] - player.x_vals[0]) < 1:
                    self.center = player
    def flip(self):
        for player in self.players:
            for i in range(len(player.x_vals)):
                player.x_vals[i] = 120 - player.x_vals[i]
        for i in range(len(self.ball.x_vals)):
            self.ball.x_vals[i] = 120 - self.ball.x_vals[i]
        self.LOS = 120 - self.LOS
        self.is_flipped = not self.is_flipped
    def flip_y(self):
        for player in self.players:
            for i in range(len(player.y_vals)):
                player.y_vals[i] = 53.3 - player.y_vals[i]
        for i in range(len(self.ball.y_vals)):
            self.ball.y_vals[i] = 53.3 - self.ball.y_vals[i]
        self.transverse = 53.3 - self.transverse
    def get_potential_pullers(self):
        for player in self.players:
            if player.position == 'G' or player.position == 'T' or player.position == 'TE':
                player.is_potential_puller = True
    def check_for_pullers(self, frame):
        center_y = self.center.y_vals[frame]
        for player in self.players:
            if player.is_potential_puller:
                if player.y_vals[0] < self.transverse:
                    if player.y_vals[frame] > center_y and player.y_vals[frame] > self.transverse and player.x_vals[frame] < self.LOS:
                        if self.center.initial_direction > 90 and self.center.initial_direction < 270:
                            if player.initial_direction > 0 and player.initial_direction < 90:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
                            elif player.initial_direction > 270 and player.initial_direction < 360:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
                        elif self.center.initial_direction > 0 and self.center.initial_direction < 90:
                            if player.initial_direction > 90 and player.initial_direction < 270:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
                        elif self.center.initial_direction > 270 and self.center.initial_direction < 360:
                            if player.initial_direction > 90 and player.initial_direction < 270:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
                elif player.y_vals[0] > self.transverse:
                    if player.y_vals[frame] < center_y and player.y_vals[frame] < self.transverse and player.x_vals[frame] < self.LOS:
                        if self.center.initial_direction > 90 and self.center.initial_direction < 270:
                            if player.initial_direction > 0 and player.initial_direction < 90:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
                            elif player.initial_direction > 270 and player.initial_direction < 360:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
                        elif self.center.initial_direction > 0 and self.center.initial_direction < 90:
                            if player.initial_direction > 90 and player.initial_direction < 270:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
                        elif self.center.initial_direction > 270 and self.center.initial_direction < 360:
                            if player.initial_direction > 90 and player.initial_direction < 270:
                                player.is_puller = True
                                if player not in self.pullers:
                                    self.pullers.append(player)
    def check_counter(self):
        curr_side = None
        if len(self.pullers) >= 2:
            for player in self.pullers:
                if player.y_vals[0] > self.transverse:
                    new_side = 'right'
                    if curr_side != None:
                        if curr_side != new_side:
                            return False
                    else:
                        curr_side = new_side
                else:
                    new_side = 'left'
                    if curr_side != None:
                        if curr_side != new_side:
                            return False
                    else:
                        curr_side = new_side
            return True
        return False
    def get_nearest_on_ball(self, player):
        current_best = None
        nearest_player = None
        if self.pullers[0].y_vals[0] > self.transverse:
            for new_player in self.players:
                if new_player == player or new_player.team == self.D_team or new_player.y_vals[0] > player.y_vals[0]:
                    continue
                else:
                    split = abs(new_player.y_vals[0] - player.y_vals[0])
                    if current_best == None:
                        current_best = split
                        nearest_player = new_player
                    elif split < current_best:
                        current_best = split
                        nearest_player = new_player
        else:
            for new_player in self.players:
                if new_player == player or new_player.team == self.D_team or new_player.y_vals[0] < player.y_vals[0]:
                    continue
                else:
                    split = abs(new_player.y_vals[0] - player.y_vals[0])
                    if current_best == None:
                        current_best = split
                        nearest_player = new_player
                    elif split < current_best:
                        current_best = split
                        nearest_player = new_player
        return nearest_player, current_best
    def get_EMLOS(self):
        if self.pullers[0].y_vals[0] > self.transverse:
            for player in self.players:
                if player.team == self.O_team:
                    if player.y_vals[0] < self.transverse:
                        if player.position not in inLine:
                            continue
                        else:
                            nearest_player, split = self.get_nearest_on_ball(player)
                            if nearest_player == None or nearest_player.position == 'WR':
                                player.EMLOS = True   
                            elif nearest_player.position == "TE" and split > 2:
                                player.EMLOS = True
                                for player_2 in self.players:
                                    if player_2 != player and player_2.EMLOS == True:
                                        player_2.EMLOS = False
        else:
            for player in self.players:
                if player.team == self.O_team:
                    if player.y_vals[0] > self.transverse:
                        if player.position not in inLine:
                            continue
                        else:
                            nearest_player, split = self.get_nearest_on_ball(player)
                            if nearest_player == None or nearest_player.position == "WR":
                                player.EMLOS = True
                            elif nearest_player.position == "TE" and split > 2:
                                player.EMLOS = True
                                for player_2 in self.players:
                                    if player_2 != player and player_2.EMLOS == True:
                                        player_2.EMLOS = False
    def TE_is_EMLOS(self):
        for player in self.players:
            if player.position == 'TE' and player.EMLOS == True:
                self.TE_EMLOS = True
    def filter_EMLOS(self):
        if self.TE_EMLOS:
            for player in self.players:
                if player.EMLOS == True and player.position != 'TE':
                    player.EMLOS = False
    def get_nearest_EDGE(self, player):
        current_best_split = None
        nearest_EDGE = None
        player_x = player.x_vals[0]
        player_y = player.y_vals[0]
        for new_player in self.players:
            if new_player.position == "OLB" or new_player.position == "DE" or player.position == "ILB":
                new_player_x = new_player.x_vals[0]
                new_player_y = new_player.y_vals[0]
                split = distance(player_x, player_y, new_player_x, new_player_y)
                if current_best_split == None or split < current_best_split:
                    current_best_split = split
                    nearest_EDGE = new_player
        return nearest_EDGE
    def get_ps_EDGE(self):
        for player in self.players:
            if player.EMLOS == True:
                ps_edge = self.get_nearest_EDGE(player)
                ps_edge.ps_EDGE = True
    def get_run_fit(self):
        for player in self.players:
            if player.ps_EDGE == True:
                if player.initial_direction > 225 and player.initial_direction < 325:
                    self.fit = 'box'
                else:
                    self.fit = 'spill'
    def get_yards_gained(self):
        pbp_self = pbp_global
        pbp_self = pbp_self[pbp_self['old_game_id'] == self.game_id]
        pbp_self = pbp_self[pbp_self['play_id'] == self.play_id]
        pbp_self_np = pbp_self.values
        self.yards_gained = pbp_self_np[0, 29]



class Player:
    def __init__(self, name, position, id, team):
        self.id = id
        self.name = name
        self.position = position
        self.team = team
        self.x_vals = []
        self.y_vals = []
        self.orientations = []
        self.dirs = []
        self.is_potential_puller = False
        self.is_puller = False
        self.ball_snap_frame = None
        self.initial_direction = None
        self.EDGE = False
        self.tackle = False
        self.assist = False
        self.EMLOS = False
        self.ps_EDGE = False
    def __repr__(self):
        return(f"Player: {self.name}, Team: {self.team}, Position: {self.position}, Player ID: {self.id}")
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        if isinstance(other, Player):
            return self.id == other.id
        else:
            return False
    def add_tracking(self, x_val, y_val, orientation, direction):
        self.x_vals.append(x_val)
        self.y_vals.append(y_val)
        self.orientations.append(orientation)
        self.dirs.append(direction)
    def get_initial_direction(self):
        sum = 0
        for frame in range(self.ball_snap_frame, self.ball_snap_frame + 5):
            sum += self.dirs[frame]
        self.initial_direction = sum//5


class Ball:
    def __init__(self):
        self.x_vals = []
        self.y_vals = []
        self.orientations = []
    def __repr__(self):
        return('ball')
    def add_tracking(self, x_val, y_val):
        self.x_vals.append(x_val)
        self.y_vals.append(y_val)

class global_player:
    def __init__(self, name, team, position, ID):
        self.name = name
        self.team = team
        self.position = position
        self.ID = ID
        self.net_spill_yards = 0
        self.total_spill_snaps = 0
        self.net_box_yards = 0
        self.total_box_snaps = 0
        self.average_spill_yards = None
        self.average_box_yards = None
    def __repr__(self):
        return(f"Player: {self.name}, Team: {self.team}, Position: {self.position}, Player ID: {self.id}")
    def __eq__ (self, other):
        if isinstance(other, global_player):
            return self.ID == other.ID
        else:
            return False
    def __hash__(self):
        return hash(str(self))
    def get_average_spill_yards(self):
        return self.net_spill_yards/self.total_spill_snaps
    def get_average_box_yards(self):
        return self.net_box_yards/self.total_box_snaps


def play_accessor(game, play, file):
    #file from NFL Big Data Bowl, found on kaggle at https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/overview
    #file from NFL Big Data Bowl, found on kaggle at https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/overview
    week1copy = file
    week1copy = week1copy[week1copy['gameId'] == game]
    week1copy = week1copy[week1copy['playId'] == play]
    week1_np = week1copy.values
    #file from NFL Big Data Bowl, found on kaggle at https://www.kaggle.com/competitions/nfl-big-data-bowl-2023/overview
    plays = plays_global
    plays = plays[plays['gameId'] == game]
    plays = plays[plays['playId'] == play]
    plays_np = plays.values
    play_1 = Play(game, play)
    play_1.D_team = plays_np[0,9]
    play_1.O_team = plays_np[0,8]
    play_1.team_side = plays_np[0, 10]
    player_id_list = set()
    players_rows, players_cols = players_global_np.shape
    week1_rows, week1_cols = week1_np.shape
    for week1_row in range(week1_rows):
        if play_1.dir == None:
            play_1.dir = week1_np[week1_row, 8]
        player_id = week1_np[week1_row, 2]
        player_team = week1_np[week1_row, 7]
        player_x = week1_np[week1_row, 9]
        player_y = week1_np[week1_row, 10]
        player_o = week1_np[week1_row, 14]
        player_dir = week1_np[week1_row, 15]
        if not math.isnan(player_id):
            if player_id not in player_id_list:
                for player_row in range(players_rows):
                    if players_global_np[player_row, 0] == player_id:
                        player_name = players_global_np[player_row, 6]
                        player_position = players_global_np[player_row, 5]
                        id = player_id
                        player = Player(player_name, player_position, id, player_team)
                        play_1.players.append(player)
                        player_id_list.add(player_id)
                    else:
                        continue
            else:
                for player in play_1.players:
                    if player.id == player_id:
                        player.add_tracking(player_x, player_y, player_o, player_dir)
                    if week1_np[week1_row, 16] == 'ball_snap' or week1_np[week1_row, 16] == 'snap_direct' or week1_np[week1_row, 16] == "autoevent_ballsnap":
                        if player.ball_snap_frame == None:
                            player.ball_snap_frame = week1_np[week1_row, 4] - 2
                    else:
                        continue
        else:
            if play_1.ball == None:
                play_1.ball = Ball()
                play_1.ball.add_tracking(player_x, player_y)
            else:
                play_1.ball.add_tracking(player_x, player_y)
    return play_1



def get_tackles(gameID, playID, play):
    tackles = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tackles.csv')
    tackles = tackles[tackles['gameId'] == gameID]
    tackles = tackles[tackles['playId'] == playID]
    tackles_np = tackles.values
    t_rows, t_cols = tackles_np.shape
    if t_rows == 0:
        return None
    else:
        for t_row in range(t_rows):
            if tackles_np[t_row, 3] == 1:
                tackling_player = tackles_np[t_row, 2]
                for player in play.players:
                    if player.id == tackling_player:
                        player.tackle = True
            elif tackles_np[t_row, 4] == 1:
                tackling_player = tackles_np[t_row, 2]
                for player in play.players:
                    if player.id == tackling_player:
                        player.assist = True

def distance(x1, y1, x2, y2):
    modified_x = (x2-x1)**2
    modified_y = (y2-y1)**2
    return (modified_x + modified_y)**0.5




play_list = []
counter_plays = []
spills = []
spillsDict = {'players': [], "net spill yards": [], "total spill snaps": [], "average spill yards": []}
boxes = []
boxesDict = {'players': [], "net box yards": [], "total box snaps": [], "average box yards": []}
p_rows, p_cols = plays_global.shape
for row in range(p_rows):
    gameID = plays_global_np[row, 0]
    if gameID in w1_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week1_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    elif gameID in w2_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week2_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    elif gameID in w3_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week3_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    elif gameID in w4_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week4_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    elif gameID in w5_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week5_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    elif gameID in w6_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week6_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    elif gameID in w7_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week7_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    elif gameID in w8_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week8_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
    if gameID in w9_games:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week9_global)
        print(new_play.game_id, new_play.play_id)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
for play in play_list:
    if play.LOS > 60 and play.team_side == play.O_team:
        play.flip()
        play.flip_y()
    elif play.LOS < 60 and play.team_side == play.D_team:
        play.flip()
        play.flip_y()
    play.get_potential_pullers()
    play.get_center()
    if play.center == None:
        play_list.remove(play)
        continue
    for player in play.players:
        print(player.name)
        player.get_initial_direction()
    play.center.get_initial_direction()
    for frame in range(len(play.players[0].x_vals)):
        play.check_for_pullers(frame)
    if play.check_counter():
        get_tackles(play.game_id, play.play_id, play)
        play.get_EMLOS()
    for player in play.players:
        if player.EMLOS == True:
            play.TE_is_EMLOS()
            counter_plays.append(play)
            break
for play in counter_plays:
    play.filter_EMLOS()
    play.get_ps_EDGE()
    play.get_run_fit()
    play.get_yards_gained()
    if play.fit == 'spill':
        for player in play.players:
            if player.ps_EDGE == True:
                was_found = False
                for new_player in spills:
                    if new_player.ID == player.id:
                        was_found = True
                        new_player.total_spill_snaps += 1
                        new_player.net_spill_yards += play.yards_gained
                if was_found == False:
                    player_global = global_player(player.name, player.team, player.position, player.id) 
                    player_global.net_spill_yards = play.yards_gained
                    player_global.total_spill_snaps += 1
                    spills.append(player_global)

    else:
        for player in play.players:
            if player.ps_EDGE == True:
                was_found = False
                for new_player in boxes:
                    if new_player.ID == player.id:
                        was_found = True
                        new_player.total_box_snaps += 1
                        new_player.net_box_yards += play.yards_gained
                if was_found == False:
                    player_global = global_player(player.name, player.team, player.position, player.id) 
                    player_global.net_box_yards = play.yards_gained
                    player_global.total_box_snaps += 1
                    boxes.append(player_global)
print('spills')
for player in spills:
    average_yards = player.get_average_spill_yards()
    spillsDict['players'].append(player.name)
    spillsDict['net spill yards'].append(player.net_spill_yards)
    spillsDict['total spill snaps'].append(player.total_spill_snaps)
    spillsDict['average spill yards'].append(average_yards)
print('boxes')
for player in boxes:
    average_yards = player.get_average_box_yards()
    boxesDict['players'].append(player.name)
    boxesDict['net box yards'].append(player.net_box_yards)
    boxesDict['total box snaps'].append(player.total_box_snaps)
    boxesDict['average box yards'].append(average_yards)

spillsDF = pd.DataFrame(data = spillsDict)
boxesDF = pd.DataFrame(data = boxesDict)
spillsDF.to_csv('spills.csv')
boxesDF.to_csv('boxes.csv')