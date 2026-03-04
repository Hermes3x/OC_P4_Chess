from models.match import Match
import datetime


class Round:
    def __init__(self, tournament, start_date=None):
        self.tournament = tournament
        self.tournament_players = tournament.tournament_players
        self.rounds_id = tournament.actual_round
        self.matchs = []
        if start_date is None:
            self.start_date = datetime.datetime.now()
        else:
            self.start_date = start_date
        self.end_date = None

    def create_matchs(self):
        """Génère les matchs du round sans aucun doublon via backtracking."""
        # Créer une copie des joueurs pour pouvoir les manipuler sans altérer la liste du tournoi
        players_pool = self.tournament_players.copy()

        def backtrack_pairing(unpaired_players):
            # Condition d'arrêt : si la liste est vide, tous les joueurs on été pairés
            if not unpaired_players:
                return []

            # On prend le premier joueur de la liste pour lui chercher un adversaire
            p1 = unpaired_players[0]

            # On teste tous les autres joueurs restants
            for i in range(1, len(unpaired_players)):
                p2 = unpaired_players[i]

                # Si p2 n'a jamais joué contre p1, c'est un match valide
                if p2.national_chess_id not in p1.opponents:

                    # On retire p1 et p2 de la liste des joueurs à apparier
                    remaining = unpaired_players[1:i] + unpaired_players[i+1:]

                    # On relance la fonction avec les joueurs restants
                    result = backtrack_pairing(remaining)

                    # Si la suite a fonctionné, on valide cette paire et on remonte le résultat
                    if result is not None:
                        return [(p1, p2)] + result

            # Si aucune combinaison ne marche pour p1, on est dans une impasse (cul-de-sac)
            return None

        # Lancement de la fonction de backtracking
        valid_pairs = backtrack_pairing(players_pool)

        # Plan B de sécurité : si le backtracking échoue (ex: dernier round, trop de matchs déjà joués
        if valid_pairs is None:
            print("Attention : Impossible de générer des paires 100% inédites. Forçage du classement...")
            valid_pairs = []
            while len(players_pool) >= 2:
                valid_pairs.append((players_pool.pop(0), players_pool.pop(0)))

        # Création effective des objets Match
        for p1, p2 in valid_pairs:
            match = Match(p1, p2)
            match.draw_color()
            self.matchs.append(match)

            p1.add_opponent(p2)
            p2.add_opponent(p1)

    def close_round(self):
        all_finished = all((m.player1_score + m.player2_score)
                           > 0
                           for m in self.matchs)
        if not all_finished:
            return

        self.end_date = datetime.datetime.now()
        return

    def __str__(self):
        match_str = "\n".join(str(match) for match in self.matchs)
        return f'Date de démarrage : {self.start_date}\n{match_str}'

    def to_dict(self):
        return {
            'round_id': self.rounds_id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date) if self.end_date else None,
            'matchs': [match.to_dict() for match in self.matchs]
            }
