import random
import pypokedex # pyright: ignore[reportMissingImports]
import pygame # pyright: ignore[reportMissingImports]
import requests
from rich.console import Console
from rich.progress_bar import ProgressBar
from rich.panel import Panel
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

currEnemyPoisoned = False
currUserPoisoned = False
currEnemyBurned = False
currUserBurned = False

userStatusEffects = []
enemyStatusEffects = []

battle_log = []

def print_boxed(text, color="blue"):
    console.print(Panel(text, border_style=color, expand=False))

def battle_dialogue(text, color="blue"):
    battle_log.append(text)
    print_boxed(text, color)
    return

def safe_get_json(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        if not r.text.strip():
            return None
        return r.json()
    except:
        return None

def getMovePower(move):
    move = move.lower().replace(" ", "-")
    url = f"https://pokeapi.co/api/v2/move/{move}"
    data = safe_get_json(url)
    return data["power"] if data and data.get("power") else 40

def getMoveClass(move):
    move = move.lower().replace(" ", "-")
    url = f"https://pokeapi.co/api/v2/move/{move}"
    data = safe_get_json(url)
    return data["damage_class"]["name"] if data else "physical"

def getMoveType(move):
    move = move.lower().replace(" ", "-")
    url = f"https://pokeapi.co/api/v2/move/{move}"
    data = safe_get_json(url)
    return data["type"]["name"] if data else "normal"

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
        return "dark_orange"
    elif move_type == "poison":
        return "magenta"
    elif move_type == "ground":
        return "yellow"
    elif move_type == "flying":
        return "cyan"
    elif move_type == "psychic":
        return "hot_pink"
    elif move_type == "bug":
        return "green"
    elif move_type == "rock":
        return "sandy_brown"
    elif move_type == "ghost":
        return "purple"
    elif move_type == "dragon":
        return "blue"
    elif move_type == "steel":
        return "grey50"
    elif move_type == "dark":
        return "grey37"
    elif move_type == "fairy":
        return "hot_pink"
    else:
        return "white"
    
def poisonTarget(target):
    global currEnemyPoisoned, currUserPoisoned, userStatusEffects, enemyStatusEffects
    if target == curUser_pkmn:
        currUserPoisoned = True
        userStatusEffects.append("[bold magenta]Poisoned[/]")
    elif target == curEnemy_pkmn:
        currEnemyPoisoned = True
        enemyStatusEffects.append("[bold magenta]Poisoned[/]")
    

def burnTarget(target):
    global currEnemyBurned, currUserBurned
    if target == curUser_pkmn:
        currUserBurned = True
        userStatusEffects.append("[bold red]Burned[/]")
    elif target == curEnemy_pkmn:
        currEnemyBurned = True
        enemyStatusEffects.append("[bold red]Burned[/]")

def useMove(user, target, move):
    global userHP, enemyHP, currEnemyPoisoned, currUserPoisoned, currEnemyBurned, currUserBurned
    if move.lower() == "recover":
        heal = int(user.base_stats.hp*0.5)
        if user == curUser_pkmn:
            userHP+=heal
            if userHP > user.base_stats.hp:
                userHP=user.base_stats.hp
            battle_dialogue(f"[bold cyan]Your {user.name.upper()}[/] recovered HP!", "dim")
        else:
            enemyHP+=heal
            if enemyHP > user.base_stats.hp:
                enemyHP=user.base_stats.hp
            battle_dialogue(f"[bold]The Opponent's[/bold] {user.name.upper()} recovered HP!", "dim")
        return
    elif move.lower() in ["agility", "rock-polish", "automize"]:
        user.base_stats = user.base_stats._replace(speed=int(user.base_stats.speed * 2))
        if user == curUser_pkmn:
            battle_dialogue(f"[bold cyan]Your {user.name.upper()}'s[/] speed sharply rose!", "dim")
        else:
            battle_dialogue(f"[bold]The Opponent's[/bold] {user.name.upper()}'s speed sharply rose!", "dim")
        return
    elif move.lower() == "swords-dance":
        user.base_stats = user.base_stats._replace(attack=int(user.base_stats.attack * 2))
        if user == curUser_pkmn:
            battle_dialogue(f"[bold cyan]Your {user.name.upper()}'s[/] attack sharply rose!", "dim")
        else:
            battle_dialogue(f"[bold]The Opponent's[/bold] {user.name.upper()}'s attack sharply rose!", "dim")
        return
    elif move.lower() == "growl":
        target.base_stats = target.base_stats._replace(attack=int(target.base_stats.attack * 0.66))
        if target == curUser_pkmn:
            battle_dialogue(f"[bold cyan]Your {target.name.upper()}'s[/] attack fell!", "dim")
        else:
            battle_dialogue(f"[bold]The Opponent's[/bold] {target.name.upper()}'s attack fell!", "dim")
        return
    elif move.lower() in ["charm", "feather-dance"]:
        target.base_stats = target.base_stats._replace(attack=int(target.base_stats.attack * 0.5))
        if target == curUser_pkmn:
            battle_dialogue(f"[bold cyan]Your {target.name.upper()}'s[/] attack sharply fell!", "dim")
        else:
            battle_dialogue(f"[bold]The Opponent's[/bold] {target.name.upper()}'s attack sharply fell!", "dim")
        return
    elif move.lower() in ["tail-whip", "leer"]:
        target.base_stats = target.base_stats._replace(defense=int(target.base_stats.defense * 0.66))
        if target == curUser_pkmn:
            battle_dialogue(f"[bold cyan]Your {target.name.upper()}'s[/] defense fell!", "dim")
        else:
            battle_dialogue(f"[bold]The Opponent's[/bold] {target.name.upper()}'s defense fell!", "dim")
        return
    elif move.lower() == "screech":
        target.base_stats = target.base_stats._replace(defense=int(target.base_stats.defense * 0.5))
        if target == curUser_pkmn:
            battle_dialogue(f"[bold cyan]Your {target.name.upper()}'s[/] defense sharply fell!", "dim")
        else:
            battle_dialogue(f"[bold]The Opponent's[/bold] {target.name.upper()}'s defense sharply fell!", "dim")
        return
    elif move.lower() in ["toxic", "poison-gas", "poison-powder", "toxic-spikes", "poison-thread"]:
        poisonTarget(target)
        battle_dialogue(f"{target.name.upper()} was poisoned!", "magenta")
        return

    elif move.lower() in ["will-o-wisp", "sacred-fire", "inferno", "burning-jealousy"]:
        burnTarget(target)
        battle_dialogue(f"{target.name.upper()} was burned!", "red")
        return
    if "steel" not in target.types:
        if currEnemyPoisoned:
            enemyPoisonDamage=enemyHP*.125
            enemyHP-=enemyPoisonDamage
            battle_dialogue(f"[bold]The Opponent's[/bold] {target.name.upper()} is poisoned and lost [bold red]{enemyPoisonDamage}[/]", "magenta")
        elif currUserPoisoned:
            userPoisonDamage=userHP*.125
            userHP-=userPoisonDamage
            battle_dialogue(f"[bold]Your[/bold] {target.name.upper()} is poisoned and lost [bold red]{userPoisonDamage}[/]", "magenta")

    if currEnemyBurned:
        enemyBurnDamage=enemyHP*.0625
        enemyHP-=enemyBurnDamage
        battle_dialogue(f"[bold]The Opponent's[/bold] {target.name.upper()} is burned and lost [bold red]{enemyBurnDamage}[/]", "red")
    elif currUserBurned:
        userBurnDamage=userHP*.0625
        userHP-=userBurnDamage
        battle_dialogue(f"[bold]Your[/bold] {target.name.upper()} is burned and lost [bold red]{userBurnDamage}[/]", "red")
    
    power = getMovePower(move)

    move_class = getMoveClass(move)

    if move_class == "physical":
        attack_stat = user.base_stats.attack
        defense_stat = target.base_stats.defense

    elif move_class == "special":
        attack_stat = user.base_stats.sp_atk
        defense_stat = target.base_stats.sp_def

    else:
        battle_dialogue("But it failed!", "dim")
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
        battle_dialogue("[bold yellow]It's super effective![/bold yellow]", "yellow")
    elif effectiveness == 0:
        battle_dialogue("[bold dim]It doesn't affect the opponent...[/bold dim]", "dim")
    elif effectiveness < 1:
        battle_dialogue("[dim]It's not very effective...[/dim]", "dim")

    damage = int(damage * effectiveness)

    if target == curEnemy_pkmn:
        enemyHP -= damage
        battle_dialogue(f"[bold]The Opponent's[/bold] {target.name.upper()} took [bold red]{damage}[/] damage", "red")
    else:
        userHP -= damage
        battle_dialogue(f"[bold cyan]Your {target.name.upper()}[/] took [bold red]{damage}[/] damage", "red")


def enemyAttack():
    global userHP
    if currentEnemyMoveSet:
        move = random.choice(currentEnemyMoveSet)
    else:
        move = '[bold white]Tackle[/]'
    battle_dialogue(f"[bold]The Opponent's [/bold]{curEnemy_pkmn.name.upper()} used [bold {getMoveColor(move)}]{move.replace('-', ' ').capitalize()}[/]")
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
                battle_dialogue("Please enter a number.")
                return
        elif choice in moves:
            move = choice
        else:
            battle_dialogue("Invalid move selection.")
            return
    else:
        move = "[bold white]Tackle[/]"
    if curUser_pkmn.base_stats.speed > curEnemy_pkmn.base_stats.speed:
        battle_dialogue(f"[bold cyan]Your {curUser_pkmn.name.upper()}[/] used [bold {getMoveColor(move)}]{move.replace('-', ' ').capitalize()}[/]", "blue")
        useMove(curUser_pkmn,curEnemy_pkmn,move)
        enemyAttack()
        newTurn()
    else:
        enemyAttack()
        battle_dialogue(f"[bold cyan]Your {curUser_pkmn.name.upper()}[/] used {move.replace("-", " ").capitalize()}", color="blue")
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
        f"[bold cyan]Your {curUser_pkmn.name.upper()}[/] ({', '.join(userStatusEffects)}):",
        userHPBar,
        f"{userHP}/{curUser_pkmn.base_stats.hp} HP"
    )

    console.print(
        f"[bold]Opponent's {curEnemy_pkmn.name.upper()}[/] ({', '.join(enemyStatusEffects)}):",
        enemyHPBar,
        f"{enemyHP}/{curEnemy_pkmn.base_stats.hp} HP"
    )
    newTurn()

def newTurn():
    if enemyHP <= 0:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sounds/victory.mp3')
        pygame.mixer.music.play()
        battle_dialogue(f"[bold]The Opponent's[/bold] {curEnemy_pkmn.name.upper()} fainted\nYOU WIN", "green")
        console.print("Press Enter to exit or [bold cyan]1[/] for the battle log\n")
        option = input(">")
        if option == "1":
            for line in battle_log:
                console.print(line)
            input("Press Enter to exit")
        else:
            return

    elif userHP <= 0:
        pygame.mixer.music.stop()
        battle_dialogue(f"[bold cyan]Your {curUser_pkmn.name.upper()}[/] fainted\nYOU LOST", "red")
        console.print("Press Enter to exit or [bold cyan]1[/] for the battle log\n")
        option = input(">")
        if option == "1":
            for line in battle_log:
                console.print(line)
            input("Press Enter to exit")
        else:
            return
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
    battle_dialogue(f"[bold]The Opponent[/bold] sent out [bold]{curEnemy_pkmn.name.upper()}[/bold]\n"
        f"[bold cyan]You[/] sent out [bold]{curUser_pkmn.name.upper()}[/bold]", color="blue")
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