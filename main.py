# from controllers.playersmanager import PlayersManager
from models.player import Player
from models.tournament import Tournament
import random


tournament1 = Tournament(
    name="Tournoi OpenClassrooms",
    place="Paris",
    date="27/01/2026",
    rounds_qty=4,
    note="Projet 4")

tournament1.add_player(Player('Voltaire', 'Arouet', '21/11/1694', 'VA00001', 0))
tournament1.add_player(Player('Marie', 'Curie', '07/11/1867', 'MC12345', 0))
tournament1.add_player(Player('Albert', 'Einstein', '14/03/1879', 'AE54321', 0))
tournament1.add_player(Player('Léon', 'Blum', '09/04/1872', 'LB98765', 0))
tournament1.add_player(Player('Simone', 'Weil', '03/02/1909', 'SW11111', 0))
tournament1.add_player(Player('René', 'Descartes', '31/03/1596', 'RD22222', 0))
tournament1.add_player(Player('Jeanne', 'dArc', '06/01/1412', 'JA33333', 0))
tournament1.add_player(Player('Louis', 'Pasteur', '27/12/1822', 'LP44444', 0))

print(tournament1)

round1 = tournament1.create_round()
print('matchs du round 1: ')
for match in round1.matchs:
    p1, p2 = match.players_pair
    match.score(random.choice([p1, p2, None]))
    print(f'{match}')


tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
for player in tournament1.tournament_players:
    print(f'{player}')


round2 = tournament1.create_round()
print('\nmatchs du round 2: ')
for match in round2.matchs:
    p1, p2 = match.players_pair
    match.score(random.choice([p1, p2, None]))
    print(f'{match}')

tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
for player in tournament1.tournament_players:
    print(f'{player}')

round3 = tournament1.create_round()
print('\nmatchs du round 3: ')
for match in round3.matchs:
    p1, p2 = match.players_pair
    match.score(random.choice([p1, p2, None]))
    print(f'{match}')

tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
for player in tournament1.tournament_players:
    print(f'{player}')

round4 = tournament1.create_round()
print('\nmatchs du round 4: ')
for match in round4.matchs:
    p1, p2 = match.players_pair
    match.score(random.choice([p1, p2, None]))
    print(f'{match}')

print('\n🏆 CLASSEMENT FINAL DU TOURNOI 🏆')
tournament1.tournament_players.sort(key=lambda p: (-p.score, p.last_name))
for i, player in enumerate(tournament1.tournament_players, 1):
    print(f'{i}. {player.first_name} {player.last_name} - {player.score} pts')


# for pair in tournament1.rounds_list:
    

#  chess_tournament.tournament_players.append([player, player_score_initial_score,[]])

# for player in self.tournament_players:
#                 if player[0] == match.player1[0]:
#                     player[1] += match.score1
#                 if player[0] == match.player2[0]:
#                     player[1] += match.score2


# MATCH_SCORE = [(1, 0), (0.5, 0.5), (0, 1)]
# random.shuffle(MATCH_SCORE)