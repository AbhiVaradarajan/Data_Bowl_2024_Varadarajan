from cmu_graphics import *
import pandas as pd
import numpy as np
import math

player_file = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/players_db.csv')
player_file_np = player_file.values
plays_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/db_plays.csv')
plays_global = plays_global[plays_global['passResult'] != 'C']
plays_global = plays_global[plays_global['passResult'] != 'I']
plays_global = plays_global[plays_global['passResult'] != 'R']
plays_global = plays_global[plays_global['passResult'] != 'S']
plays_global = plays_global[plays_global['passResult'] != 'IN']
plays_global_np = plays_global.values
week1_global = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/tracking_week_1.csv')
week1_global_np = week1_global.values
seen_plays = set()
w1_rows, w1_cols = week1_global_np.shape
for row in range(w1_rows):
    gameID = week1_global_np[row, 0]
    if gameID not in seen_plays:
        seen_plays.add(gameID)
defPositions = {"NT", "DT", 'OLB', "ILB", "DE", "CB", "SS", "FS"}
inLine = {"TE", "G", "C", "T"}




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
    players_rows, players_cols = player_file_np.shape
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
                    if player_file_np[player_row, 0] == player_id:
                        player_name = player_file_np[player_row, 6]
                        player_position = player_file_np[player_row, 5]
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
                    if week1_np[week1_row, 16] == 'ball_snap' or week1_np[week1_row, 16] == 'snap_direct':
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
boxes = []
p_rows, p_cols = plays_global.shape
for row in range(p_rows):
    gameID = plays_global_np[row, 0]
    if gameID in seen_plays:
        playID = plays_global_np[row, 1]
        new_play = play_accessor(gameID, playID, week1_global)
        new_play.get_transverse()
        new_play.get_LOS()
        play_list.append(new_play)
for play in play_list:
    if play.LOS > 60 and play.team_side == play.O_team:
        play.flip()
    elif play.LOS < 60 and play.team_side == play.D_team:
        play.flip()
    else:
        play.flip_y()
    play.get_potential_pullers()
    play.get_center()
    if play.center == None:
        play_list.remove(play)
        continue
    for player in play.players:
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


        







def onAppStart(app):
    app.field_left = (app.width/2)-(700)
    app.field_top = (app.height/2)-(240)
    app.plays = counter_plays
    app.play_index = 0
    app.curr_play = app.plays[app.play_index]
    app.players = app.curr_play.players
    app.LOS = app.curr_play.LOS
    app.transverse = app.curr_play.transverse
    app.index = 0
    app.frames = len(app.curr_play.players[0].x_vals)
    app.ball = app.curr_play.ball
    app.paused = True
    app.stepsPerSecond = 10

def redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = 'dimGray')
    drawLabel(f'{app.curr_play.fit}', app.width/2, 40)
    drawRect(app.field_left, app.field_top, 1200, 540, fill = 'green', border = 'white', borderWidth = 5)
    for hash_x in range(1, 20):
        drawRect((app.field_left + 100) + (hash_x * 50), app.field_top, 3, 540, fill = 'white')
    drawRect(app.field_left, app.field_top, 100, 540, fill = 'indigo', border = 'white', borderWidth = 5)
    drawRect(app.field_left + 1100, app.field_top, 100, 540, fill = 'indigo', border = 'white', borderWidth = 5)
    drawRect(app.field_left + (app.LOS)* 10, app.field_top, 3, 540, fill = 'blue')
    drawRect(app.field_left, app.field_top + (app.transverse*10), 1200, 3, fill = 'black')
    for player in app.players:
        if player.is_puller:
            color = 'yellow'
        elif player == app.curr_play.center:
            color = 'purple'
        elif player.EMLOS:
            color = "deepPink"
        elif player.ps_EDGE:
            color = 'blue'
        elif player.team == app.curr_play.O_team:
            color = 'red'
        else:
            color = 'cyan'
        if app.curr_play.O_team == player.team:
            drawCircle(app.field_left + (player.x_vals[app.index])*10, app.field_top + ((player.y_vals[app.index])*10), 10, fill = color, border = 'black', borderWidth = 1)
        else:
            drawCircle(app.field_left + (player.x_vals[app.index])*10, app.field_top + ((player.y_vals[app.index])*10), 10, fill = color, border = 'black', borderWidth = 1)
        drawLabel(f'{player.position}', app.field_left + (player.x_vals[app.index])*10, app.field_top + ((player.y_vals[app.index])*10), size = 10, rotateAngle = player.orientations[app.index])
    drawOval(app.field_left + (app.ball.x_vals[app.index])*10, app.field_top + ((app.ball.y_vals[app.index])*10), 20, 10, fill = 'brown', opacity = 50, border = 'black', borderWidth = 1)


def onStep(app):
    if not app.paused:
        if app.index < app.frames-1:
            app.index+=1
        if app.index == app.frames:
            app.paused = True

def onKeyPress(app, key):
    if key == 'space':
        app.paused = not app.paused
    elif key == 'enter': 
        app.play_index += 1
        if app.play_index == len(app.plays):
            app.play_index = 0
        app.curr_play = app.plays[app.play_index]
        app.players = app.curr_play.players
        app.LOS = app.curr_play.LOS
        app.transverse = app.curr_play.transverse
        app.index = 0
        app.frames = len(app.curr_play.players[0].x_vals)
        app.ball = app.curr_play.ball
        app.paused = True
    elif key == 'r':
        app.curr_play = app.plays[app.play_index]
        app.players = app.curr_play.players
        app.index = 0
        app.frames = len(app.curr_play.players[0].x_vals)
        app.ball = app.curr_play.ball
        app.paused = True
def main():
    runApp(width = 1920, height = 1080)
main()
