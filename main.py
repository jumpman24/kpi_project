from models import *

print(Country.get_by_id(1))
print(City.get_by_id(630))
print(Rank.get_by_id(1))
print(NationalRank.get_by_id(1))
print(Player.get_by_id(1))
print(Player.get_player_info(1, 2, 3, 4))
print(Tournament.get_by_id(1130))
print(Participant.get_by_id(2777))
print(Tournament.get_tournament_info(1130, 1131, 1132))
