import random
import pypokedex # pyright: ignore[reportMissingImports]
import pygame # pyright: ignore[reportMissingImports]
user_pkmn = []
enemy_pkmn = []
currentUserMoveSet = []
currentEnemyMoveSet = []
pygame.mixer.init()
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

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

def enemyAttack():
    global userHP
    if currentEnemyMoveSet:
        move = random.choice(currentEnemyMoveSet)
    else:
        move = 'Tackle'
    print(f"\n{style.BOLD}The opponent's{style.END} {curEnemy_pkmn.name.upper()} used {move}")
    userHP -= random.randint(10, 40)
    print(f"{style.BOLD}Your{style.END} {curUser_pkmn.name.upper()} took {curUser_pkmn.base_stats.hp - userHP} damage")


def attack():
    global enemyHP
    moves = currentUserMoveSet[:4]
    if moves:
        choices = ' '.join(f'[{m}]' for m in moves)
        choice = input(f"Choose a move {style.BOLD}{choices}{style.END}\n>")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(moves):
                move = moves[idx]
            else:
                print("Please enter a number.")
                return
        elif choice in moves:
            move = choice
        else:
            print("Invalid move selection.")
            return
    else:
        move = "Tackle"
    if curUser_pkmn.base_stats.speed > curEnemy_pkmn.base_stats.speed:
        print(f"\n{style.BOLD}Your{style.END} {curUser_pkmn.name.upper()} used {move}")
        enemyHP -= random.randint(10, 40)
        print(f"{style.BOLD}The opponent's{style.END} {curEnemy_pkmn.name.upper()} took {curEnemy_pkmn.base_stats.hp - enemyHP} damage")
        enemyAttack()
        newTurn()
    else:
        enemyAttack()
        print(f"{style.BOLD}Your{style.END} {curUser_pkmn.name.upper()} used {move}")
        enemyHP -= random.randint(10, 40)
        print(f"{style.BOLD}The opponent's{style.END} {curEnemy_pkmn.name.upper()} took {curEnemy_pkmn.base_stats.hp - enemyHP} damage")
        newTurn()

def overview():
    print(
        f"""
        \n{style.BOLD}Your{style.END} {curUser_pkmn.name.upper()}: {userHP}HP
        \n{style.BOLD}Opponnent's{style.END} {curEnemy_pkmn.name.upper()}: {enemyHP}HP
        """
    )
    newTurn()

def newTurn():
    if enemyHP <= 0:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/victory.mp3')
        pygame.mixer.music.play()
        print(f"The enemy's {curEnemy_pkmn.name.upper()} fainted")
        print("YOU WIN")
        input("Press Enter to exit")
    elif userHP <= 0:
        pygame.mixer.music.stop()
        print(f"Your {curUser_pkmn.name.upper()} fainted")
        print("YOU LOST")
        input("Press Enter to exit")
    else:
        play = int(input(f"\nWhat do you want to do?\n{style.BOLD}[ATTACK (1)] [OVERVIEW (2)] [POKEMON (3)]{style.END}\n>"))
        if play == 1:
            attack()
        elif play == 2:
            overview()


def startGame():
    pygame.mixer.music.load('sounds/battle.mp3')
    pygame.mixer.music.play(-1)
    print(f"{style.BOLD}The opponent{style.END} sent out {style.BOLD}{curEnemy_pkmn.name.upper()}{style.END}")
    print(f"{style.BOLD}You{style.END} sent out {style.BOLD}{curUser_pkmn.name.upper()}{style.END}")
    newTurn()

def titleScreen():
    pygame.mixer.music.load('sounds/title-screen.mp3')
    pygame.mixer.music.play(-1)
    print(
        """                        
                             ##*=+*#                        
    ##**#####     #*#**##*# %#*+*## %**##***#   %##         
 #***+==-==+**#  %#+=-**==**#******##*==*+-+#   %#****##### 
%#*------==--*#  ###=-+=--=*+-***-+##=--+=-=*#####*--+#*=+*#
 %#*+=--=***-+##***#+---=*#*-+#*=**##------=**++=+*=-=*+-=*#
  ##%*=--+#==#=+*-==*=--==**+---=--+*=-+-==*==#**++*--*--*# 
    %%*---=*#*-=***-*+=**=-=******##+-=#**+*=-===-*++---=#  
     %#*--+#%*-----+*==#%%#**==#%%%%#**%##*+**==**==*--=*#  
     %%#+-=*#%#***#%#**#  %%%%###    %%%%%#***#%%#**#--+#   
      %%#==*# %%%% %%%%       %%          %%%%% %%%%#++##   
       %%#%%%
        Python Battle Sim\n       
        """
    )
    start = int(input("Enter 1 to Start\n>"))
    if start == 1:
        startGame()
    else:
        start = input("Enter 1 to Start")

titleScreen()