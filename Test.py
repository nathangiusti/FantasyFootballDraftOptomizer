import yaml
import csv
from enum import Enum


class Position(Enum):
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"

class Player:
    def __init__(self, name, rank):
        self.name = name
        self.rank = rank
        self.score = 0

def get_base_position(position, config):
    return 0

def load_position_rankings(config, position):
    ret = []
    rankings_config = config["rankings"]
    base_position = get_base_position(position, config)
    with open(rankings_config[position.value]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            ret.append(Player(row[rankings_config["name_column"]], row[rankings_config["rank_column"]]))




with open('SampleConfig.yaml', 'r') as stream:
    config_file = yaml.safe_load(stream)

for position in Position:
    rankings = load_position_rankings(config_file, position)

