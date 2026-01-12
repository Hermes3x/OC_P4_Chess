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
