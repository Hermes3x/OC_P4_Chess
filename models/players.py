class Player:
    def __init__(self, first_name,
                 last_name,
                 birth_date,
                 national_chess_id):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id

    def __str__(self):
        return (f'{self.last_name}'
                f' {self.first_name}'
                f' {self.birth_date}'
                f' {self.national_chess_id}')
