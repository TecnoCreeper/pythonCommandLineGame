import random
import os
import time



class Player:
    def __init__(self, job, max_health, health, base_damage, armor, bonus_damage, crit_chance, evasion_chance):
        self.job = job
        self.max_health = max_health
        self.health = health
        self.base_damage = base_damage
        self.armor = armor
        self.bonus_damage = bonus_damage
        self.crit_chance = crit_chance
        self.evasion_chance = evasion_chance


class Monster:
    def __init__(self, element, health, base_damage, armor, burn, stun):
        self.element = element
        self.health = health
        self.base_damage = base_damage
        self.armor = armor
        self.burn = burn
        self.stun = stun



def menu():
    print("----------\nWelcome to Dragon Slayer")
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



def set_p1_stats():
    # ask job until valid and set job
    job_selection = 0
    while (job_selection != "1" and job_selection != "2" and job_selection != "3"):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Choose your job:\n1 - Warrior\n2 - Thief\n3 - Archer")
        job_selection = input()
    else:
        if (job_selection == "1"):
            job_selection = "Warrior"
        elif (job_selection == "2"):
            job_selection = "Thief"
        elif (job_selection == "3"):
            job_selection = "Archer"
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------\nJob selected!")
    
    if (job_selection == "Warrior"):
        p1.health = 150
        p1.base_damage = 15
        p1.armor = 20
        p1.crit_chance = 10
        p1.evasion_chance = 5
    elif (p1.job == "Thief"):
        p1.health = 100
        p1.base_damage = 30
        p1.armor = 5
        p1.crit_chance = 20
        p1.evasion_chance = 15
    elif (p1.job == "Archer"):
        p1.health = 150
        p1.base_damage = 15
        p1.armor = 10
        p1.crit_chance = 15
        p1.evasion_chance = 10
    p1.max_health = p1.health



def m1_generation():
    global BURN_DMG
    global BURN_CHANCE
    global burn_turns
    global STUN_CHANCE

    #random monster element
    m_elements = ("fire", "earth", "electro")
    m_element = random.choice(m_elements)
    m1.element = m_element

    #scaling random stats
    m1.health = random.randint(50, 100) * floor // 3
    m1.base_damage = random.randint(10, 40) * floor // 3

    #monster effects
    #fire / burn
    if (m1.element == "fire"):
        m1.burn = True
        BURN_DMG = 10
        BURN_CHANCE = 15
        burn_turns = 0
    else:
        m1.burn = False

    #earth / armor
    if (m1.element == "earth"):
        m1.armor = int(floor * 5 / 2)
    else:
        m1.armor = 0

    #electro / stun
    if (m1.element == "electro"):
        m1.stun = True
        STUN_CHANCE = 15
    else:
        m1.stun = False



def display_stats():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"----------\nFloor {floor}\n----------\n")
    print("A monster appeared!\n")
    if (m1.armor > 0):
        print(f"Your stats:\t\t\t{m1.element.title()} monster stats:\nHealth: {p1.health}\t\t\tHealth: {m1.health}\nDamage: {p1.base_damage + p1.bonus_damage}\t\t\tDamage: {m1.base_damage}\nArmor: {p1.armor}\t\t\tArmor: {m1.armor}")
    else:
        print(f"Your stats:\t\t\t{m1.element.title()} monster stats:\nHealth: {p1.health}\t\t\tHealth: {m1.health}\nDamage: {p1.base_damage + p1.bonus_damage}\t\t\tDamage: {m1.base_damage}\nArmor: {p1.armor}")
    if (player_burnt == True):
        print(f"Burn turns left: {burn_turns}")
    if (player_stunned == True):
        print("Stunned!")
    print("----------")


def crit_roll():
    global player_damage
    #crit roll
    CRIT_MULT = 1.5
    if (random.randint(1,100) <= p1.crit_chance):
        crit = True
    else:
        crit = False

    #calculate damage
    if (crit == True):
        player_damage = int((p1.base_damage + p1.bonus_damage) * CRIT_MULT)
        print("Critical attack!")
        time.sleep(1)
    else:
        player_damage = int(p1.base_damage + p1.bonus_damage)

    print(f"You attack for {player_damage}.")
    time.sleep(0.5)


def evade_roll():
    global dmg_taken
    global evade
    #evade roll
    if (random.randint(1,100) <= p1.evasion_chance):
        evade = True
    else:
        evade = False

    #if evade dmg_taken = 0
    if (evade == True):
        dmg_taken = 0
        print("You evaded the attack!")
        time.sleep(1)
    else:
        dmg_taken = (m1.base_damage - p1.armor)



def burn_apply():
    global player_burnt
    global burn_turns
    #check if: - monster can apply burn - player no evade - player not burnt yet
    if (m1.burn == True and evade == False and player_burnt == False):

        #roll burn chance
        if (random.randint(1,100) <= BURN_CHANCE):
            player_burnt = True
            burn_turns = 3
            print("You got burnt!")
            time.sleep(1)

    #apply eventual burn damage
    if (player_burnt == True):
        p1.health = p1.health - BURN_DMG
        burn_turns = burn_turns - 1

        #check if burn status has ended
        if (burn_turns == 0):
            player_burnt = False
            print("You are not burnt anymore!")
            time.sleep(1)



def stun_apply():
    global player_stunned
    if (m1.stun == True and evade == False and player_stunned == False):

        #roll stun chance
        if (random.randint(1,100) <= STUN_CHANCE):
            player_stunned = True
            print("You got stunned!")
            time.sleep(1)



def combat():
    global floor
    global player_burnt
    global burn_turns
    global player_stunned
    next = False

    #generate monster
    m1_generation()

    #combat loop
    while (next == False):
        #display stats
        display_stats()

        #TOD0 Implement multiple attacks here (new func, choose you attack, mana / special)

        print("Press ENTER to attack")
        input()

        if (player_stunned == False):
            #attack dmg and critical attack chance
            crit_roll()
        
            #calculate monster health
            m1.health = m1.health - (player_damage - m1.armor)
            if (m1.armor > 0):
                print(f"The monster defended for {m1.armor}.")
                time.sleep(0.5)
            print(f"Damage inflicted: {player_damage - m1.armor}.")
            time.sleep(0.5)
        else:
            player_stunned = False

        #check if monster is dead
        if (m1.health <= 0):
            next = True
            player_burnt = False
            os.system('cls' if os.name == 'nt' else 'clear')
            print("----------\nYou defeated the monster!")
            time.sleep(1)
            continue

        #evade chance
        evade_roll()

        #burn
        burn_apply()
                
        #stun
        stun_apply()

        #apply damage taken
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
        bonus_selection()
        combat()



def regen():
    #regenerate health
    p1.health = p1.health + int((p1.health * 0.3))
    if (p1.health > p1.max_health):
        p1.health = p1.max_health
    print("----------\nHealth regenerated!")
    time.sleep(1)



def bonus_selection():
    #bonuses pool
    bonuses = ("max health", "damage", "armor")

    #extraxt 3 random bonuses from pool
    bonuses_choices = random.sample(bonuses, 3)

    #b1, b2, b3 are basically aliases
    b1 = bonuses_choices[0]
    b2 = bonuses_choices[1]
    b3 = bonuses_choices[2]

    #select bonus until valid choice
    next = False
    while(next == False):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------\nChoose a bonus:")
        print(f"1 - {b1.title()} bonus\n2 - {b2.title()} bonus\n3 - {b3.title()} bonus")
        x = input()
        if x.isdigit():
            b_selection = int(x)
            if (b_selection == 1 or b_selection == 2 or b_selection == 3):
                next = True
                continue
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------\nBonus selected")
        time.sleep(1)

    #bonus assign
    if (b_selection == 1):
        b_selection = b1
    elif (b_selection == 2):
        b_selection = b2
    elif (b_selection == 3):
        b_selection = b3

    #bonus adding
    if (b_selection == "max health"):
        p1.max_health = p1.max_health + 15
    elif (b_selection == "damage"):
        p1.bonus_damage = p1.bonus_damage + 5
    elif (b_selection == "armor"):
        p1.armor = p1.armor + 5



def lost():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("You died :(")
    time.sleep(1)
    print(f"----------\nYou defeated {floor} monsters")
    time.sleep(1)
    #save if highscore
    r = open("highscore.txt", "r")
    x = int(r.readline())
    r.close()
    if (floor > x):
        h = open("highscore.txt", "w")
        h.write(str(floor))
        h.close()
        print("----------\nNew highscore!")
        time.sleep(1)
    print("----------\nPress ENTER to restart")
    input()
    game()



def game():
    #Initialize stuff, probably bs but it works :wink:
    os.system('cls' if os.name == 'nt' else 'clear')
    global p1
    global m1
    global floor
    global burn_turns
    global player_burnt
    global player_stunned
    p1 = Player("job", 0, 0, 0, 0, 0, 0, 0)
    m1 = Monster("job", 0, 0, 0, False, False)
    floor = 1
    burn_turns = 0
    player_burnt = False
    player_stunned = False
    menu()
    set_p1_stats()
    combat()



p1 = Player("job", 0, 0, 0, 0, 0, 0, 0)
m1 = Monster("job", 0, 0, 0, False, False)
floor = 1
burn_turns = 0
player_burnt = False
player_stunned = False
game()