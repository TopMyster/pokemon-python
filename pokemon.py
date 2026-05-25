import random
import pypokedex
user_pkmn=[]
enemy_pkmn=[]
curUser_pkmn = user_pkmn[0]
curEnemy_pkmn = enemy_pkmn[0]
rand_dex1 = random.randint(1, 1010)
rand_dex2 = random.randint(1, 1010)
newUserPokemon = pypokedex.get(dex=rand_dex1)
newEnemyPokemon = pypokedex.get(dex=rand_dex2)
userHP = curUser_pkmn.base_stats.hp
enemyHP = curEnemy_pkmn.base_stats.hp
currentUserMoveSet = {move.name for move in curUser_pkmn.moves['scarlet-violet']}
currentEnemyMoveSet = {move.name for move in curEnemy_pkmn.moves['scarlet-violet']}

def givePkmn():
    user_pkmn.append(newUserPokemon.name)
    enemy_pkmn.append(newEnemyPokemon.name)

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

def enemyAttack():
    print(f"The opponent's {curEnemy_pkmn} used {currentEnemyMoveSet[random.randint(1,4)]}")
    userHP -= random.randint(10,60)
    print(f"Your {curUser_pkmn} took {curUser_pkmn.base_stats.hp-userHP} damage")

def attack():
    moveOptions = input(currentEnemyMoveSet[0,1])
    if curUser_pkmn.base_stats > curEnemy_pkmn.base_stats:
        print(f"Your {curUser_pkmn} used {moveOptions}")
        enemyHP -= random.randint(10,60)
        print(f"The opponent's {curEnemy_pkmn} took {curEnemy_pkmn.base_stats.hp-enemyHP} damage")
        enemyAttack()
    else: 
        enemyAttack()
        enemyHP -= random.randint(10,60)
        print(f"The opponent's {curEnemy_pkmn} took {curEnemy_pkmn.base_stats.hp-enemyHP} damage")

def newTurn():
    play = input(f"What do you want to do?\n{style.BOLD}[Attack (1)] [Pokemon (2)]{style.END}\n>")
    if play == 1:
        attack()

# Starting the Game
def startGame():
    givePkmn()
    print(f"{style.BOLD}The opponent{style.END} sent out {style.BOLD}{curEnemy_pkmn}{style.END}")
    print(f"{style.BOLD}You{style.END} sent out {style.BOLD}{curUser_pkmn}{style.END}")
    newTurn()

startGame()