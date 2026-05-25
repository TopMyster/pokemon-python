import random
import pypokedex
rand_dex = random.randint(1, 1010)
pokemon = pypokedex.get(dex=rand_dex)
print(f"You encountered {pokemon.name}")
    