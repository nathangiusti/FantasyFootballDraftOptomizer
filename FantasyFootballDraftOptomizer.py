import yaml
import csv
from enum import Enum


class Position(Enum):
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"


class Player:
    def __init__(self, name, position, rank):
        self.name = name
        self.position = position
        self.rank = rank
        self.value = 0


def player_sort_score(player):
    return player.score


def player_sort_value(player):
    return player.value


def combine_rankings(rankings):
    ret_list = []
    for pos in rankings:
        ret_list = ret_list + rankings[pos]
    ret_list.sort(key=player_sort_value, reverse=True)
    return ret_list


def load_position_rankings(config):
    name_rank_map = {Position.QB: [], Position.WR: [], Position.RB: [], Position.TE: []}
    rankings_config = config["rankings"]
    for pos in Position:
        with open(rankings_config[pos.value]) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                if row[0]:
                    name_rank_map[pos].append(Player(row[3], pos, row[0]))
    return name_rank_map


def calculate_player_values(score_list, player_list, num_players_in_position):
    score_list.sort(key=float, reverse=True)
    point_spread = score_list[0] - score_list[num_players_in_position]
    differential = point_spread / num_players_in_position
    for player in player_list:
        player.value = point_spread - (int(player.rank) * differential)


def load_positions(config_file):
    position_list = {Position.QB: 0, Position.WR: 0, Position.TE: 0, Position.RB: 0}
    for position in config_file['positions']:

        if position == 'FLEX':
            position_list[Position.RB] = position_list[Position.RB] + .5
            position_list[Position.WR] = position_list[Position.WR] + .5
        else:
            position_list[Position[position]] = position_list[Position[position]] + 1

    for position in position_list:
        position_list[position] = int(position_list[position] * config_file['league_size'])
    return position_list


def load_stat_file(config_file):
    score_list = {Position.QB: [], Position.WR: [], Position.RB: [], Position.TE: []}
    with open(config_file['stat_file']) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        next(csv_reader)

        for row in csv_reader:
            if not row[3]:
                continue
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

            score = passing_yard * config_file['scoring']['passing_yard'] \
                    + passing_touchdown * config_file['scoring']['passing_touchdown'] \
                    + interception * config_file['scoring']['interception'] \
                    + rushing_yard * config_file['scoring']['rushing_yard'] \
                    + rushing_touchdown * config_file['scoring']['rushing_touchdown'] \
                    + receiving_yard * config_file['scoring']['receiving_yard'] \
                    + return_touchdown * config_file['scoring']['return_touchdown'] \
                    + fumble_lost * config_file['scoring']['fumble_lost'] \
                    + two_point_conversion * config_file['scoring']['two_point_conversion'] \
                    + receptions * config_file['scoring']['ppr']
            score_list[Position[row[3]]].append(score)
    return score_list


def initialize():
    with open('SampleConfig.yaml', 'r') as stream:
        config_file = yaml.safe_load(stream)

    name_rank = load_position_rankings(config_file)
    position_list = load_positions(config_file)
    score_list = load_stat_file(config_file)

    return name_rank, score_list, position_list


def main():
    name_rank, score_list, position_list = initialize()
    for pos in Position:
        calculate_player_values(score_list[pos], name_rank[pos], position_list[pos])
    final_results = combine_rankings(name_rank)

    for player in final_results:
        print('{},{},{}'.format(player.name, player.position.name, int(player.value * 10)/10))


main()


