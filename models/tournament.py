from models.round import Round
import random


class Tournament:
    """Représente un tournoi d'échecs, gérant les joueurs, les rounds et les scores globaux."""

    def __init__(self, name, place, date, rounds_qty, note, end_date=None, players_scores=None):
        """Initialise un nouveau tournoi.
        Args:
            note (str): Les remarques générales du directeur du tournoi.
            players_scores (dict, optional): Dictionnaire des scores {ID: score}. Defaults to None"""
        self.name = name
        self.place = place
        self.date = date
        # Force le nombre de rounds à 4 comme demandé dans les spécifications par défaut
        self.rounds_qty = 4
        self.actual_round = 0
        self.rounds_list = []
        self.tournament_players = []
        self.note = note
        self.end_date = end_date
        # Initialisation du dictionnaire de suivi des scores du tournoi
        if players_scores is None:
            self.players_scores = {}
        else:
            self.players_scores = players_scores

    def add_player(self, player):
        """Ajoute un joueur au tournoi et initialise son score à 0.
        Args:
            player (Player): L'objet Player à ajouter"""
        self.tournament_players.append(player)
        if player.national_chess_id not in self.players_scores:
            self.players_scores[player.national_chess_id] = 0.0

    def create_round(self):
        """Prépare et génère le round suivant du tournoi.
        Gère le tri des joueurs (aléatoire pour le round 1, selon le classement ensuite).
        Returns:
            Round ou None: Le nouvel objet Round créé, ou None si impossible
                           (round précédent non terminé ou limite de rounds atteinte)"""

        # Vérifie si le round précédent est bien terminé
        if len(self.rounds_list) > 0:
            last_round = self.rounds_list[-1]
            if last_round.end_date is None:
                return None

        # Vérifie si le tournoi est déjà terminé
        if len(self.rounds_list) >= self.rounds_qty:
            return None

        self.actual_round += 1

        # Trie les joueurs pour l'appariement
        if self.actual_round == 1:
            random.shuffle(self.tournament_players)
        else:
            # Rounds suivants : tri par score (décroissant) puis par nom (alphabétique)
            self.tournament_players.sort(key=lambda p: (-self.players_scores[p.national_chess_id], p.last_name))

        # Création du round et de ses matchss
        current_round = Round(self)
        current_round.create_matchs()
        self.rounds_list.append(current_round)

        return current_round

    def update_players_scores_from_round(self, round_obj):
        """Met à jour le classement général du tournoi à partir des résultats d'un round terminé.
        Args:
            round_obj (Round): L'objet Round venant d'être clôturé"""
        for match in round_obj.matchs:
            p1, p2 = match.players_pair

            if p1.national_chess_id in self.players_scores:
                self.players_scores[p1.national_chess_id] += match.player1_score
            if p2.national_chess_id in self.players_scores:
                self.players_scores[p2.national_chess_id] += match.player2_score

    def __str__(self):
        """Retourne une présentation textuelle basique du tournoi."""
        return (f'Le tournoi {self.name} '
                f'se déroulera à {self.place} '
                f'le {self.date} '
                f'et se jouera en {self.rounds_qty} rounds')

    def to_dict(self):
        """Sérialise le tournoi en dictionnaire pour la sauvegarde JSON.
        Les joueurs ne sont sauvegardés que par leur ID pour éviter la duplication de données.
        Returns:
            dict: Dictionnaire complet représentant l'état actuel du tournoi"""
        return {
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "round_qty": self.rounds_qty,
            "rounds_list": [round.to_dict()
                            for round in
                            self.rounds_list],
            "players_ids": [p.national_chess_id
                            for p in
                            self.tournament_players],
            "note": self.note,
            "end_date": self.end_date,
            }
