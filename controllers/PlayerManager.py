import random
from models.players import Player

class PlayerManager:
    def __init__(self):
        self.players_list = []
        self.pairs = []

    def add_player(self, player):
        self.players_list.append(player)

    def shuffle_players(self):
        random.shuffle(self.players_list)

    def pairing_players(self):
        self.pairs = []
        if len(self.players_list) % 2 == 0:
            for i in range(0, len(self.players_list), 2):
                pair = (self.players_list[i], self.players_list[i + 1])
                self.pairs.append(pair)

        else: 
            print('il manque un joueur pour former un match supplémentaire')
                     
    def __str__(self):
        players = [p.first_name for p in self.players_list]
        pairs_str = [f'{p1.first_name} vs {p2.first_name}'
                     for (p1, p2) in self.pairs]

        return f"Players: {players} | Pairs: {pairs_str}"

player1 = Player('Edouard', 'Plastik', '5/12/1963', 'AN123456')
player2 = Player('Gerard', 'Contemporain', '12/05/1936', 'NA654321')
player3 = Player('Gaspard', 'Chitect', '3/09/1393', 'BC4657981')
player4 = Player('Baltasar', 'Delatable', '25/12/0003', 'CB649785')

manager = PlayerManager()
manager.add_player(player1)
manager.add_player(player2)
manager.add_player(player3)
manager.add_player(player4)

print(manager)

manager.shuffle_players()
print(manager)

manager.pairing_players()
print(manager)
