import random
from models.players import Player


class Match:
    def __init__(self,
                 player1,
                 player2,
                 ):
        self.status = "En_attente"
        self.player1 = player1
        self.player2 = player2
        self.draw_colors()
        self.match_result = None

    def draw_colors(self):
        random_color = random.randint(0, 1)

        if random_color == 1:
            self.player1_color = "White"
            self.player2_color = "Black"

        else:
            self.player1_color = "Black"
            self.player2_color = "White"

    def set_match_result(self, player1_score, player2_score):
        self.match_result = (player1_score, player2_score)
        self.status = "terminé"
        self.player1.score += player1_score
        self.player2.score += player2_score

    def __str__(self):
        if self.match_result is None:
            match_result_str = "Le match n'est pas commencé"

        else:
            match_result_str = f"{self.match_result[0]}-{self.match_result[1]}"

        return (f"Match : {self.player1.first_name} ({self.player1_color}) "
                f"vs {self.player2.first_name} ({self.player2_color}) | "
                f"Résultat : {match_result_str} | Statut : {self.status}")


player1 = Player('Edouard', 'Plastik', '5/12/1963', 'AN123456', 1) 
player2 = Player('Gerard', 'Contemporain', '12/05/1936', 'NA654321', 2)

match1 = Match(player1, player2)
match1.set_match_result(1, 0)

print(match1)