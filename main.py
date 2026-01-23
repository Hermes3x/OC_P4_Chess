from models.players import Player
from models.matchs import Match
from models.rounds import Rounds

player1 = Player('Voltaire', 'Arouet', '21/11/1694', 'VA00001')
player2 = Player('Marie', 'Curie', '07/11/1867', 'MC12345')
player3 = Player('Albert', 'Einstein', '14/03/1879', 'AE54321')
player4 = Player('Léon', 'Blum', '09/04/1872', 'LB98765')
player5 = Player('Simone', 'Weil', '03/02/1909', 'SW11111')
player6 = Player('René', 'Descartes', '31/03/1596', 'RD22222')
player7 = Player('Jeanne', 'dArc', '06/01/1412', 'JA33333')
player8 = Player('Louis', 'Pasteur', '27/12/1822', 'LP44444')

rounds_players_sorted_list = [player1,
                              player2,
                              player3,
                              player4,
                              player5,
                              player6,
                              player7,
                              player8]

round1 = Rounds(rounds_players_sorted_list)
round1.create_matchs()
print(round1)
