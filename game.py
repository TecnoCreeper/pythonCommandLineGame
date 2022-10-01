import random
import os
import time

class Player:
    def __init__(self, job, health, base_damage, armor, bonus_damage):
        self.job = job
        self.health = health
        self.base_damage = base_damage
        self.armor = armor
        self.bonus_damage = bonus_damage


class Monster:
    def __init__(self, element, health, base_damage, armor):
        self.element = element
        self.health = health
        self.base_damage = base_damage
        self.armor = armor


def menu():
    print("----------\nWelcome to Dragon Slayer\n")
    try:
        h = open("highscore.txt", "r")
    except FileNotFoundError:
        c = open("highscore.txt", "w")
        c.write("0")
        c.close()
    h = open("highscore.txt", "r")
    x = h.readline()
    print(f"Highscore: {x}")
    print("Press ENTER to start")
    input()
    next = False
    # ask job until valid and set job
    while (next == False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Choose your job:\n1 - Warrior\n2 - Thief\n3 - Archer")
        x = input()
        if x.isdigit():
            job_selection = int(x)
            if (job_selection == 1):
                p1.job = "Warrior"
                next = True
                continue
            elif (job_selection == 2):
                p1.job = "Thief"
                next = True
                continue
            elif (job_selection == 3):
                p1.job = "Archer"
                next = True
                continue
    else:
        print("----------\nJob selected!\n----------")


def set_p1_stats():
    global max_health
    if (p1.job == "Warrior"):
        p1.health = 125
        p1.base_damage = 15
        p1.armor = 15
    elif (p1.job == "Thief"):
        p1.health = 100
        p1.base_damage = 30
        p1.armor = 5
    elif (p1.job == "Archer"):
        p1.health = 150
        p1.base_damage = 15
        p1.armor = 10
    max_health = p1.health
    p1.bonus_damage = 0


def m1_generation():
    #random monster element
    m_elements = ("fire", "earth", "electro")
    m_element = random.choice(m_elements)
    m1.element = m_element
    #scaling random stats
    m1.health = random.randint(50, 150) * floor // 3
    m1.base_damage = random.randint(10, 50) * floor // 3
    #monster effects
    a = 0
    if (m1.element == "Earth"):
        a = int(5 * floor / 2)
    m1.armor = a



def combat():
    global floor
    next = False
    #generate monster
    m1_generation()
    #combat loop
    while (next == False): 
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"----------\nFloor {floor}\n----------\n")
        print("A monster appeared!\n")
        print(f"Your stats:\t\t\tMonster stats:\nHealth: {p1.health}\t\t\tHealth: {m1.health}\nDamage: {p1.base_damage + p1.bonus_damage}\t\t\tDamage: {m1.base_damage}\nArmor: {p1.armor}\t\t\tArmor: {m1.armor}")
        #Implement multiple attacks here (new func, choose you attack, mana / special)
        print("\n----------\nPress ENTER to attack")
        input()
        #calculate monster health after attack
        m1.health = m1.health - ((p1.base_damage + p1.bonus_damage) - m1.armor)
        #check if monster is dead
        if (m1.health <= 0):
            next = True
            print("\n----------\nYou defeated the monster!")
            continue
        #check if damage taken by player is > 0
        dmg_taken = (m1.base_damage - p1.armor)
        if (dmg_taken > 0):
            p1.health = p1.health - dmg_taken
        #check if player is dead
        if (p1.health <= 0):
            lost()
    #when monster is dead
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        floor = floor + 1
        regen()
        time.sleep(1)
        bonus_selection()
        combat()



def regen():
    #regenerate health
    p1.health = p1.health + int((p1.health * 0.3))
    if (p1.health > max_health):
        p1.health = max_health
    print("----------\nHealth regenerated!")



def bonus_selection():
    global max_health
    #bonuses random extraction
    bonuses = ["max health", "damage", "armor"]
    bonuses_choices = random.sample(bonuses, 3)
    b1 = bonuses_choices[0] #b1, b2, b3 are basically aliases
    b2 = bonuses_choices[1]
    b3 = bonuses_choices[2]
    #select bonus until valid
    next = False
    while(next == False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------\nChoose a bonus:\n")
        print(f"1 - {b1.title()} bonus\n2 - {b2.title()} bonus\n3 - {b3.title()} bonus")
        x = input()
        if x.isdigit():
            b_selection = int(x)
            if (b_selection == 1 or b_selection == 2 or b_selection == 3):
                next = True
                continue
    else:
        print("\n----------\nBonus selected\n----------\n")
        time.sleep(1)
    #bonus assign
    if (b_selection == 1):
        b_selection = b1
    elif (b_selection == 2):
        b_selection = b2
    elif (b_selection == 3):
        b_selection = b3
    #bonus adding - probably a better way to do this maybe dictionary (?)
    if (b_selection == "max health"):
        max_health = max_health + 15
    elif (b_selection == "damage"):
        p1.bonus_damage = p1.bonus_damage + 5
    elif (b_selection == "armor"):
        p1.armor = p1.armor + 5



def lost():
    global dead
    print("You died :(")
    dead = True
    print(f"You defeated {floor} monsters")
    #save if highscore
    r = open("highscore.txt", "r")
    x = int(r.readline())
    if (floor > x):
        h = open("highscore.txt", "w")
        h.write(str(floor))
        h.close()
        print("New highscore!")
    print("Press ENTER to restart")
    input()
    game()



#game
def game():
    # Initialize stuff
    os.system('cls' if os.name == 'nt' else 'clear')
    global p1
    global m1
    global floor
    global max_health
    global dead
    p1 = Player("0", 0, 0, 0, 0)
    m1 = Monster("0", 0, 0, 0)
    floor = 1
    max_health = 0
    dead = False
    menu()
    while (dead == False):
        set_p1_stats()
        combat()


p1 = Player("0", 0, 0, 0, 0)
m1 = Monster("0", 0, 0, 0)
floor = 1
max_health = 0
dead = False
game()