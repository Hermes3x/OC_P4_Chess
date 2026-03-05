class Player:
    """Représente un joueur d'échecs avec ses données personnelles et son historique d'affrontements."""

    def __init__(self, first_name,
                 last_name,
                 birth_date,
                 national_chess_id,
                 ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id
        # Historique des adversaires pour éviter les matchs répétés au sein d'un tournoi
        self.opponents = []

    def add_opponent(self, opponent):
        """Enregistre un adversaire pour éviter une revanche future dans le même tournoi.
        Args:
            opponent (Player): L'objet Player de l'adversaire"""
        self.opponents.append(opponent.national_chess_id)

    def __str__(self):
        """Retourne une représentation textuelle du joueur pour l'affichage."""
        return (f'{self.last_name}'
                f' {self.first_name}'
                f' {self.birth_date}'
                f' {self.national_chess_id}'
                f' {self.opponents}')

    def to_dict(self):
        """Sérialise le joueur en dictionnaire pour la sauvegarde JSON.
        Note: L'historique des adversaires (self.opponents) n'est pas sauvegardé ici
        car il est spécifique à un tournoi. Il est géré par le DatabaseController.
        Returns:
            dict: Dictionnaire contenant les informations du joueur"""
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "birth_date": self.birth_date,
                "national_chess_id": self.national_chess_id,
                }

    @classmethod
    def from_dict(cls, data):
        """Désérialise un joueur depuis un dictionnaire JSON.
        Args:
            data (dict): Dictionnaire contenant les clés first_name, last_name,
                        birth_date, national_chess_id.
        Returns:
            Player: Nouvel objet Player reconstruit à partir des données"""
        return cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            birth_date=data['birth_date'],
            national_chess_id=data['national_chess_id'],
            )
