import random
from classes.magic import spell
from classes.inventory import item

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


class person:
    def __init__(self,name, hp, mp, atk, df, magic, item):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk +10
        self.df = df
        self.magic = magic
        self.item = item
        self.action = ["Attack","Magic","Items"]

    def choose_target(self, enemies):
        i = 1
        print(bcolors.FAIL + bcolors.BOLD + "TARGET : " + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp != 0:
                print("    " + str(i) + " . " + enemy.name.replace(" ", ""))
                i += 1
        choice = int(input("Choose target : ")) - 1
        return choice

    def generate_dmg(self):
        return random.randrange(self.atkl,self.atkh)

    def take_dmg(self, dmg):
        self.hp -= dmg
        if self.hp <=0:
            self.hp = 0
            return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_maxhp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_maxmp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n----------------------------------")
        print(bcolors.OKBLUE + bcolors.BOLD + "ACTION" + bcolors.ENDC)
        for item in self.action:
            print("    " + str(i) + " : ", item)
            i +=1

    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\nMAGIC" + bcolors.ENDC
              + " (Choose 0 to go back to the previous menu)")
        for spell in self.magic:
            print("    " + str(i) + " : ",spell.name, ", cost : ", spell.cost)
            i += 1

    def choose_item(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + "\nITEMS" + bcolors.ENDC
              + " (Choose 0 to go back to the previous menu)")
        for it in self.item:
            print("    " + str(i) + " : ", it["item"].name, " : ",
                  it["item"].description + bcolors.FAIL + bcolors.BOLD +
                  "  x(" + str(it["quantity"]) + ")" + bcolors.ENDC)
            i += 1

    def get_enemy_stats(self):
        hp_bar = ""
        hp_bar_ticks = ((self.hp / self.maxhp) * 100) / 2

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 11:
            hp_decrease = 11 - len(hp_string)

            while hp_decrease > 0:
                current_hp += " "
                hp_decrease -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print("                          __________________________________________________")
        print(self.name + current_hp + "|" + bcolors.FAIL + hp_bar
              + bcolors.ENDC + "|")

    def get_stats(self):
        hp_bar = ""
        mp_bar = ""
        hp_bar_ticks = ((self.hp /  self.maxhp) * 100) / 4
        mp_bar_ticks = ((self.mp /  self.maxmp) * 100) / 10

        while hp_bar_ticks > 0:
            hp_bar += "█"
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_bar_ticks > 0:
            mp_bar += "█"
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            hp_decrease = 9 - len(hp_string)

            while hp_decrease > 0:
                current_hp += " "
                hp_decrease -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            mp_decrease = 7 - len(mp_string)

            while mp_decrease > 0:
                current_mp += " "
                mp_decrease -= 1

            current_mp += mp_string

        else:
            current_mp = mp_string

        print("                          _________________________              __________")
        print(self.name + current_hp + "  |" + bcolors.OKGREEN + hp_bar
              + bcolors.ENDC + "|   " + current_mp + "  |" + bcolors.OKBLUE + mp_bar
              + bcolors.ENDC + "|")

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.maxhp * 100

        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            spell, magic_dmg = self.choose_enemy_spell()
            return spell, magic_dmg
        else:
            return spell, magic_dmg
