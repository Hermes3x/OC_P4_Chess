#round = 4

class Tournament:
    def __init__(self,
                 id,
                 name,
                 place,
                 begin_date,
                 end_date,
                 tournament_nomber):
        self.id = id
        self.name = name
        self.place = place
        self.begin_date = begin_date
        self.end_date = end_date
        self.round = round
        self.tournament_nomber = tournament_nomber
        self.round_list = []
        self.players_list = {} #joueur + son score + [anciens adversaires]
        self.description = " "

        self.tournament_players_list = []
        self.pairs = []

    def __str__(self):
        return (f'{self.name} '
                f'{self.place}')
