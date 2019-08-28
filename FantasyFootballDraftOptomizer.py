import yaml
import csv
from enum import Enum


class Position(Enum):
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"


class Player:
    def __init__(self, name, position, rank, score):
        self.name = name
        self.position = position
        self.rank = rank
        self.score = score
        self.value = 0


def player_sort_score(player):
    return player.score


def player_sort_value(player):
    return player.value


def combine_rankings(rankings):
    ret_list = []
    for pos in rankings:
        ret_list = ret_list + pos
    ret_list.sort(key=player_sort_value, reverse=True)
    return ret_list


def load_position_rankings(config):
    name_rank_map = {}
    rankings_config = config["rankings"]
    for pos in Position:
        with open(rankings_config[pos.value]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                if row[0]:
                    name_rank_map[row[3]] = row[0]
    return name_rank_map


def calculate_player_values(player_list, position):
    player_list.sort(key=player_sort_score, reverse=True)
    point_spread = player_list[0].score - player_list[position_list[position]].score
    differential = point_spread / position_list[position]
    for player in player_list:
        player.value = point_spread - (int(player.rank) * differential)


with open('SampleConfig.yaml', 'r') as stream:
    config_file = yaml.safe_load(stream)
    name_rank = load_position_rankings(config_file)

qb_list = []
wr_list = []
rb_list = []
te_list = []

with open(config_file['stat_file']) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    next(csv_reader)
    for row in csv_reader:
        passing_yard = float(row[9]) if row[9] else 0
        passing_touchdown = float(row[10]) if row[10] else 0
        interception = float(row[11]) if row[11] else 0
        rushing_yard = float(row[13]) if row[13] else 0
        rushing_touchdown = float(row[15]) if row[15] else 0
        receptions = float(row[17]) if row[17] else 0
        receiving_yard = float(row[18]) if row[18] else 0
        return_touchdown = float(row[21]) if row[21] else 0
        fumble_lost = float(row[22]) if row[22] else 0
        two_point_conversion = float(row[24]) if row[24] else 0

        score = passing_yard * config_file['scoring']['passing_yard']\
            + passing_touchdown * config_file['scoring']['passing_touchdown']\
            + interception * config_file['scoring']['interception'] \
            + rushing_yard * config_file['scoring']['rushing_yard'] \
            + rushing_touchdown * config_file['scoring']['rushing_touchdown'] \
            + receiving_yard * config_file['scoring']['receiving_yard'] \
            + return_touchdown * config_file['scoring']['return_touchdown'] \
            + fumble_lost * config_file['scoring']['fumble_lost'] \
            + two_point_conversion * config_file['scoring']['two_point_conversion'] \
            + receptions * config_file['scoring']['ppr']
        if row[1] in name_rank:
            if row[3] == 'QB':
                qb_list.append(Player(row[1], row[3], name_rank[row[1]], score))
            elif row[3] == 'RB':
                rb_list.append(Player(row[1], row[3], name_rank[row[1]], score))
            elif row[3] == 'WR':
                wr_list.append(Player(row[1], row[3], name_rank[row[1]], score))
            elif row[3] == 'TE':
                te_list.append(Player(row[1], row[3], name_rank[row[1]], score))

position_list = {'QB': 0, 'WR': 0, 'TE': 0, 'RB': 0}

for position in config_file['positions']:
    if position == 'FLEX':
        position_list['RB'] = position_list['RB'] + .5
        position_list['WR'] = position_list['WR'] + .5
    else:
        position_list[position] = position_list[position] + 1

for position in position_list:
    position_list[position] = int(position_list[position] * config_file['league_size'])

calculate_player_values(qb_list, 'QB')
calculate_player_values(wr_list, 'WR')
calculate_player_values(rb_list, 'RB')
calculate_player_values(te_list, 'TE')


final_results = combine_rankings([qb_list, wr_list, rb_list, te_list])

for player in final_results:
    print('{},{},{}'.format(player.name, player.position, int(player.value * 10)/10))






