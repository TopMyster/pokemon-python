import random
import pypokedex # pyright: ignore[reportMissingImports]
import pygame # pyright: ignore[reportMissingImports]
import requests
from rich.console import Console
from rich.progress_bar import ProgressBar
console = Console()
user_pkmn = []
enemy_pkmn = []
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
allUserMoves = [move.name for move in curUser_pkmn.moves['scarlet-violet']]
allEnemyMoves = [move.name for move in curEnemy_pkmn.moves['scarlet-violet']]
currentUserMoveSet = random.sample(allUserMoves, min(4, len(allUserMoves)))
currentEnemyMoveSet = random.sample(allEnemyMoves, min(4, len(allEnemyMoves)))

def print_boxed(text):
    lines = text.splitlines()
    width = max(len(line) for line in lines)
    border = '+' + '-' * (width + 2) + '+'
    console.print(border)
    for line in lines:
        console.print(f"| {line.ljust(width)} |")
    console.print(border)

def getMovePower(move):
    move = move.lower().replace(" ", "-")

    url = f"https://pokeapi.co/api/v2/move/{move}"
    data = requests.get(url).json()

    return data["power"] or 40

def getMoveClass(move):
    move = move.lower().replace(" ", "-")

    url = f"https://pokeapi.co/api/v2/move/{move}"
    data = requests.get(url).json()

    return data["damage_class"]["name"]

def getMoveType(move):
    move = move.lower().replace(" ", "-")

    url = f"https://pokeapi.co/api/v2/move/{move}"
    data = requests.get(url).json()

    return data["type"]["name"]

def getMoveColor(move):
    move_type = getMoveType(move)

    if move_type == "normal":
        return "white"
    elif move_type == "fire":
        return "red"
    elif move_type == "water":
        return "blue"
    elif move_type == "grass":
        return "green"
    elif move_type == "electric":
        return "yellow"
    elif move_type == "ice":
        return "cyan"
    elif move_type == "fighting":
        return "brown"
    elif move_type == "poison":
        return "magenta"
    elif move_type == "ground":
        return "yellow"
    elif move_type == "flying":
        return "cyan"
    elif move_type == "psychic":
        return "pink"
    elif move_type == "bug":
        return "green"
    elif move_type == "rock":
        return "brown"
    elif move_type == "ghost":
        return "magenta"
    elif move_type == "dragon":
        return "blue"
    elif move_type == "steel":
        return "white"
    elif move_type == "dark":
        return "gray"
    elif move_type == "fairy":
        return "pink"
    else:
        return "white"

def useMove(user, target, move):
    global userHP, enemyHP
    if move.lower() == "recover":
        heal = int(user.base_stats.hp*0.5)
        if user == curUser_pkmn:
            userHP+=heal
            if userHP > user.base_stats.hp:
                userHP=user.base_stats.hp
            console.print(f"[bold]Your[/bold] {user.name.upper()} recovered HP!")
        else:
            enemyHP+=heal
            if enemyHP > user.base_stats.hp:
                enemyHP=user.base_stats.hp
            console.print(f"[bold]The Opponent's[/bold] {user.name.upper()} recovered HP!")
        return
    elif move.lower() in ["agility", "rock-polish", "automize"]:
        user.base_stats = user.base_stats._replace(speed=int(user.base_stats.speed * 2))
        if user == curUser_pkmn:
            console.print(f"[bold]Your[/bold] {user.name.upper()}'s speed sharply rose!")
        else:
            console.print(f"[bold]The Opponent's[/bold] {user.name.upper()}'s speed sharply rose!")
        return
    elif move.lower() == "swords-dance":
        user.base_stats = user.base_stats._replace(attack=int(user.base_stats.attack * 2))
        if user == curUser_pkmn:
            console.print(f"[bold]Your[/bold] {user.name.upper()}'s attack sharply rose!")
        else:
            console.print(f"[bold]The Opponent's[/bold] {user.name.upper()}'s attack sharply rose!")
        return
    elif move.lower() == "growl":
        target.base_stats = target.base_stats._replace(attack=int(target.base_stats.attack * 0.66))
        if target == curUser_pkmn:
            console.print(f"[bold]Your[/bold] {target.name.upper()}'s attack fell!")
        else:
            console.print(f"[bold]The Opponent's[/bold] {target.name.upper()}'s attack fell!")
        return
    elif move.lower() in ["charm", "feather-dance"]:
        target.base_stats = target.base_stats._replace(attack=int(target.base_stats.attack * 0.5))
        if target == curUser_pkmn:
            console.print(f"[bold]Your[/bold] {target.name.upper()}'s attack sharply fell!")
        else:
            console.print(f"[bold]The Opponent's[/bold] {target.name.upper()}'s attack sharply fell!")
        return
    elif move.lower() in ["tail-whip", "leer"]:
        target.base_stats = target.base_stats._replace(defense=int(target.base_stats.defense * 0.66))
        if target == curUser_pkmn:
            console.print(f"[bold]Your[/bold] {target.name.upper()}'s defense fell!")
        else:
            console.print(f"[bold]The Opponent's[/bold] {target.name.upper()}'s defense fell!")
        return
    elif move.lower() == "screech":
        target.base_stats = target.base_stats._replace(defense=int(target.base_stats.defense * 0.5))
        if target == curUser_pkmn:
            console.print(f"[bold]Your[/bold] {target.name.upper()}'s defense sharply fell!")
        else:
            console.print(f"[bold]The Opponent's[/bold] {target.name.upper()}'s defense sharply fell!")
        return
    
    power = getMovePower(move)

    move_class = getMoveClass(move)

    if move_class == "physical":
        attack_stat = user.base_stats.attack
        defense_stat = target.base_stats.defense

    elif move_class == "special":
        attack_stat = user.base_stats.sp_atk
        defense_stat = target.base_stats.sp_def

    else:
        console.print("But it failed!")
        return

    damage = int((attack_stat / defense_stat) * power / 10)

    crit_chance = random.randint(1, 24)
    
    if crit_chance == 1:
        damage = int(damage * 1.5)

    op_types = target.types

    move_type = getMoveType(move)

    type_data = requests.get(f"https://pokeapi.co/api/v2/type/{move_type}").json()
    no_damage = [t["name"] for t in type_data["damage_relations"]["no_damage_to"]]
    half_damage = [t["name"] for t in type_data["damage_relations"]["half_damage_to"]]
    double_damage = [t["name"] for t in type_data["damage_relations"]["double_damage_to"]]

    effectiveness = 1.0
    for op_type in op_types:
        if op_type in no_damage:
            effectiveness *= 0
        elif op_type in half_damage:
            effectiveness *= 0.5
        elif op_type in double_damage:
            effectiveness *= 2

    if effectiveness > 1:
        console.print("[bold yellow]It's super effective![/bold yellow]")
    elif effectiveness == 0:
        console.print("[bold dim]It doesn't affect the opponent...[/bold dim]")
    elif effectiveness < 1:
        console.print("[dim]It's not very effective...[/dim]")

    damage = int(damage * effectiveness)

    if target == curEnemy_pkmn:
        enemyHP -= damage
        console.print(f"[bold]The Opponent's[/bold] {target.name.upper()} took {damage} damage")
    else:
        userHP -= damage
        console.print(f"[bold]Your[/bold] {target.name.upper()} took {damage} damage")


def enemyAttack():
    global userHP
    if currentEnemyMoveSet:
        move = random.choice(currentEnemyMoveSet)
    else:
        move = 'tackle'
    console.print(f"\n[bold]The Opponent's [/bold]{curEnemy_pkmn.name.upper()} used {move}")
    useMove(curEnemy_pkmn, curUser_pkmn, move)

def attack():
    global userHP, enemyHP
    moves = currentUserMoveSet
    if moves:
        choices = ' '.join(f'[bold {getMoveColor(m)}][{m.replace("-", " ").capitalize()} ({idx + 1})] [/]' for idx, m in enumerate(moves))
        console.print(f"[red]Choose a Move[/red]\n{choices}")
        choice = input(">")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(moves):
                move = moves[idx]
            else:
                console.print("Please enter a number.")
                return
        elif choice in moves:
            move = choice
        else:
            console.print("Invalid move selection.")
            return
    else:
        move = "tackle"
    if curUser_pkmn.base_stats.speed > curEnemy_pkmn.base_stats.speed:
        console.print(f"\n[bold]Your[/bold] {curUser_pkmn.name.upper()} used {move}")
        useMove(curUser_pkmn,curEnemy_pkmn,move)
        enemyAttack()
        newTurn()
    else:
        enemyAttack()
        console.print(f"[bold]Your[/bold] {curUser_pkmn.name.upper()} used {move}")
        useMove(curUser_pkmn,curEnemy_pkmn,move)
        newTurn()

def overview():
    userHPBar = ProgressBar(
        total=curUser_pkmn.base_stats.hp,
        completed=userHP
    )

    enemyHPBar = ProgressBar(
        total=curEnemy_pkmn.base_stats.hp,
        completed=enemyHP
    )

    console.print(
        f"[bold]Your[/bold] {curUser_pkmn.name.upper()}:",
        userHPBar,
        f"{userHP}/{curUser_pkmn.base_stats.hp} HP"
    )

    console.print(
        f"[bold]Opponent's[/bold] {curEnemy_pkmn.name.upper()}:",
        enemyHPBar,
        f"{enemyHP}/{curEnemy_pkmn.base_stats.hp} HP"
    )
    newTurn()

def newTurn():
    if enemyHP <= 0:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/victory.mp3')
        pygame.mixer.music.play()
        boxed = (
            f"The enemy's {curEnemy_pkmn.name.upper()} fainted\n"
            "YOU WIN"
        )
        print_boxed(boxed)
        input("Press Enter to exit")
    elif userHP <= 0:
        pygame.mixer.music.stop()
        boxed = (
            f"Your {curUser_pkmn.name.upper()} fainted\n"
            "YOU LOST"
        )
        print_boxed(boxed)
        input("Press Enter to exit")
    else:
        console.print("\nWhat do you want to do?")
        console.print("[bold red]ATTACK (1)[/] [bold blue]OVERVIEW (2)[/] [bold yellow]POKEMON (3)[/]")
        play = int(input(">"))
        if play == 1:
            attack()
        elif play == 2:
            overview()
        elif play == 3:
            return


def startGame():
    pygame.mixer.music.load(f'sounds/themes/theme-{random.randint(1,9)}.mp3')
    pygame.mixer.music.play(-1)
    boxed = (
        f"[bold]The Opponent[/bold] sent out [bold]{curEnemy_pkmn.name.upper()}[/bold]\n"
        f"[bold]You[/bold] sent out [bold]{curUser_pkmn.name.upper()}[/bold]"
    )
    print_boxed(boxed)
    newTurn()

def titleScreen():
    pygame.mixer.music.load('sounds/title-screen.mp3')
    pygame.mixer.music.play(-1)
    logo = r"""
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
"""

    colored = ""

    for ch in logo:
        if ch in "#%*":
            colored += f"[bold blue]{ch}[/]"
        elif ch in "=+-":
            colored += f"[bold yellow]{ch}[/]"
        else:
            colored += ch

    console.print(colored)
    console.print("\n[bold blue]Python[/bold blue] [bold yellow]Battle Sim[/bold yellow]")  
    console.print("Enter [bold white]1[/] to start")
    start = int(input(">"))
    if start == 1:
        startGame()
    else:
        start = int(input(">"))

titleScreen()