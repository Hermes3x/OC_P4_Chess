from controllers.database_controller import DatabaseController
from models.player import Player
from models.tournament import Tournament
import random
import pprint


tournament1 = Tournament(
    name="Tournoi OpenClassrooms",
    place="Paris",
    date="27/01/2026",
    rounds_qty=4,
    note="Projet 4")

db_controller = DatabaseController()
players_from_json = db_controller.load_players_from_json()

for player in players_from_json:
    tournament1.add_player(player)

print(f'{len(players_from_json)} joueurs ont été ajoutés au tournoi')

round1 = tournament1.create_round()
for match in round1.matchs:
    p1, p2 = match.players_pair
    match.score(random.choice([p1, p2, None]))
    print(f'{match}')

round1.close_round()

round2 = tournament1.create_round()
for match in round2.matchs:
    p1, p2 = match.players_pair
    match.score(random.choice([p1, p2, None]))
    print(f'Résultats \n{match}')

round2.close_round()

print("\n--- TEST EXPORT COMPLET ---")
full_dict = tournament1.to_dict()
pprint.pprint(full_dict)


# round1 = tournament1.create_round()
# print('\nmatchs du round 1: \n')
# for match in round1.matchs:
#     p1, p2 = match.players_pair
#     match.score(random.choice([p1, p2, None]))
#     print(f'{match}')


# tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
# for player in tournament1.tournament_players:
#     print(f'{player}')


# round2 = tournament1.create_round()
# print('\nmatchs du round 2: ')
# for match in round2.matchs:
#     p1, p2 = match.players_pair
#     match.score(random.choice([p1, p2, None]))
#     print(f'{match}')

# tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
# for player in tournament1.tournament_players:
#     print(f'{player}')

# round3 = tournament1.create_round()
# print('\nmatchs du round 3: ')
# for match in round3.matchs:
#     p1, p2 = match.players_pair
#     match.score(random.choice([p1, p2, None]))
#     print(f'{match}')

# tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
# for player in tournament1.tournament_players:
#     print(f'{player}')

# round4 = tournament1.create_round()
# print('\nmatchs du round 4: ')
# for match in round4.matchs:
#     p1, p2 = match.players_pair
#     match.score(random.choice([p1, p2, None]))
#     print(f'{match}')

# print('\n🏆 CLASSEMENT FINAL DU TOURNOI 🏆')
# tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
# for i, player in enumerate(tournament1.tournament_players, 1):
#     print(f'{i}. {player.first_name} {player.last_name} - {player.score} pts')


# for pair in tournament1.rounds_list:
    

#  chess_tournament.tournament_players.append([player, player_score_initial_score,[]])

# for player in self.tournament_players:
#                 if player[0] == match.player1[0]:
#                     player[1] += match.score1
#                 if player[0] == match.player2[0]:
#                     player[1] += match.score2


# MATCH_SCORE = [(1, 0), (0.5, 0.5), (0, 1)]
# random.shuffle(MATCH_SCORE)