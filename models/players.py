class Player:
    def __init__(self, last_name,
                 first_name,
                 birth_date,
                 national_chess_id,
                 player_id):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id
        self.player_id = player_id
        self.score = 0
        self.opponent = []

    def __str__(self):
        return (f'Identité du joueur : {self.last_name} '
                f'{self.first_name} | '
                f'Identifiant National : {self.national_chess_id} | '
                f'Score : {self.score} | '
                f'Player ID: {self.player_id}')

    def __repr__(self):
        return (f'Player({self.first_name!r},{self.last_name!r})')

    def add_point(self, points):
        """Ajoute des points au score du joueur : 0.5 ou 1"""
        self.score += points
