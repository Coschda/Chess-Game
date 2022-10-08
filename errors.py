class ChessError(Exception):
    pass

class BadMoveError(ChessError):
    """Appelée quand un coup n'est pas bon ou pas valide."""
    def __str__(self):
        return "Le coup entré n'est pas valide."

class TwoPossibleError(ChessError):
    def __str__(self):
        return "Deux pièces peuvent faire le même coup."

class VraimentBizarre(ChessError):
    def __str__(self):
        return "Alors t'es pas censé voir ça"