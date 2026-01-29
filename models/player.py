class Player:
    def __init__(self, first_name,
                 last_name,
                 birth_date,
                 national_chess_id,
                 score):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id
        self.score = 0  # dans tournoi?
        self.opponents = []  # liste des IDs déjà joués # dans tournoi

    def add_opponent(self, opponent):
        self.opponents.append(opponent.national_chess_id)

    def __str__(self):
        return (f'{self.last_name}'
                f' {self.first_name}'
                f' {self.birth_date}'
                f' {self.national_chess_id}'
                f' {self.score}'
                f' {self.opponents}')

    def to_dict(self):
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "birth_date": self.birth_date,
                "national_chess_id": self.national_chess_id,
                }

    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            national_chess_id=data['national_chess_id'],
            score=0
        )
