import random
from players import Player


class Tournament:
    def __init__(self,
                 name,
                 place,
                 begin_date,
                 end_date,
                 tournament_nomber):
        self.name = name
        self.place = place
        self.begin_date = begin_date
        self.end_date = end_date
        self.round = 4
        self.tournament_nomber = tournament_nomber
        self.round_list = []
        self.players_list = []
        self.description = " "

    def __str__(self):
        return (f'{self.name} '
                f'{self.place}')

    def add_player(self, player):
        self.players_list.append(player)

    def shuffle_palyers(self):
        random.shuffle(self.players_list)


player1 = Player('Edouard', 'Plastik', '5/12/1963', 'AN123456')
player2 = Player('Gerard', 'Contemporain', '12/05/1936', 'NA654321')
player3 = Player('Gaspard', 'Chitect', '3/09/1393', 'BC4657981')
player4 = Player('Baltasar', 'Delatable', '25/12/0003', 'CB649785')

tn1 = Tournament('Coco', 'Tatouine', 'A long time ago', '01/12/-4768', '')

tn1.add_player(player1)
tn1.add_player(player2)
tn1.add_player(player3)
tn1.add_player(player4)

print(tn1)

print("\n--- OREDRE INITIAL ---")
for player in tn1.players_list:
    print(player)

shuffled_players = tn1.shuffle_palyers()
print("\n --- ORDRE APRES MELANGE ---")
for player in tn1.players_list:
    print(player)
