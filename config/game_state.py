class GameState:
    # количество съеденной еды
    eaten_food = 0

    # все приведения
    ghosts = []
    # анимация курсора (глаз)
    eyes = []
    # тексты
    texts = []

    pman = None

    max_score = 0

    score = None

    bs, bp, hm = None, None, None
