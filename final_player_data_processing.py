import pandas as pd

spills = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/spills.csv')
spills_np = spills.values
s_rows, s_cols = spills.shape
boxes = pd.read_csv('/Users/abhivaradarajan/Downloads/Data_Bowl/boxes.csv')
boxes_np = boxes.values
b_rows, b_cols = boxes.shape


spillsSet = []
boxesSet = set()
final_dict = {'player': [], 'avg box yds': [], 'avg spill yds': []}

def get_avg_spill_yards(player):
    for row in range(s_rows):
        if spills_np[row, 1] == player:
            return spills_np[row, 4]

def get_avg_box_yards(player):
    for row in range(b_rows):
        if boxes_np[row, 1] == player:
            return boxes_np[row, 4]

for row in range(s_rows):
    player = spills_np[row, 1]
    if spills_np[row, 3] >= 2:
        spillsSet.append(player)
for row in range(b_rows):
    player = boxes_np[row, 1]
    if boxes_np[row, 3] >= 2:
        boxesSet.add(player)
print(spillsSet)
for player in spillsSet:
    if player in boxesSet:
        final_dict['player'].append(player)
        final_dict['avg spill yds'].append(get_avg_spill_yards(player))
        final_dict['avg box yds'].append(get_avg_box_yards(player))

finalDF = pd.DataFrame(data = final_dict)
finalDF.to_csv('final_data.csv')



