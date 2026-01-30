class TournamentView:
    def get_tournament_data(self):
        print("Veuillez renseigner les informations du tournoi")
        name = input("Nom du tournoi : ")
        place = input("Lieu : ")
        date = input("Date (jj/mm/aaaa) : ")
        rounds = 4  # on fixe à 4 pour coller à l’énoncé
        note = input("Note / description : ")

        return {"name": name,
                "place": place,
                "date": date,
                "round_qty": rounds,
                "note": note,
                }

    def get_tournament_players_from_json(self):
        print("Veuillez inscrire les joueurs qui participeront à votre tournoi")
        load_players = input("Ajouter les joueurs depuis un fichier .json ? Y/n")

        return load_players

    def ask_add_player_manually(self):
        add_player = input("Souhaitez vous ajouter un joueur manuellement ? Y/n")

        return add_player

    def get_new_player_info(self):
        print("---Ajout d'un nouveau joueur---")
        first_name = input("Prénom :")
        last_name = input("Nom :")
        birth_date = input("Date de naissance : ")
        chess_id = input("ID Chess (AB12345) : ")
        return {
            "first_name": first_name,
            "last_name": last_name, 
            "birth_date": birth_date, 
            "national_chess_id": chess_id
            }
