# ------------------------------------------------------------------------------
# Game Rules
# ------------------------------------------------------------------------------

# See http://www.mirekw.com/ca/rullex_life.html

amoeba = {
    "S": (1, 3, 5, 8),
    "B": (3, 5, 7)
}

assimilation = {
    "S": (4, 5, 6, 7),
    "B": (3, 4, 5)
}

coagulations = {
    "S": (2, 3, 5, 6, 7, 8),
    "B": (3, 7, 8)
}

conway = {
    "S": (2, 3),
    "B": (3,)
}

coral = {
    "S": (4, 5, 6, 7, 8),
    "B": (3,)
}

day_night = {
    "S": (3, 4, 6, 7, 8),
    "B": (3, 6, 7, 8)
}

diamoeba = {
    "S": (5, 6, 7, 8),
    "B": (3, 5, 6, 7, 8)
}

flakes = {
    "S": (0, 1, 2, 3, 4, 5, 6, 7, 8),
    "B": (3,)
}

gnarl = {
    "S": (1,),
    "B": (1,)
}

high_life = {
    "S": (2, 3),
    "B": (3, 6)
}

life_34 = {
    "S": (3, 4),
    "B": (3, 4)
}

long_life = {
    "S": (5,),
    "B": (3, 4, 5)
}

maze = {
    "S": (1, 2, 3, 4, 5),
    "B": (3,)
}

mazectric = {
    "S": (1, 2, 3, 4),
    "B": (3,)
}

maze_mice = {
    "S": (1, 2, 3, 4, 5),
    "B": (3, 7)
}

move = {
    "S": (2, 4, 5),
    "B": (3, 6, 8)
}

pseudo_life = {
    "S": (2, 3, 8),
    "B": (3, 5, 7)
}

replicator = {
    "S": (1, 3, 5, 7),
    "B": (1, 3, 5, 7)
}

seeds = {
    "S": (),
    "B": (2,)
}

serviettes = {
    "S": (),
    "B": (2, 3, 4)
}

stains = {
    "S": (2, 3, 5, 6, 7, 8),
    "B": (3, 6, 7, 8)
}

two_by_two = {
    "S": (1, 2, 5),
    "B": (3, 6)
}

walled_cities = {
    "S": (2, 3, 4, 5),
    "B": (4, 5, 6, 7, 8)
}

# ------------------------------------------------------------------------------
# Rules Dictionary
# ------------------------------------------------------------------------------

rules = {
    "2x2": two_by_two,
    "34 Life": life_34,
    "Amoeba": amoeba,
    "Assimilation": assimilation,
    "Coagulations": coagulations,
    "Conway's Life": conway,
    "Coral": coral,
    "Day and Night": day_night,
    "Diamoeba": diamoeba,
    "Flakes": flakes,
    "Gnarl": gnarl,
    "High Life": high_life,
    "Long Life": long_life,
    "Maze": maze,
    "Mazectric": mazectric,
    "Maze Mice": maze_mice,
    "Move": move,
    "Pseudo Life": pseudo_life,
    "Replicator": replicator,
    "Seeds": seeds,
    "Serviettes": serviettes,
    "Stains": stains,
    "Walled Cities": walled_cities
}
