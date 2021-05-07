from classes.game import person, bcolors
from classes.magic import spell
from classes.inventory import item
import random

# Create black magic
fire = spell("Fire", 10, 60, "black")
thunder = spell("Thunder", 40, 80, "black")
blizzard = spell("Blizzard", 100, 120, "black")

# Create white magic
cure = spell("Cure", 15, 90, "white")
healer = spell("Healer", 10, 60, "white")

# Create Items
potion = item("Potion", "potion", "Heals 50 HP", 50)
hipotion = item("High-Potion", "potion", "Heals 90 HP", 90)
superpotion = item("Super-Potion", "potion", "Heals 150 HP", 150)
elixr = item("Elixr", "elixr", "Heals full HP/MP of 1 member", 9999)
hielixr = item("High-Elixr", "elixr", "Heals full HP/MP of all", 9999)
grenade = item("Grenade", "attack", "damages 500 HP", 500)

player_spell = [fire, thunder, blizzard, cure, healer]
enemy_spell = [fire, blizzard, cure]

player_item = [{"item": potion, "quantity": 15},
               {"item": hipotion, "quantity": 10},
               {"item": superpotion, "quantity": 5},
               {"item": elixr, "quantity": 3},
               {"item": hielixr, "quantity": 2},
               {"item": grenade, "quantity": 2}]

# Instantiate people
player1 = person("Donnie Yenn : ", 2250, 150, 400, 150, player_spell, player_item)
player2 = person("Tony Jaa :    ", 2050, 200, 250, 250, player_spell, player_item)
player3 = person("Bruce Lee :   ", 1550, 400, 450, 400, player_spell, player_item)
players = [player1, player2, player3]

enemy1 = person("Terminator :  ", 11200, 1000, 300, 20, enemy_spell, [])
enemy2 = person("Minion     :  ", 1200, 600, 400, 10, enemy_spell, [])
enemy3 = person("Goblin     :  ", 1000, 400, 500, 5, enemy_spell, [])
enemies = [enemy1, enemy2, enemy3]

defeated_enemies = 0
defeated_players = 0

running = True

while running:
    print(bcolors.FAIL + bcolors.BOLD + "\nNAME                      "
          + bcolors.OKGREEN + "HP                                     "
          + bcolors.OKBLUE + "MP" + bcolors.ENDC)
    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        if defeated_enemies == 3:
            print(bcolors.OKGREEN + bcolors.BOLD + "You win!" + bcolors.ENDC)
            running = False
            break
        if defeated_players == 3:
            print(bcolors.FAIL + bcolors.BOLD + "Your enemies have defeated you!" + bcolors.ENDC)
            running = False
            break
        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1

        if index > 2:
            print(bcolors.FAIL + "Choose option 1 to 3" + bcolors.ENDC)
            continue

        if index == 0:
            dmg = player.generate_dmg()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_dmg(dmg)
            print(bcolors.FAIL + bcolors.BOLD + player.name.replace(" ", "").replace(":", "")
                  + " attacks "
                  + enemies[enemy].name.replace(" ", "")
                  + " for ", dmg, " damage" + bcolors.ENDC)
            print(bcolors.FAIL + bcolors.BOLD + "\nNAME                      "
                  + bcolors.OKGREEN + "HP                                     "
                  + bcolors.OKBLUE + "MP" + bcolors.ENDC)
            for i in players:
                i.get_stats()
            for i in enemies:
                i.get_enemy_stats()

            if enemies[enemy].get_hp() == 0:
                print(bcolors.FAIL + bcolors.BOLD + enemies[enemy].name.replace(" ", "").replace(":", "")
                      + " has died." + bcolors.ENDC)
                del enemies[enemy]
                defeated_enemies += 1

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + bcolors.BOLD + "\nNot enough MP\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + bcolors.BOLD + spell.name + " heals "
                      + str(magic_dmg) + " HP for " + player.name.replace(" ", "").replace(":", "")
                      + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + bcolors.BOLD + player.name.replace(" ", "").replace(":", "")
                      + " 's " + spell.name + " deals "
                      + str(magic_dmg) + " damage to "
                      + enemies[enemy].name.replace(" ", "").replace(":", "") + bcolors.ENDC)
                print(bcolors.FAIL + bcolors.BOLD + "\nNAME                      "
                      + bcolors.OKGREEN + "HP                                     "
                      + bcolors.OKBLUE + "MP" + bcolors.ENDC)
                for i in players:
                    i.get_stats()
                for i in enemies:
                    i.get_enemy_stats()
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD + enemies[enemy].name.replace(" ", "")
                          + " has died." + bcolors.ENDC)
                    del enemies[enemy]
                    defeated_enemies += 1

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose Item: ")) - 1

            if item_choice == -1:
                continue

            items = player.item[item_choice]["item"]

            if player.item[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + bcolors.BOLD + "\nNot enough items\n" + bcolors.ENDC)
                continue

            player.item[item_choice]["quantity"] -= 1

            if items.type == "potion":
                player.heal(items.props)
                print(bcolors.OKGREEN + bcolors.BOLD + items.name + " heals "
                      + str(items.props) + " HP for " + player.name.replace(" ", "").replace(":", "")
                      + bcolors.ENDC)

            elif items.type == "elixr":
                if items.name == "High-Elixr":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                        print(bcolors.OKGREEN + bcolors.BOLD + items.name
                              + " heals full HP/MP of player " + i.name.replace(" ", "").replace(":", "")
                              + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + bcolors.BOLD + items.name
                      + " heals full HP/MP of player " + player.name.replace(" ", "").replace(":", "")
                      + bcolors.ENDC)

            elif items.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_dmg(items.props)
                print(bcolors.FAIL + bcolors.BOLD + player.name.replace(" ", "").replace(":", "")
                      + "'s " + items.name + " deals " + str(items.props)
                      + " damage to " + enemies[enemy].name.replace(":", "") + bcolors.ENDC)
                print(bcolors.FAIL + bcolors.BOLD + "\nNAME                      "
                      + bcolors.OKGREEN + "HP                                     "
                      + bcolors.OKBLUE + "MP" + bcolors.ENDC)
                for i in players:
                    i.get_stats()
                for i in enemies:
                    i.get_enemy_stats()
                if enemies[enemy].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD
                          + enemies[enemy].name.replace(" ", "").replace(":", "")
                          + " has died." + bcolors.ENDC)
                    del enemies[enemy]
                    defeated_enemies += 1
    # Check if Player won
    if defeated_enemies == 3:
        print(bcolors.OKGREEN + bcolors.BOLD + "You win!" + bcolors.ENDC)
        running = False
        break

    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # Choose attack
            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_dmg()

            players[target].take_dmg(enemy_dmg)
            print(bcolors.FAIL + bcolors.BOLD +
                  enemy.name.replace(" ", "").replace(":", "") + " attacks " +
                  players[target].name.replace(" ", "").replace(":", "") + " for", enemy_dmg, bcolors.ENDC)

            if players[target].get_hp() == 0:
                print(bcolors.FAIL + bcolors.BOLD + players[target].name.replace(" ", "").replace(":", "") +
                      " has died!" + bcolors.ENDC)
                del players[target]
                defeated_players += 1
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            current_mp = enemy.get_mp()
            if spell.cost > current_mp:
                continue
            enemy.reduce_mp(spell.cost)
            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + bcolors.BOLD + spell.name + " heals "
                      + enemy.name.replace(" ", "").replace(":", "") + " for "
                      + str(magic_dmg) + " HP" + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(players))
                players[target].take_dmg(magic_dmg)
                print(bcolors.OKBLUE + bcolors.BOLD + enemy.name.replace(" ", "").replace(":", "")
                      + " attacks with " + spell.name + " & deals "
                      + str(magic_dmg) + " damage to " + players[target].name.replace(":", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + bcolors.BOLD
                          + players[target].name.replace(" ", "").replace(":", "") + " has died.")
                    del players[target]
                    defeated_players += 1

        # Check if Enemy won
        if defeated_players == 3:
            print(bcolors.FAIL + bcolors.BOLD + "Your enemies have defeated you!" + bcolors.ENDC)
            running = False
            break
