import math

def calcular_probabilidad(rating_a, rating_b):
    """
    Calcula la probabilidad esperada de que A gane contra B.
    Formula: 1 / (1 + 10 ^ ((Rb - Ra) / 400))
    """
    return 1.0 / (1 + math.pow(10, (rating_b - rating_a) / 400))

def nuevo_rating(rating_actual, score_real, probabilidad, k_factor=32):
    """
    Calcula el nuevo rating ELO.
    R' = R + K * (S - E)
    """
    nuevo = rating_actual + k_factor * (score_real - probabilidad)
    return round(nuevo)
