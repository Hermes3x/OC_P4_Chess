import random


class Match:
    """Représente une rencontre entre deux joueurs lors d'un round"""
    def __init__(self, player1, player2):
        """Initialise un match avec deux joueurs, leurs scores à 0 et sans couleur définie"""
        self.players_pair = (player1, player2)
        self.player1_color = None
        self.player2_color = None
        self.colors = ["white", "Black"]
        self.player1_score = 0
        self.player2_score = 0
        # self.match est la structure requise par les consignes (liste de listes)
        self.match = ([player1, self.player1_score],
                      [player2, self.player2_score])

    def draw_color(self):
        """Tire au sort les couleurs (Blanc/Noir) de manière aléatoire pour les deux joueurs.
        Returns:
            str: Un message confirmant la couleur attribuée à chaque joueur"""
        random.shuffle(self.colors)
        self.player1_color = self.colors[0]
        self.player2_color = self.colors[1]
        return (f'J1 est {self.player1_color}'
                f' J2 est {self.player2_color}')

    def score(self, winner):
        """Met à jour les scores du match en fonction du résultat.
        Args:
            winner (Player ou None): L'objet Player gagnant, ou None pour une égalité.
        Returns:
            str: Une chaîne de caractères affichant le score final"""

        # Si le joueur 1 (index 0) gagne
        if self.players_pair[0] == winner:
            self.player1_score = 1.0
            self.player2_score = 0.0

        # Si le joueur 2 (index 1) gagne
        elif self.players_pair[1] == winner:
            self.player1_score = 0.0
            self.player2_score = 1.0

        # Sinon, c'est une égalité (Draw)
        else:
            self.player1_score = 0.5
            self.player2_score = 0.5

        # Mise à jour de l'attribut self.match avec les nouveaux scores
        self.match = ([self.players_pair[0], self.player1_score],
                      [self.players_pair[1], self.player2_score])
        return f'Scores du match {self.player1_score} - {self.player2_score}'

    def __str__(self):
        """Retourne une représentation textuelle du match (joueurs et score)"""
        p1, p2 = self.players_pair
        return (f"Match {p1.first_name} {p1.last_name} ({p1.national_chess_id}) vs "
                f"{p2.first_name} {p2.last_name} ({p2.national_chess_id})"
                f"\nRésultat: {self.player1_score}-{self.player2_score}")

    def to_dict(self):
        """Sérialise le match pour la sauvegarde JSON.
        Ne conserve que les IDs des joueurs, leurs scores et leurs couleurs.
        Returns:
            tuple: Contient deux listes, une pour chaque joueur"""
        p1, p2 = self.players_pair
        return ([p1.national_chess_id, self.player1_score, self.player1_color],
                [p2.national_chess_id, self.player2_score, self.player2_color])
