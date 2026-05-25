import random
import pypokedex

user_pkmn = []
enemy_pkmn = []
curUser_pkmn = None
curEnemy_pkmn = None
userHP = None
enemyHP = None
currentUserMoveSet = []
currentEnemyMoveSet = []

class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def givePkmn():
    global curUser_pkmn, curEnemy_pkmn, userHP, enemyHP, currentUserMoveSet, currentEnemyMoveSet

    rand_dex1 = random.randint(1, 1010)
    rand_dex2 = random.randint(1, 1010)
    newUserPokemon = pypokedex.get(dex=rand_dex1)
    newEnemyPokemon = pypokedex.get(dex=rand_dex2)

    user_pkmn.append(newUserPokemon)
    enemy_pkmn.append(newEnemyPokemon)

    curUser_pkmn = user_pkmn[0]
    curEnemy_pkmn = enemy_pkmn[0]
    userHP = curUser_pkmn.base_stats.hp
    enemyHP = curEnemy_pkmn.base_stats.hp
    currentUserMoveSet = [move.name for move in curUser_pkmn.moves['scarlet-violet']]
    currentEnemyMoveSet = [move.name for move in curEnemy_pkmn.moves['scarlet-violet']]


def enemyAttack():
    global userHP
    move = random.choice(currentEnemyMoveSet)
    print(f"The opponent's {curEnemy_pkmn.name} used {move}")
    userHP -= random.randint(10, 60)
    print(f"Your {curUser_pkmn.name} took {curUser_pkmn.base_stats.hp - userHP} damage")
    newTurn()


def attack():
    global enemyHP
    moves_text = ', '.join(currentUserMoveSet[:4])
    moveOptions = input(f"Choose a move ({moves_text}): \n>")
    if curUser_pkmn.base_stats.hp > curEnemy_pkmn.base_stats.hp:
        print(f"Your {curUser_pkmn.name} used {moveOptions}")
        enemyHP -= random.randint(10, 60)
        print(f"The opponent's {curEnemy_pkmn.name} took {curEnemy_pkmn.base_stats.hp - enemyHP} damage")
        enemyAttack()
    else:
        enemyAttack()
        enemyHP -= random.randint(10, 60)
        print(f"The opponent's {curEnemy_pkmn.name} took {curEnemy_pkmn.base_stats.hp - enemyHP} damage")
        newTurn()


def newTurn():
    if enemyHP == 0:
        print(f"The enemy's {curEnemy_pkmn.name} fainted")
    elif userHP == 0:
        print(f"Your {curUser_pkmn.name} fainted")
    else:
        play = input(f"What do you want to do?\n{style.BOLD}[Attack (1)] [Pokemon (2)]{style.END}\n>")
        if play == '1':
            attack()


# Starting the Game
def startGame():
    givePkmn()
    print(f"{style.BOLD}The opponent{style.END} sent out {style.BOLD}{curEnemy_pkmn.name}{style.END}")
    print(f"{style.BOLD}You{style.END} sent out {style.BOLD}{curUser_pkmn.name}{style.END}")
    newTurn()

startGame()