import random
from models.players import Player


class PlayerManager:
    def __init__(self):
        self.players_list = []

    def load_players_from_json(self):
        pass

    def create_player(self, last_name,
                      first_name,
                      birth_date,
                      national_chess_id,
                      ):
        if len(self.players_list) == 0:
            player_id = 1
        else:
            player_id = self.players_list[-1].player_id + 1

        new_player = Player(last_name,
                            first_name,
                            birth_date,
                            national_chess_id,
                            player_id)

        self.players_list.append(new_player)

        return new_player

    def save_new_player_to_json(self, new_player):
        if new_player not in self.players_list:
            self.players_list.append(new_player)

    def add_player_to_tournament(self, player):
        self.tournament_players_list.append(player)

    def shuffle_tournament_players_list(self):
        random.shuffle(self.tournament_players_list)

    def pairing_rounds_players(self):
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


manager = PlayerManager()

# manager.add_player(player2)
# manager.add_player(player3)
# manager.add_player(player4)

player1 = manager.create_player('Edouard', 'Plastik', '5/12/1963', 'AN123456')
player2 = manager.create_player('Gerard', 'Contemporain', '12/05/1936', 'NA654321')
player3 = manager.create_player('Gaspard', 'Chitect', '3/09/1393', 'BC4657981')
player4 = manager.create_player('Baltasar', 'Delatable', '25/12/0003', 'CB649785')

# print(manager)
manager.add_player_to_tournament(player1)
manager.add_player_to_tournament(player2)


# manager.shuffle_players()
# print(manager)

# manager.pairing_players()
# print(manager)
