import random
import time
import math
import json
import os
import socket  # get back to later

# -------------------------
# Scores / state
# -------------------------

KillScore = 0
DodgeScore = 0
LifeLeftScore = 0
BossScore = 0
ItemUseScore = 0
WinBonus = 0
NPCScore = 0
TotalGold = 0

inventory = ["Room Creep", "Room Creep", "Room Creep"]
ScarfInventory = []
RingInventory = []
BottleInventory = []
Gold = 0

UnlockedCharacters = ["Brawler"]
Characters = ["Brawler", "Slime", "Summoner", "Cosmic", "Dungeonspawn", "Demigod", "Priest", "Survivalist", "Pirate", "Dualed", "Orbal", "Theif", "Gambler", "Cat", "Flame", "Iced", "Jeremy"]
Moves = [
    ["Sucker Punch", "Omni Kick", "Defend", "Concussing Strike"],
    ["Bite", "Absorb", "Color Swap", "Charm"],
    ["Green Flame", "Purple Flame", "Orange Flame", "Gaurd"],
    [""],
    [""],
    [""],
    ["Dual Beam", "Dark Item", "Devine Light", "Duality"],
    ["Booster", "Bonk", "Barrage", "Mega Orb"],
    [""],
    ["D20 Punch", "Craps", "Roulette Wheel", "Slots"],
    [""],
    [""],
    [""],
    [""],
]
CharacterDescriptions = [
    "Brawler: Use your fists to punch your way through the dungeon. A well-rounded character with no special abilities.",
    "Slime: Silly little guy who has a slime for a head. Strong against colored slimes and can utilize colored blobs.",
    "Summoner: A mysterious enchantress who can summon colored flames to fight for her.",
    "Cosmic: A deity of the cosmos who's powers depend on the alignment of the stars. Each round has different effects.",
    "Dungeonspawn: One of the dungeon's monsters, who can shift into anything else.",
    "Demigod: Halfborn of the Worm-Cat, they hold immense power and can use it to their advantage.",
    "Priest: A holy worshipper cappible of bending the dungeon itself to their will. Can use divine light to heal and smite.",
    "Survivalist: A rugged adventurer who has survived many dungeons. Can use items more effectively than others.",
    "Pirate: A strange man cappible of randomly summoning water and boats, for some reason.",
    "Dualed: A mysterious being that is two people in one body. Even waves give them power and odd waves debuff them.",
    "Orbal: An odd being that can summon orbs. Attacks revolve arround orb points to execute them.",
    "Theif: Wandered into the dungeon looking for loot, now just stuck down here. Can steal from enemies and has a higher dodge chance.",
    "Gambler: A washed-up gambler who has been trapped in the dungeon for years. Has higher luck, but attacks cost gold.",
    "Cat: Literally just a cat.",
    "Flame: Flame dietety that can use fire to attack, dealing damage over time.",
    "Iced: Ice dietety that can use ice to attack, brittling enemies and adding a damage multiplier.",
    "Jeremy: Who is this. Who invited him. Why is he here."

]

Character = ""

Sword = "Pathetic Sword"

room = 49
running = True
death = False

YourLife = 5.0
MaxLife = 5.0
Saves = 2

SpectatorHits = 0

Name = ""

BossLevel = False
Hardmode = False
LevelBeat = False
HealUsed = False

# Colors
# Rarities: White -> Green -> Blue -> Purple -> Yellow -> Red (Grey for dark stuff)
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
PURPLE = "\033[35m"
GREY = "\033[30m"
RESET = "\033[0m"
BOLDRED = "\033[1;31m"
BOLDGREEN = "\033[1;32m"
BOLDYELLOW = "\033[1;33m"
BOLDBLUE = "\033[1;34m"
BOLDPURPLE = "\033[1;35m"
BOLDWHITE = "\033[1;37m"

rainbow = [
    "\033[31m",  # Red
    "\033[33m",  # Yellow
    "\033[32m",  # Green
    "\033[36m",  # Cyan
    "\033[34m",  # Blue
    "\033[35m",  # Magenta
]

def rainbow_text(text):
    result = ""
    for i, char in enumerate(text):
        result += rainbow[(i) % len(rainbow)] + char
    return result + RESET

# Room-wide multipliers
RoomDodge = 1.0
RoomDamage = 1.0
RoomDefence = 1.0

HalfDamage = 0

# Permanent upgrades
MetaDodge = 1.0
MetaDamage = 1.0
MetaDefence = 1.0
MaxInventory = 30
MaxScarfInventory = 5
MaxRingInventory = 5
MaxBottleInventory = 5

# Room chances
ChestMercy = 5
ChestRoomChance = 0.20
ThroneRoomChance = 0.00
HordeRoomChance = 0.00
DarkRoomChance = 0.00
MallRoomChance = 0.01
CalmingRoomChance = 0.02

RoomType = 0

RoomDisplays = [
    "Normal",
    GREEN+"Chest"+RESET,
    BLUE+"Mall"+RESET,
    PURPLE+"Calming"+RESET,
    YELLOW+"Throne"+RESET,
    YELLOW+"Horde"+RESET,
    GREY+"Dark"+RESET,
    rainbow_text("Slime"),
    rainbow_text("Worm"),
    rainbow_text("Astral"),
    rainbow_text("Final"),
    rainbow_text("Final(?)"),
    rainbow_text("True Final"),
    RED+"Hall"+RESET,
    "Cat",
    "Laudromat",
]

disarm_all = 0

TurnsTaken = 0

SkipRoomNow = False

CauseOfDeath = ""
MessageList = []

# -------------------------
# Enemy / reward data
# -------------------------
enemy_types1 = ["Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Pink Slime",
                "Dyna-Dot", "Just A Goob", "Cheese Bro", "Math.png", "Holy Microwave"]
enemy_types2 = ["Dyna-Mott", "Generic Goob", "D-Pad Guy", "ORB OF SILLY", "Rainbow Slime", "Math.wav", "Holy Grill"]
enemy_types3 = ["Dyna-Mite", "General Goob", "Concok", "Mountain Slime", "Big Cheese", "Math.mp4", "Holy Oven"]
enemy_types4 = ["Conqua", "Dyna-Mighty", "Tonadoe", "D-Pad Man", "Void Slime", "ORB OF GOOFY", "Shiny Gloom"]
enemy_types5 = ["Conquaction", "Dyna-Rex", "Typhoonoe", "Volcano Slime", "Timecreeper", "Spacecreeper",
                "D-Pad Sir", "Golden Big Cheese Bro", "Shiny Doom"]
elite_enemies = ["Conqueckter", "Dyna-Max", "Hurricaneadoe", "Moon Slime", "Deathcreeper", "D-Pad Person", "Shiny Terror of the Dungeon"]
pressure_enemies = ["Flameboi", "Exploding Mush", "Gloompy", "Voice From Above", "Googly Eye Storm"]

bosses = ["Slime God", "Dungeon Worm", "Astral Reflection", "Dungeonemus Maximus"]
# Lessons taught: item usage, priorities, skill or smth, and probs some combo of those ig idk
# Blessings/curses: swords, mutations, idk, and none

# IMPORTANT: enemy_bank, reward_bank, money_values must be aligned by index
enemy_bank = [
    "Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Pink Slime",
    "Dyna-Dot", "Just A Goob", "Cheese Bro", "Math.png", "Holy Microwave",
    "Dyna-Mott", "Generic Goob", "D-Pad Guy", "ORB OF SILLY", "Rainbow Slime", "Math.wav", "Holy Grill",
    "Dyna-Mite", "General Goob", "Concok", "Mountain Slime", "Big Cheese", "Math.mp4", "Holy Oven",
    "Conqua", "Dyna-Mighty", "Tonadoe", "D-Pad Man", "Void Slime", "ORB OF GOOFY", "Shiny Gloom", "Dungeon Gaurd",
    "Conquaction", "Dyna-Rex", "Typhoonoe", "Volcano Slime", "Timecreeper", "Spacecreeper",
    "D-Pad Sir", "Golden Big Cheese Bro", "Shiny Doom",
    "Conqueckter", "Dyna-Max", "Hurricaneadoe", "Moon Slime", "Deathcreeper", "D-Pad Person", "Shiny Terror of the Dungeon",
    "Flameboi", "Exploding Mush", "Gloompy", "Voice From Above", "Googly Eye Storm",
    "", "Cat",
    "Red Flame I", "Green Flame I", "Red Flame II", "Green Flame II", "Purple Flame II", "Yellow Flame II", "Red Flame III", "Green Flame III", "Purple Flame III", "Yellow Flame III", "Blue Flame III", "Orange Flame III", "Rainbow Flame", "Worm Gaurd",
    "Presuiter", "Screamer", "Gazer", "Spectator",
    "Slime God", "Dungeon Worm", "Astral Reflection", "Dungeonemus Maximus"
]

worm_summons = ["Red Flame I", "Green Flame I", "Red Flame II", "Green Flame II", "Purple Flame II", "Yellow Flame II", "Red Flame III", "Green Flame III", "Purple Flame III", "Yellow Flame III", "Blue Flame III", "Orange Flame III", "Rainbow Flame"]

# Rarities: White -> Green -> Blue -> Purple -> Yellow -> Red
enemy_displays = [
    "Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Pink Slime",
    "Dyna-Dot", "Just A Goob", "Cheese Bro", "Math.png", "Holy Microwave",
    GREEN+"Dyna-Mott"+RESET, GREEN+"Generic Goob"+RESET, GREEN+"D-Pad Guy"+RESET, GREEN+"ORB OF SILLY"+RESET, GREEN+"Rainbow Slime"+RESET, GREEN+"Math.wav"+RESET, GREEN+"Holy Grill"+RESET,
    BLUE+"Dyna-Mite"+RESET, BLUE+"General Goob"+RESET, BLUE+"Concok"+RESET, BLUE+"Mountain Slime"+RESET, BLUE+"Big Cheese"+RESET, BLUE+"Math.mp4"+RESET, BLUE+"Holy Oven"+RESET,
    PURPLE+"Conqua"+RESET, PURPLE+"Dyna-Mighty"+RESET, PURPLE+"Tonadoe"+RESET, PURPLE+"D-Pad Man"+RESET, PURPLE+"Void Slime"+RESET, PURPLE+"ORB OF GOOFY"+RESET, PURPLE+"Shiny Gloom"+RESET, PURPLE+"Dungeon Gaurd"+RESET,
    YELLOW+"Conquaction"+RESET, YELLOW+"Dyna-Rex"+RESET, YELLOW+"Typhoonoe"+RESET, YELLOW+"Volcano Slime"+RESET, YELLOW+"Timecreeper"+RESET, YELLOW+"Spacecreeper"+RESET,
    YELLOW+"D-Pad Sir"+RESET, YELLOW+"Golden Big Cheese Bro"+RESET, YELLOW+"Shiny Doom"+RESET,
    RED+"Conqueckter"+RESET, RED+"Dyna-Max"+RESET, RED+"Hurricaneadoe"+RESET, RED+"Moon Slime"+RESET, RED+"Deathcreeper"+RESET, RED+"D-Pad Person"+RESET, RED+"Shiny Terror of the Dungeon"+RESET,
    "Flameboi", "Exploding Mush", GREEN+"Gloompy"+RESET, GREEN+"Voice From Above"+RESET, BLUE+"Googly Eye Storm"+RESET,
    "", "Cat",
    "Red Flame I", "Green Flame I", BLUE+"Red Flame II"+RESET, BLUE+"Green Flame II"+RESET, BLUE+"Purple Flame II"+RESET, BLUE+"Yellow Flame II"+RESET, YELLOW+"Red Flame III"+RESET, YELLOW+"Green Flame III"+RESET, YELLOW+"Purple Flame III"+RESET, YELLOW+"Yellow Flame III"+RESET, YELLOW+"Blue Flame III"+RESET, YELLOW+"Orange Flame III"+RESET, rainbow_text("Rainbow Flame"), "Worm Gaurd",
    GREY+"Presuiter"+RESET, GREY+"Screamer"+RESET, GREY+"Gazer"+RESET, GREY+"Spectator"+RESET,
    rainbow_text("Slime God"), rainbow_text("Dungeon Worm"), rainbow_text("Astral Reflection"), rainbow_text("Dungeonemus Maximus")
]

# Rarities: White -> Green -> Blue -> Purple -> Yellow -> Red
item_displays = [
    "Red Blob", "Orange Blob", "Yellow Blob", "Green Blob", "Blue Blob", "Purple Blob", "Pink Blob",
    "Dyna-Stick", "Nothing", "Cheddar", "x=2a-b±b2-4ac", "Food 1",
    GREEN+"Dyna-Grenade"+RESET, "Nothing", GREEN+".zip bomb"+RESET, GREEN+"Potion of Orb"+RESET, GREEN+"Rainbow Blob"+RESET, GREEN+"d=(x2x2)2+(y2-y1)2"+RESET, GREEN+"Food 2"+RESET,
    BLUE+"Dyna-Bomb"+RESET, "Nothing", BLUE+"Healing Potion"+RESET, BLUE+"Mountain Blob"+RESET, BLUE+"Big Cheddar"+RESET, BLUE+"x=(-b±√(b^2-4ac))/(2a)"+RESET, BLUE+"Food 3"+RESET,
    PURPLE+"Greater Healing Potion"+RESET, PURPLE+"Dyna-Missile"+RESET, PURPLE+"Rage Juice"+RESET, PURPLE+".zip nuke"+RESET, PURPLE+"Void Blob"+RESET, PURPLE+"Super Potion of Orb"+RESET, PURPLE+"Glowy Malice"+RESET, "Nothing",
    YELLOW+"Heal Concoction"+RESET, YELLOW+"Dyna-Nuke"+RESET, YELLOW+"Determination Juice"+RESET, YELLOW+"Lava Blob"+RESET, YELLOW+"Room Creep"+RESET, YELLOW+"Item Creep"+RESET,
    YELLOW+"9 ronnabite .zip bomb"+RESET, YELLOW+"Golden Cheddar"+RESET, YELLOW+"Glowy Feeling of Unease"+RESET,
    RED+"Heal Totem"+RESET, RED+"Dyna-Antimater Bomb"+RESET, RED+"Pacifist Juice"+RESET, RED+"Moon Blob"+RESET, RED+"Demolisher Creep"+RESET, RED+"two billion ronnabite .zip bomb"+RESET, RED+"Glowy Ultimate Dungeon Prize"+RESET,
    "Fire Charge", "Exploding Spores", GREEN+"Gloomper"+RESET, GREEN+"Call to Arms"+RESET, BLUE+"Arts and Crafts"+RESET,
    RED+"Rainbow Run"+RESET, GREEN+"Cat Food"+RESET,
    "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing",
    GREY+"Dark Stone"+RESET, GREY+"Dark Stone"+RESET, GREY+"Dark Stone"+RESET, GREY+"Dark Stone"+RESET,
    "", "", "", ""
]

reward_bank = [
    "Red Blob", "Orange Blob", "Yellow Blob", "Green Blob", "Blue Blob", "Purple Blob", "Pink Blob",
    "Dyna-Stick", "Nothing", "Cheddar", "x=2a-b±b2-4ac", "Food 1",
    "Dyna-Grenade", "Nothing", ".zip bomb", "Potion of Orb", "Rainbow Blob", "d=(x2x2)2+(y2-y1)2", "Food 2",
    "Dyna-Bomb", "Nothing", "Healing Potion", "Mountain Blob", "Big Cheddar", "x=(-b±√(b^2-4ac))/(2a)", "Food 3",
    "Greater Healing Potion", "Dyna-Missile", "Rage Juice", ".zip nuke", "Void Blob", "Super Potion of Orb", "Glowy Malice", "Nothing",
    "Heal Concoction", "Dyna-Nuke", "Determination Juice", "Lava Blob", "Room Creep", "Item Creep",
    "9 ronnabite .zip bomb", "Golden Cheddar", "Glowy Feeling of Unease",
    "Heal Totem", "Dyna-Antimater Bomb", "Pacifist Juice", "Moon Blob", "Demolisher Creep", "two billion ronnabite .zip bomb", "Glowy Ultimate Dungeon Prize",
    "Fire Charge", "Exploding Spores", "Gloomper", "Call to Arms", "Arts and Crafts",
    "Rainbow Run", "Cat Food",
    "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing", "Nothing",
    "Dark Stone", "Dark Stone", "Dark Stone", "Dark Stone",
    "", "", "", ""
]

descriptions = [
    "Red Blob: Super effective against Green Slimes.",
    "Orange Blob: Super effective against Blue Slimes.",
    "Yellow Blob: Super effective against Purple Slimes.",
    "Green Blob: Super effective against Red Slimes.",
    "Blue Blob: Super effective against Orange Slimes.",
    "Purple Blob: Super effective against Yellow Slimes.",
    "Pink Blob: Super effective against Dyna-Dot and Goob species.",
    "Dyna-Stick: Explosive stick that does 10 damage to one enemy.",
    "",
    "Cheddar: A delicious piece of cheese. It doesn't do anyive stick that does 25 damage to one enemy.",
    "x=2a-b±b2-4ac: Takes out 5% of an enemy's current health.",
    "Food: Delicious dish. Eat it and see what happens!",
    "Dyna-Grenade: Explosive stick that does 25 damage to one enemy.",
    "",
    ".zip bomb: A small bomb that does 10 damage to all enemies, and 5 bonus damage to one enemy.",
    "Potion of Orb: A mysterious concoction with random effects. It can heal you, boost your damage, or even make you take more damage!",
    "Rainbow Blob: Super effective against all colored slimes or void slimes, but not as effective as colored blobs against their specific color.",
    "d=(x2x2)2+(y2-y1)2: Takes out 10% of an enemy's current health.",
    "Food: Delicious dish. Eat it and see what happens!",
    "Dyna-Bomb: Explosive stick that does 50 damage to one enemy.",
    "",
    "Healing Potion: A potion that heals you for 1 health.",
    "Mountain Blob: Super effective against volcano slimes.",
    "Big Cheddar: A big piece of cheddar. It doesn't do anything, but NPCs really love it!",
    "x=(-b±√(b^2-4ac))/(2a): Takes out 15% of an enemy's current health.",
    "Food: Delicious dish. Eat it and see what happens!",
    "Greater Healing Potion: A stronger potion that heals you for 3 health.",
    "Dyna-Missile: Explosive stick that does 100 damage to one enemy.",
    "Rage Juice: A juice that stuns an enemy. It stuns bosses for 1 turn, and regular enemies for 3 turns.",
    ".zip nuke: A powerful bomb that does 75 damage to all enemies, and 25 bonus damage to one enemy.",
    "Void Blob: Super effective against rainbow slimes, but not as effective as colored blobs against their specific color.",
    "Super Potion of Orb: A stronger version of the Potion of Orb, with more extreme random effects that are always positive.",
    "Glowy Malice: A super shiny glob! If you throw it, all enemies will be distracted for a turn!",
    "",
    "Heal Concoction: A concoction that heals you for 5 health.",
    "Dyna-Nuke: Explosive stick that does 200 damage to one enemy.",
    "Determination Juice: A juice that stuns an enemy. It stuns regular enemies for the rest of the room, and bosses for 3 turns.",
    "Lava Blob: Super effective against mountain slimes.",
    "Room Creep: A mysterious object that allows you to skip the rest of the room after dodging an attack. It doesn't work on boss rooms.",
    "Item Creep: A mysterious object that allows you to steal an item from an enemy after dodging an attack. It doesn't work on boss rooms.",
    "9 ronnabite .zip bomb: An extremely powerful bomb that does 150 damage to all enemies, and 75 bonus damage to one enemy.",
    "Golden Cheddar: A golden piece of cheddar. It doesn't do anything, but NPCs really, really love it!",
    "Glowy Feeling of Unease: A super shiny scary thing! If you throw it, all enemies will be distracted for 3 turns!",
    "Heal Totem: A powerful totem that heals you for 10 health.",
    "Dyna-Antimater Bomb: An extremely powerful explosive stick that does 300 damage to one enemy.",
    "Pacifist Juice: A powerful juice that stuns an enemy. It stuns regular enemies for the rest of the room, and bosses for 5 turns.",
    "Moon Blob: Super effective against all slimes, tough enemies and bosses, but not as effective as colored blobs against their specific color.",
    "Demolisher Creep: A mysterious object that allows you to deal 500 damage to all enemies after dodging an attack. It doesn't work on boss rooms.",
    "two billion ronnabite .zip bomb: A super powerful bomb that does 250 damage to all enemies, and 100 bonus damage to one enemy.",
    "Glowy Ultimate Dungeon Prise: The ultimate prise of the dungeon! If you throw it, all enemies will be distracted for 5 turns!",
    "Fire Charge: Deals 5 damage at the start of the game, but scales with the rooms.",
    "Exploding Spores: Gives you extra attack damage for the room!",
    "Gloomper: Makes dodges far easier for the rest of the room.",
    "Call to Arms: Gives you a chance to do 10 extra damage. Scales with the rooms.",
    "Arts and Crafts: Deals 25 damage, scales with the rooms.",
    "Rainbow Run: Hey! How did you get this?! Get out of here, cheater! You should be ashamed of yourself!",
    "Cat Food: Hey! How did you get this?! Get out of here, cheater! You should be ashamed of yourself!",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Dark Stone",
    "Dark Stone",
    "Dark Stone",
    "Dark Stone",
    "",
    "",
    "",
    ""
]

checks = [
    "Red Slime: Basic enemy. Weak to Green Blobs.",
    "Orange Slime: Basic enemy. Weak to Green Blobs.",
    "Yellow Slime: Basic enemy. Weak to Green Blobs.",
    "Green Slime: Basic enemy. Weak to Green Blobs.",
    "Blue Slime: Basic enemy. Weak to Green Blobs.",
    "Purple Slime: Basic enemy. Weak to Green Blobs.",
    "Pink Slime: Tiny, hardy slime. No known opposite.",
    "Dyna-Dot: Silly explosive guy. Uses harder dodges than slimes.",
    "Just A Goob: Glob of ???? who can't attack, but is tanky.",
    "Cheese Bro: The copycat of the dungeon, has no unique atacks (and also uses lots of slang).",
    "Math.png: Loud enemy who wants you to do your math homework.",
    "Holy Microwave: Devine creature that serves the dungeon. Don't ask where it gets its ingredients."
    "Dyna-Mott: Funny little fella who uses harder dodges.",
    "Generic Goob: Formless, brainless creature who doesn't attack, but can tank a lot of damage.",
    "D-Pad Guy: Angry little fella who makes you repeat up, down, left, and right patterns.",
    "ORB OF SILLY: A mysterious concoction with random effects. It can heal you, boost your damage, or even make you take more damage!",
    "Rainbow Blob: Super effective against all colored slimes or void slimes, but not as effective as colored blobs against their specific color.",
    "d=(x2x2)2+(y2-y1)2: Takes out 10% of an enemy's current health.",
    "Holy Grill: Devine creature that serves the dungeon. Don't ask where it gets its ingredients."
    "Dyna-Bomb: Explosive stick that does 50 damage to one enemy.",
    "",
    "Healing Potion: A potion that heals you for 1 health.",
    "Mountain Blob: Super effective against volcano slimes.",
    "Big Cheddar: A big piece of cheddar. It doesn't do anything, but NPCs really love it!",
    "x=(-b±√(b^2-4ac))/(2a): Takes out 15% of an enemy's current health.",
    "Holy Oven: Devine creature that serves the dungeon. Don't ask where it gets its ingredients."
    "Greater Healing Potion: A stronger potion that heals you for 3 health.",
    "Dyna-Missile: Explosive stick that does 100 damage to one enemy.",
    "Rage Juice: A juice that stuns an enemy. It stuns bosses for 1 turn, and regular enemies for 3 turns.",
    ".zip nuke: A powerful bomb that does 75 damage to all enemies, and 25 bonus damage to one enemy.",
    "Void Blob: Super effective against rainbow slimes, but not as effective as colored blobs against their specific color.",
    "Super Potion of Orb: A stronger version of the Potion of Orb, with more extreme random effects that are always positive.",
    "Glowy Malice: A super shiny glob! If you throw it, all enemies will be distracted for a turn!",
    "Dungeon Gaurd: Royal protector of the dungeon, makes enemies take half damage while present. May or may not be a Goob.",
    "Heal Concoction: A concoction that heals you for 5 health.",
    "Dyna-Nuke: Explosive stick that does 300 damage to one enemy.",
    "Determination Juice: A juice that stuns an enemy. It stuns regular enemies for the rest of the room, and bosses for 3 turns.",
    "Lava Blob: Super effective against mountain slimes.",
    "Room Creep: A mysterious object that allows you to skip the rest of the room after dodging an attack. It doesn't work on boss rooms.",
    "Item Creep: A mysterious object that allows you to steal an item from an enemy after dodging an attack. It doesn't work on boss rooms.",
    "9 ronnabite .zip bomb: An extremely powerful bomb that does 200 damage to all enemies, and 50 bonus damage to one enemy.",
    "Golden Cheddar: A golden piece of cheddar. It doesn't do anything, but NPCs really, really love it!",
    "Glowy Feeling of Unease: A super shiny scary thing! If you throw it, all enemies will be distracted for 3 turns!",
    "Heal Totem: A powerful totem that heals you for 10 health.",
    "Dyna-Antimater Bomb: An extremely powerful explosive stick that does 750 damage to one enemy.",
    "Pacifist Juice: A powerful juice that stuns an enemy. It stuns regular enemies for the rest of the room, and bosses for 5 turns.",
    "Moon Blob: Super effective against all slimes, tough enemies and bosses, but not as effective as colored blobs against their specific color.",
    "Demolisher Creep: A mysterious object that allows you to deal 500 damage to all enemies after dodging an attack. It doesn't work on boss rooms.",
    "two billion ronnabite .zip bomb: A super powerful bomb that does 300 damage to all enemies, and 100 bonus damage to one enemy.",
    "Glowy Ultimate Dungeon Prise: The ultimate prise of the dungeon! If you throw it, all enemies will be distracted for 5 turns!",
    "Fire Charge: Deals 5 damage at the start of the game, but scales with the rooms.",
    "Exploding Spores: Gives you extra attack damage for the room!",
    "Gloomper: Makes dodges far easier for the rest of the room.",
    "Call to Arms: Gives you a chance to do 10 extra damage. Scales with the rooms.",
    "Arts and Crafts: Deals 25 damage, scales with the rooms.",
    "Rainbow Run: It may or may not do some cool stuff.",
    "Cat Food: Yippie food for enemies :3",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Presuiter: Terrifying mass of eyeballs and blades. Quite cute when brought out of the light. Will chase down targets and deal large ammounts of damage.",
    "Screamer: Horrifiying being with it's dark flesh opening to expose it's heart. Produces ear-splitting screams to attack.",
    "Gazer: Not to be confused with a slime, a horrific dark body with one eye and teeth. Bites down with incredible force to attack."
    "Spectator: Humanoid shadow being. Commonly thought to be the ghost of fallen dungeoneers. Deals no damage, but instantly kills you if you miss 5 dodges."
    "Slime God: Terrifying mound of slime. Mindless, and it's only intention is to consume all.",
    "Dungeon Worm: ",
    "Astral Reflection: ",
    "Dungeonemus Maximus: "
]

money_values = [
    1, 1, 1, 1, 1, 1, 3,
    5, 0, 10, 5, 5,
    10, 0, 10, 0, 5, 10, 0, 10,
    15, 0, 20, 7, 30, 1, 15,
    30, 25, 25, 25, 10, 0, 25,
    50, 45, 45, 15, 55, 55,
    45, 100, 45,
    80, 75, 75, 20, 120, 75, 75,
    5, 10, 20, 40, 80,
    0, 5,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    100, 100, 100, 100,
    150, 300, 500, 1000
]

assert len(enemy_bank) == len(reward_bank) == len(money_values) == len(descriptions) == len(enemy_displays) == len(item_displays), (
    f"enemy/item bank mismatch: enemies={len(enemy_bank)} rewards={len(reward_bank)} money={len(money_values)} descriptions={len(descriptions)} enemy displays={len(enemy_displays)} item displays={len(item_displays)}"
)

# NPC item pools (tiers)
NPCItems1 = ["Red Blob", "Orange Blob", "Yellow Blob", "Green Blob", "Blue Blob", "Purple Blob", "Pink Blob", "Dyna-Stick", "Cheddar", "x=2a-b±b2-4ac"]
NPCItems2 = ["Dyna-Grenade", ".zip bomb", "Potion of Orb", "Rainbow Blob", "d=(x2x2)2+(y2-y1)2"]
NPCItems3 = ["Dyna-Bomb", "Healing Potion", "Mountain Blob", "Big Cheddar", "x=(-b±√(b^2-4ac))/(2a)"]
NPCItems4 = ["Greater Healing Potion", "Dyna-Missile", "Rage Juice", ".zip nuke"]
NPCItems5 = ["Heal Concoction", "Dyna-Nuke", "Determination Juice", "Lava Blob", "Room Creep", "Item Creep",
             "9 ronnabite .zip bomb", "Super Potion of Orb"]
NPCItems6 = ["Heal Totem", "Dyna-Antimater Bomb", "Pacifist Juice", "Moon Blob", "Demolisher Creep", "two billion ronnabite .zip bomb"]

NPCBlacklist = ["Fire Charge", "Exploding Spores", "Gloomper", "Call to Arms", "Arts and Crafts", "Dark Stone"]

# Item options / dodges
chaos_bank = ["Heal", "Dodge", "Damage", "Defence"]
food_1 = ["Moss", "Steak.PNG", "Cheddar", "Dyna-Sausage"]
food_2 = ["Concoc Chai Tea", "Rainbow Slime Dumplings", "SILLYCONE", "D-Pad Sandwiches"]
food_3 = ["General Food Slop", "Scrumptious Giant Cheddar", "Mountainous Slime Cake", "Burger_Recording_Final_Final_293471.mp4"]
food_1_options = [""]
food_2_options = [""]
food_3_options = [""]
combo_dodges = ["dodge dodge dodge", "dodge dodge", "dodge dodge dodge dodge", "dodge"]
easy_dodges = ["d", "dodge", ":)", "ge" "dod", "do", "dge"]
hard_dodges = ["dodgedodge", "DODGE", "egdod", "_dodge_", "Dodge", "#Dodge", "egd", "dodge!"]
harder_dodges = ["dodgedodgedodge", "DODGE DODGE", "dodgeegdod", '<"dodge">', "DodgE", "#Dodge", "Egdod", "DodgE!", "dodge??", "DODGE!!!"]
hardest_dodges = ["dodgedodgedodgedodge", "DODGE??? DODGE!!!", "dodgegdodgegdod", "func(dodge): dodge dodge dodge", "DoDGe?", "EgDoDdOdGe", "EgD eGd EgD eGd"]
harderest_dodges = ["dodgedodgedodgedodgedodge", "DODGE!!1!", "dogdodgegdodgegdoddog", "for dodge in range(random.range(do,dge))", "oH HI My NaMe iS dODgE!"]
hardererest_dodges = ["dodgedodgedodgedodgedodgedodge", "DODGE!!1!1!!11!!!one!", "dodgedogdodgegdodgegdoddogegdod",
                      "def dodge(Dodge, Dodge, Dodge, Dodge): print('YOU NEED TO DODGE')", "DddDoOOddGgGGggGeEeeEE!"]
alphebet = "abcdefghijkmnlopqrstuvwxyz"

scream_dodges = ["AAAAaAaaaAuUUuuuUggGGGggGGhHHHH!!", "EEEeeeEEEEaaaaeEEeeeaaEEEEEE!!", "RRRrrAaaaaaAAhhhHHHHHHhhhhHHHHH!!"]

concok_dodge = [
    "Step one of making a potion: Dodge. This is the most important step.",
    "Step seven of making a potion: Stir. What else would you do?",
    "Some common ingredients are: Mushroom, Moss, Bricks. That's all we get arround here.",
    "I contain the finest of ingredients. It tastes spicy on it's own, though.",
    "I don't like Math PNGs. They're so loud and obnoxious. I wish they would just leave.",
    "Step 12 of making a potion: Dodge again. Why, you probably ask? Because.",
    "D-Pad guys are a wierd lot. They just walk in squares all day! Strange.",
    "Can we all just admit that I'm the smartest enemy in the game yet?",
    "I truly do hate it when people just control-v my attacks. So rude!",
    "I hope I get some free cheese after this... you humans aren't the only ones!",
    "I did some research, and we can summon more of me by hummans saying 'MOREOFTHEM??' so that's cool",
    "People say I'm too annoying... BUT I THINK THEY'RE TOO EASILY ANNOYED! *sad noises*",
    "Step 29 of making a potion: blow up. This is the final step, and for a good reason.",
    "Humans are wierd. Why do they even come to this place? Who would want to kill me?",
    "Slimes are goofy. They don't even have bones! All they do is flop like a fish.",
    "I forgot my notes...",
    "Darn! No notes.",
    "HA! I remembered my notes! Oh... all that's on them is... nothing.",
]

# Item category sets (fixes incorrect slicing assumptions)
BLOB_ITEMS = {"Red Blob", "Orange Blob", "Yellow Blob", "Green Blob", "Blue Blob", "Purple Blob", "Pink Blob",
              "Rainbow Blob", "Mountain Blob", "Void Blob", "Lava Blob", "Moon Blob"}
STICK_ITEMS = {"Dyna-Stick", "Dyna-Grenade", "Dyna-Bomb", "Dyna-Missile", "Dyna-Nuke", "Dyna-Antimater Bomb", "Exploding Spores"}
DRINK_ITEMS = {"Healing Potion", "Greater Healing Potion", "Heal Concoction", "Potion of Orb", "Super Potion of Orb"}
BOMB_ITEMS = {".zip bomb", ".zip nuke", "9 ronnabite .zip bomb", "two billion ronnabite .zip bomb"}
JUICE_ITEMS = {"Rage Juice", "Determination Juice", "Pacifist Juice"}
CREEP_ITEMS = {"Room Creep", "Item Creep", "Demolisher Creep", "Heal Totem", "Glowy Ultimate Dungeon Prize", "Glowy Feeling of Unease", "Glowy Malice",
                "Call to Arms"}
MATH_ITEMS = {"x=(-b±√(b^2-4ac))/(2a)", "x=2a-b±b2-4ac", "d=(x2x2)2+(y2-y1)2", "Fire Charge"}
CHEESE_ITEMS = {"Cheddar", "Big Cheddar", "Golden Cheddar"}
WEIRD_ITEMS = {"Gloomper", "Arts and Crafts"}
CHEAT_ITEMS = {"Rainbow Run", "Cat Food"}
DARK_ITEMS = {"Dark Stone"}

SLIME_ENEMIES = ["Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Pink Slime", "Rainbow Slime", "Mountain Slime",
                "Void Slime", "Volcano Slime", "Moon Slime"]
SMOKE_ENEMIES = ["Dyna-Dot", "Dyna-Mott", "Dyna-Mite", "Dyna-Mighty", "Dyna-Rex", "Dyna-Max"]
PHASE_ENEMIES = ["Cheese Bro", "D-Pad Guy", "Big Cheese", "D-Pad Man", "Shiny Gloom", "D-Pad Sir", "Golden Big Cheese Bro", "Shiny Doom", "D-Pad Person",
                "Shiny Terror of the Dungeon"]
AWKWARD_ENEMIES = ["Just A Goob", "Generic Goob", "General Goob", "Cat"]
REVIVAL_ENEMIES = ["Concok", "Conqua", "Conquaction", "Conqueckter"]
MUSICAL_ENEMIES = ["Math.png", "Math.wav", "Math.mp4"]
EXPLOSIVE_ENEMIES = ["ORB OF SILLY", "ORB OF GOOFY", "Timecreeper", "Spacecreeper", "Deathcreeper"]
WIND_ENEMIES = ["Tonadoe", "Typhoonoe", "Hurricanadoe"]
DARK_ENEMIES = ["Presuiter", "Screamer", "Gazer", "Spectator"]

# Effectiveness tables
super_effective = {
    "Red Blob": "Green Slime",
    "Orange Blob": "Blue Slime",
    "Yellow Blob": "Purple Slime",
    "Green Blob": "Red Slime",
    "Blue Blob": "Orange Slime",
    "Purple Blob": "Yellow Slime",
    "Rainbow Blob": "Slime God",
    "Void Blob": "Rainbow Slime",
}

somewhat_effective = {
    "Pink Blob": ["Dyna-Dot", "Dyna-Mott", "Dyna-Mite", "Dyna-Mighty", "Dyna-Rex", "Dyna-Max", "Slime God"],
    "Rainbow Blob": ["Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Pink Slime", "Rainbow Slime"],
    "Void Blob": "Slime God",
    "Mountain Blob": "Slime God",
    "Lava Blob": "Slime God",
    "Moon Blob": ["Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime",
                 "Pink Slime", "Rainbow Slime", "Mountain Slime", "Void Slime"],
}

mid_effective = {
    "Pink Blob": "Slime God",
    "Rainbow Blob": "Slime God",
}

small_effective = {
    "Red Blob": "Slime God",
    "Orange Blob": "Slime God",
    "Yellow Blob": "Slime God",
    "Green Blob": "Slime God",
    "Blue Blob": "Slime God",
    "Purple Blob": "Slime God",
}

tiny_effective = {
    "Red Blob": "Void Slime",
    "Orange Blob": "Void Slime",
    "Yellow Blob": "Void Slime",
    "Green Blob": "Void Slime",
    "Blue Blob": "Void Slime",
    "Purple Blob": "Void Slime",
}

super_duper_effective = {
    "Mountain Blob": "Volcano Slime",
    "Lava Blob": "Mountain Slime",
    "Pink Blob": ["Just A Goob", "Generic Goob", "General Goob"],
    "Moon Blob": elite_enemies + bosses + enemy_types5,
}

Merchants = ["Truffle"]  # Maybe Seedless Strawberry as ITFT colab
DeepMerchants = []
Traders = ["Jerry"]
DeepTraders = []
Wizards = ["Steph"]
DeepWizards = []
Medics = []  # Maybe DrRETRO? Colab, perhaps?
DeepMedics = []
Gamblers = ["Benji"]  # Benji has higher spawn chance
DeepGamblers = []

Dialouge = [
    [  # Jerry

    ],
    [  # Truffle
        [  # welcome
            "hewwo, welcome :3",
            "welcome to my shop of awsumeness :3",
            "hi fweinds :3",
            "hewwo :3",
            "buy sumthin? :3",
        ],
        [  # small buy
            "aww tysm :3",
            "thank yous :3",
            "so sweet :3",
            "thanks for buy :3",
            "on a budget? :3",
            "get a bunch :3",
        ],
        [  # mid buy
            "aww tysm :3",
            "thank yous :3",
            "so sweet :3",
            "thanks for buy :3",
            "yea :3",
            "cool :3",
            "thx :3",
            "yay :3",
            "awsum :3",
            "nice :3",
        ],
        [  # big buy
            "aww tysm :3",
            "thank yous :3",
            "so sweet :3",
            "thanks for buy :3",
            "wowsers o_o",
            "somewuns got munners o_o",
            "woa! o_o",
            "thanks so much! o_o",
        ],
        [  # leave
            "cya :3",
            "goodbye fwiends :3",
            "cum again :3",
            "tysm fwiends :3",
            "bye bye :3",
        ]
    ],
    [ # Steph
        [  # Welcome
            "Oh, wow! Welcome!",
            "Hey! Haven't seen anyone for a while."
        ]
    ],
    [

    ],
    [  # Benji
        "WELCOME!! Waste your money here!",
        "Give your money away! I recommend it!"
    ]
]

# Upgrades / trades
upgrades = {
    # blobs
    "Red Blob": "Pink Blob",
    "Orange Blob": "Pink Blob",
    "Yellow Blob": "Pink Blob",
    "Green Blob": "Pink Blob",
    "Blue Blob": "Pink Blob",
    "Purple Blob": "Pink Blob",
    "Pink Blob": "Rainbow Blob",
    "Rainbow Blob": "Mountain Blob",
    "Mountain Blob": "Void Blob",
    "Void Blob": "Lava Blob",
    "Lava Blob": "Moon Blob",

    # sticks
    "Dyna-Stick": "Dyna-Grenade",
    "Dyna-Grenade": "Dyna-Bomb",
    "Dyna-Bomb": "Dyna-Missile",
    "Dyna-Missile": "Dyna-Nuke",
    "Dyna-Nuke": "Dyna-Antimater Bomb",

    # zip bombs
    ".zip bomb": ".zip nuke",
    ".zip nuke": "9 ronnabite .zip bomb",
    "9 ronnabite .zip bomb": "two billion ronnabite .zip bomb",

    # healing
    "Healing Potion": "Greater Healing Potion",
    "Greater Healing Potion": "Heal Concoction",
    "Heal Concoction": "Heal Totem",

    # juices
    "Rage Juice": "Determination Juice",
    "Determination Juice": "Pacifist Juice",

    # creeps
    "Room Creep": "Demolisher Creep",
    "Item Creep": "Demolisher Creep",

    # chaos
    "Potion of Orb": "Super Potion of Orb",
    "Super Potion of Orb": "Heal Totem",

    # math
    "x=2a-b±b2-4ac" : "d=(x2x2)2+(y2-y1)2",
    "d=(x2x2)2+(y2-y1)2" : "x=(-b±√(b^2-4ac))/(2a)",

    # glowy
    "x=(-b±√(b^2-4ac))/(2a)" : "Glowy Malice",
    "Glowy Malice" : "Glowy Feeling of Unease",
    "Glowy Feeling of Unease" : "Glowy Ultimate Dungeon Prize"
}

trades = {
    # color swaps
    "Red Blob": "Green Blob",
    "Orange Blob": "Blue Blob",
    "Yellow Blob": "Purple Blob",
    "Green Blob": "Red Blob",
    "Blue Blob": "Orange Blob",
    "Purple Blob": "Yellow Blob",

    # blob downgrades
    "Rainbow Blob": "Pink Blob",
    "Mountain Blob": "Rainbow Blob",
    "Void Blob": "Mountain Blob",
    "Lava Blob": "Void Blob",
    "Moon Blob": "Lava Blob",

    # other
    "Dyna-Grenade": ".zip bomb",
    ".zip bomb": "Dyna-Grenade",
    "Healing Potion": "Potion of Orb",
    "Dyna-Bomb": "Healing Potion",
    "Greater Healing Potion": "Rage Juice",
    "Rage Juice": "Greater Healing Potion",
    "Dyna-Missile": ".zip nuke",
    ".zip nuke": "Dyna-Missile",
    "Super Potion of Orb": "Potion of Orb",
    "Heal Concoction": "Determination Juice",
    "Determination Juice": "Heal Concoction",
    "Room Creep": "Item Creep",
    "Item Creep": "Room Creep",
    "Dyna-Nuke": "9 ronnabite .zip bomb",
    "9 ronnabite .zip bomb": "Dyna-Nuke",
    "Heal Totem": "Pacifist Juice",
    "Pacifist Juice": "Heal Totem",
    "Dyna-Antimater Bomb": "two billion ronnabite .zip bomb",
    "two billion ronnabite .zip bomb": "Dyna-Antimater Bomb",
}

Chests1 = ["Wood Chest", "Cheese Chest", "Brick Chest"]
Chests2 = ["Ice Chest", "Bronze Chest"]
Chests3 = ["Magic Chest", "Big Cheese Chest", "Silver Chest"]
Chests4 = ["Purple Chest", "Void Chest", "Gold Chest"]
Chests5 = ["Creepy Chest", "Big Golden Cheese Chest", "Platnum Chest"]
Chests6 = ["Creepier Chest", "Super Cool Chest", "Diamond Chest"]

# loot

Loot1 = [
    "Hardy Scarf",
    "Math Ring",
    "Bottle of Pocket",
]

Loot2 = [
    "Scarf",
    "Ring",
    "Bottle",
]

Loot3 = [
    "Scarf",
    "Ring",
    "Bottle",
]

Loot4 = [
    "Special Purple Scarf",
    "Ring",
    "Bottle",
]

Loot5 = [
    "Meditative Scarf",
    "Ring",
    "Bottle",
]

Loot6 = [
    "Scarf",
    "Explosive Ring",
    "Bottle of Revive"
]

Scarfs = [
    "Hardy Scarf",
    "Scarf",
    "Scarf",
    "Scarf",
    "Meditative Scarf",
    "Special Purple Scarf",
]

Rings = [
    "Math Ring",
    "Ring",
    "Ring",
    "Ring",
    "Ring",
    "Explosive Ring",
]

Bottles = [
    "Bottle of Pocket",
    "Bottle",
    "Bottle",
    "Bottle",
    "Bottle",
    "Bottle of Revive",
]

Other = [

]

loot_bank = [
    "Hardy Scarf", "Math Ring", "Bottle of Pocket",
    "Scarf", "Ring", "Bottle",
    "Scarf", "Ring", "Bottle",
    "Special Purple Scarf", "Ring", "Bottle",
    "Meditative Scarf", "Ring", "Bottle",
    "Scarf", "Explosive Ring", "Bottle of Revive",
]

loot_displays = [
    BOLDWHITE+"Hardy Scarf"+RESET, BOLDWHITE+"Math Ring"+RESET, BOLDWHITE+"Bottle of Pocket"+RESET,
    BOLDGREEN+"Scarf"+RESET, BOLDGREEN+"Ring"+RESET, BOLDGREEN+"Bottle"+RESET,
    BOLDBLUE+"Scarf"+RESET, BOLDBLUE+"Ring"+RESET, BOLDBLUE+"Bottle"+RESET,
    BOLDPURPLE+"Special Purple Scarf"+RESET, BOLDBLUE+"Ring"+RESET, BOLDBLUE+"Bottle"+RESET,
    BOLDYELLOW+"Meditative Scarf"+RESET, BOLDBLUE+"Ring"+RESET, BOLDBLUE+"Bottle"+RESET,
    BOLDRED+"Scarf"+RESET, BOLDBLUE+"Explosive Ring"+RESET, BOLDBLUE+"Bottle of Revive"+RESET,
]

death_messages1 = [  # Generic, <name> ________ <enemy>
" was slain ",
" got put on the wrong side of the grass ",
" was removed from the dungeon ",
" got sent to the bone zone ",
" got got ",
" was erased ",
" has been bonked on the head ",
" got stabbed ",
" was swarmed ",
" was outplayed ",
"'s flailing about has been stopped ",
"'s corpse will be put to good use ",
" was sent away ",
"'s ticker was stopped ",
" was turned into experience points ",
" got skill checked ",
" was reduced to loot ",
" got folded ",
" got sent back to character select ",
" was stomped ",
" was looked at funny ",
" was poked in the eye ",
]

death_messages2 = [  # Generic, <enemy> __________ <name>
" booted ",
" killed ",
" pwned ",
"'s most recent target: ",
" oofed ",
" zapped ",
" ez'd ",
" slapped ",
" yeeted ",
" farted on ",
" shot a rubber chicken at ",
" ded'd ",
]

death_messages3 = [ # Generic, <name> _______________
" didn't make it",
" perished",
" forgot to dodge",
" has a skill issue",
" was slain",
" gave up the ghost",
" kinda just... you know",
" went splat",
" got put on the wrong side of the grass",
" was removed from the dungeon",
" didn't feel too welcome",
" got sent to the bone zone",
" got got",
" was erased",
" has been bonked on the head",
" got stabbed",
" is a loser",
" tried... and failed",
" was swarmed",
" was outplayed",
" expired",
"'s flailing about has stopped",
" went bye bye",
"'s corpse will be put to good use",
" was sent away",
"'s ticker was stopped",
" lost",
" was turned into experience points",
" got skill checked",
" forgot which button was dodge",
" underestimated the dungeon",
" lost an argument with the dungeon",
" was reduced to loot",
" got folded",
" got sent back to character select",
" was stomped",
" was looked at funny",
" was emoted on by thier own ghost",
" farted",
" got stuck in a dishwasher",
" fell down the stairs violently",
" was poked in the eye",
" has fallen down",
]

death_messages4 = [  # Generic, ______________ <name>
"The dungeon booted ",
"Something killed ",
"The dungeon is too hard for ",
"Combat is hard for ",
"Mortality was invented by ",
"Time caught up to ",
"Fate had plans for ",
"Death is undefeated against ",
"Something pwned ",
"The dungeon's most recent target: ",
"Something oofed ",
"The dungeon ez'd ",
"Something slapped ",
"The Dungeon yeeted ",
"Rubber chickens were shot at ",
"Jeremy farted on ",
]

death_messages5 = [  # Post-50, <name> ______________ <enemy>
" was devoured ",
" got donated to science ",
" got turned to fossel fuel ",
" was turned to dust ",
" was murdered ",
" has been added to the collection ",
" was violently unalived ",
" got put to bed ",
" had a forceful heart transplant ",
" was sent to the backrooms ",
" became a punching sandbag ",
" was shoved into a vending machine ",
" is very very much so killed ",
]

death_messages6 = [ # Post-50, <enemy> _______________ <name>
" found ",
" violently exploded ",
" committed arson on ",
" shanked ",
" massacred ",
" flicked ",
" lobotomized ",
" has plans for ",
" expelled ",
" sat on ",
]

death_messages7 = [  # Post-50, <name> __________
" was devoured",
" is nowhere to be found",
" is now part of the dungeon",
" got donated to science",
" is now a ghost",
" got turned to fossel fuel",
" couldn't see",
" was murdered",
" has been added to the collection",
" was violently unalived",
" disappeared without a trace",
" got put to bed",
" had a forceful heart transplant",
" was sent to the backrooms",
" was not the imposter. 1 imposter remains",
" was shoved into a vending machine",
" is very very much so killed",
]

death_messages8 = [  # Post-50, __________ <name>
"The darkness claims ",
"The dungeon swallows ",
"It was too dark for ",
"Something violently exloded ",
"Something committed arson on ",
"Something found ",
"Something shanked ",
"Something massacred ",
"Something flicked ",
"Something lobotomized ",
"The dungeon expelled ",
"The dungeon sat on ",
"Did it hear you? Because it sure did hear "
]

death_messages9 = [ # To a boss/elite, <name> _______________ <enemy/boss>
" couldn't live to tell the tale because of ",
" evaporated in the glory of ",
"'s journey was ended by ",
" hit a rough spot because of ",
" wasn't ready for the fight against ",
" is far less powerful than ",
" spectacularly died because of ",
" was shanked, massacred, flicked, and lobotomized by ",
" learned why everyone fears ",
" discovered the power of ",
" should have run from ",
" was made into a cautionary tale by ",
" found out about ",
" was deleted from existence by ",
" was no match for ",
" got humbled by ",
" was forced to bask in the devine glory of ",
" underestimated ",
" was atomized by ",
" became a speed bump for ",
" challenged ",
" forgot about ",
" couldn't comprehend ",
" learned the hard way about ",
" witnessed the true power of ",
" was instantly promoted to spectator by ",
" got eaten, was digested, and pooped out as a sad turd by ",
" was falling, and kept falling, and kept falling, and- I think you get the idea. -"
]

death_messages10 = [  # To a dark enemy, <name> _________________ <enemy>
" was too scared of ",
" was eaten alive by ",
" died by a thousand horrific screams to ",
" got nibbled on by ",
" was in the territory of ",
"'s corpse was kidnapped by ",
"'s vital organs were removed by ",
" had an extetential crisis because of ",
" was terrified by ",
" is now mush because of ",
" got their toes munched by ",
" WAS SENT TO UR GRANDMAS HOUSE TO EAT COOKIE WITH ",
" heard whispers from ",
" stared too long at ",
" was consumed by ",
" was never seen again after meeting ",
" had their sanity borrowed by ",
" got dragged into the shadows by ",
" looked directly at ",
" became another victim of ",
" was too loud for ",
" was informed of their expiration date by ",
" got [REDACTED] by ",
" was not invited by ",
]

win_messages1 = [  # Generic, <name> __________________
" won",
" did it 100 times",
" should go touch grass",
" didn't die",
" made some enemies sad",
" bested the game",
" did it",
" beat up some bosses",
" beat up some enemies",
" escaped",
" found the prize",
" committed dungeon violence successfully",
" made the dungeon regret existing",
" won and probably won't stop talking about it",
" escaped with all of their organs",
" proved the monsters wrong",
" collected a victory",
" survived out of pure spite",
" is probably bored now",
]

win_messages2 = [  # Generic, ______________ <name>
"The dungeon wasn't hard enough for ",
"The dungeon is a joke for ",
"Enemies don't like ",
"Bosses don't like ",
"Random person -> ",
"Did you know that ",
]

win_messages3 = [ # Perfect, <name> ________________
" made it out without a scratch",
" didn't get hit",
" dodged",
" REALLY needs to touch some grass. Like seriously",
" took the achivement",
" didn't even get a 1-hit wonder",
" won and DEFINATELY won't stop talking about it",
" is genuinely too committed to this low-quality game",
]

# -------------------------
# Enemy spawning progression
# -------------------------
EnemyOptions = enemy_types1
APPLIED_MILESTONES = set()

def get_enemy_options(room_num: int) -> None:
    global EnemyOptions, APPLIED_MILESTONES

    if room_num >= 10 and 10 not in APPLIED_MILESTONES:
        APPLIED_MILESTONES.add(10)
        for e in enemy_types2:
            if e not in EnemyOptions:
                EnemyOptions.append(e)

    if room_num >= 25 and 25 not in APPLIED_MILESTONES:
        APPLIED_MILESTONES.add(25)
        for e in enemy_types3:
            if e not in EnemyOptions:
                EnemyOptions.append(e)

    if room_num >= 40 and 40 not in APPLIED_MILESTONES:
        APPLIED_MILESTONES.add(40)
        for e in enemy_types4:
            if e not in EnemyOptions:
                EnemyOptions.append(e)

    if room_num >= 75 and 75 not in APPLIED_MILESTONES:
        APPLIED_MILESTONES.add(75)
        for e in enemy_types5:
            if e not in EnemyOptions:
                EnemyOptions.append(e)

def spawn_enemy(room_num: int, SpecialEvent: int) -> tuple[list[str], list[float]]:
    options = EnemyOptions

    print("Room " + str(room_num )+ ": " + RoomDisplays[RoomType] + " Room")

    # Base health scaling
    if room_num < 10:
        base_life = math.ceil(room_num / 2)
        roomscale = 1
    elif room_num < 25:
        base_life = math.ceil(room_num / 1.5)
        roomscale = 2
    elif room_num < 40:
        base_life = room_num
        roomscale = 3
    elif room_num < 75:
        base_life = math.ceil(room_num * 1.5)
        roomscale = 4
    else:
        base_life = math.ceil(room_num * 2)
        roomscale = 5

    if room_num == 1:
        enemy_amount = 1
        current = ["Red Slime"]
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif room_num == 2:
        enemy_amount = 1
        current = ["Green Slime"]
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif room_num == 3:
        enemy_amount = 1
        current = ["Dyna-Dot"]
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif room_num == 4:
        enemy_amount = 2
        current = ["Just A Goob", "Dyna-Dot"]
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif room_num == 5:
        enemy_amount = 2
        current = ["Cheese Bro", "Dyna-Dot"]
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif RoomType == 13:
        base_life = 300
        enemy_amount = len(elite_enemies) + 1
        current = elite_enemies.copy()
        current.append("Shiny Terror of the Dungeon")
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif RoomType == 3:
        current = []
        healths = []
    elif RoomType == 4:
        enemy_amount = 1
        current = (random.choice(elite_enemies))
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif RoomType == 5:
        enemy_amount = random.randint(25, 35)
        options = enemy_types1
        current = [random.choice(options) for _ in range(enemy_amount)]
        healths = [int(round(base_life / 10, 1) + random.randint(1, 4)) for _ in range(enemy_amount)]
    elif RoomType == 6:
        enemy_amount = 2
        options = DARK_ENEMIES
        current = [random.choice(options) for _ in range(enemy_amount)]
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
    elif RoomType == 7:
        current = ["Slime God"]
        healths = [150]
    elif RoomType == 8:
        current = ["Dungeon Worm"]
        healths = [300]
    elif RoomType == 9:
        current = ["Astral Reflection"]
        healths = [500]
    elif RoomType == 10:
        current = ["Dungeonemus Maximus"]
        healths = [1000]
    else:
        enemy_amount = random.randint(1, 1 + roomscale)
        if SpecialEvent == 1:  # Cat invasion event
            options = ["Cat"]
        elif SpecialEvent == 2:  # Concok thing event
            options = ["Concok", "Conqua", "Conquaction", "Conqueckter"]

        current = [random.choice(options) for _ in range(enemy_amount)]
        healths = [int(base_life + random.randint(0, 3)) for _ in range(enemy_amount)]
           

    tanky = {"Pink Slime", "Mountain Slime", "Volcano Slime", "Rainbow Slime", "Moon Slime"}
    frail = {"Dyna-Dot", "Dyna-Mott", "Dyna-Mite", "Dyna-Mighty", "Dyna-Rex", "Dyna-Max"}
    bulky_goobs = {"Just A Goob", "Generic Goob", "General Goob"}
    jacked = {"Void Slime"}

    if current:
        if RoomType != 5:
            for i, enemy in enumerate(current):
                if enemy not in bosses:
                    hp = healths[i]

                    if enemy in SLIME_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " drips in!")
                    if enemy in SMOKE_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " appears in a puff of smoke!")
                    if enemy in PHASE_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " phases into reality!")
                    if enemy in AWKWARD_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " is just... there.")
                    if enemy in REVIVAL_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " is reanimated!")
                    if enemy in MUSICAL_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " is conducted into battle!")
                    if enemy in EXPLOSIVE_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " makes an explosive entrance!")
                    if enemy in WIND_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " blows into battle!")
                    if enemy in DARK_ENEMIES:
                        print("a " + enemy_displays[enemy_bank.index(enemy)] + " has found it's prey.")

                    if enemy in tanky:
                        hp = int(hp * 1.2)
                    if enemy in frail:
                        hp = int(hp * 0.5)
                    if enemy in bulky_goobs:
                        hp = int(hp * 2)
                    if enemy in jacked:
                        hp = int(hp * 5)

                    healths[i] = max(1, hp)
                    print("it has " + str(healths[i]) + " health.")
                else:
                    if enemy == "Slime God":
                        input("The air grows cold...")
                        input("A strange goop seeps through the cracks in the walls...")
                        input("A mound forms in the middle of the room!")
                        input("...")
                        print("The " + enemy_displays[enemy_bank.index(enemy)] + " has spawned!!")
                    elif enemy == "Dungeon Worm":
                        input("You hear a rumbling...")
                        input("The floor is trembling...")
                        input("The dungeon flips on it's side!")
                        input("...")
                        print("The " + enemy_displays[enemy_bank.index(enemy)] + " has spawned!!")
                    elif enemy == "Astral Reflection":
                        input("The room is shimmering in etheral energy...")
                        input("Above you, you can see a projection of the stars...")
                        input("Before you, you see... you!")
                        input("...")
                        print("The " + enemy_displays[enemy_bank.index(enemy)] + " has spawned!!")
                    elif enemy == "Dungeonemus Maximus":
                        input("Your mind goes numb...")
                        input("Two glowing eyes appear in front of you...")
                        input("The torches go out...")
                        input("...")
                        print("The " + enemy_displays[enemy_bank.index(enemy)] + " has spawned!!")
                    print("it has " + str(healths[i]) + " health.")
        else:
            print("A whole bunch of enemies spawn!")
    else:
        print("There are no enemies in this room!")

    return current, healths # type: ignore

def achivements_reward():
    AchivementsFile = open('Achivements.json')
    data = json.load(AchivementsFile)
    for i in data["achivements"]:
        if i["progress"] >= i["require"]:
            if i["reward1"] and i["reward1"] not in UnlockedCharacters:
                UnlockedCharacters.append(i["reward1"])
            if i["reward2"]:
                pass
            if i["reward3"]:
                pass

# -------------------------
# Input helpers
# -------------------------
def inventory_check() -> int:
    if not inventory:
        print("What type of attack would you like to use?\n0: " + Sword + "\n1: Character" + "\n2: Check\n")
        while True:
            userinput = input()
            if userinput == "0":
                return -1
            if userinput == "1":
                return -2
            if userinput == "2":
                return -3
    else:
        print("What type of attack would you like to use?\n0: " + Sword + "\n1: Character\n2: Check\n3: Item\n")
        while True:
            userinput = input()
            if userinput == "0":
                return -1
            if userinput == "1":
                return -2
            if userinput == "2":
                return -3
            if userinput == "3":
                break

    while True:
        userinput = input("What inventory item would you like to use? Use item number, and input 0 for none. ").strip()
        if userinput == "0":
            print("you decided not to use an item.")
            return -1
        if not userinput.isdigit():
            print("Please enter a valid response.")
            continue
        idx = int(userinput) - 1
        if 0 <= idx < len(inventory):
            return idx
        print("Please enter a valid response.")

def attack_check(current_enemies: list[str]) -> int:
    while True:
        userinput = input("Which enemy would you like to attack? Use enemy number. ").strip()
        if not userinput.isdigit():
            print("Please enter a valid response.")
            continue
        idx = int(userinput) - 1
        if 0 <= idx < len(current_enemies):
            return idx
        print("Please enter a valid response.")

# -------------------------
# Rewards / effectiveness
# -------------------------
def grant_reward(slain_enemy: str) -> None:
    global inventory, Gold, TotalGold, item_displays, reward_bank
    if slain_enemy not in enemy_bank:
        print("You would have gotten something, but someone forgot to code it!")
        return

    i = enemy_bank.index(slain_enemy)
    reward = reward_bank[i]
    money = money_values[i]

    if money != 0:
        money += random.randrange(0, 3)

    if reward != "Nothing":
        if len(inventory) < MaxInventory:
            inventory.append(reward)
        else:
            while True:
                for idx, item in enumerate(inventory, start=1):
                    print(f"{idx}: {item_displays[reward_bank.index(item)]}")
                print("Your inventory is full!")
                userinput = input("Choose something to replace, or 0 not to replace it with anything.")
                if userinput == "0":
                    print("You didn't take the item.")
                    return
                if userinput.isdigit():
                    if int(userinput) < 31 and int(userinput) > 0:
                        inventory.append(reward)
                        print("You dropped the " + inventory[int(userinput) + 1] + " for the " + reward + ".")
                        inventory.remove(inventory[int(userinput) + 1])
                        return
                    else:
                        print("please enter a valid response.")
                else:
                    print("please enter a valid response.")



    Gold += money
    TotalGold += money
    print("you got " + item_displays[reward_bank.index(reward)] + ", and " + str(money) + " gold!")

def _contains_target(target, enemy: str) -> bool:
    if isinstance(target, str):
        return enemy == target
    return enemy in target

def apply_effectiveness(item: str, enemy: str, your_damage: float) -> int:
    # Keep the strongest checks first
    if item in super_duper_effective and _contains_target(super_duper_effective[item], enemy):
        print("It worked amazingly! Your attack did 200 damage!")
        return int(200 * your_damage)

    if item in super_effective and enemy == super_effective[item]:
        print("It worked super duper well! Your attack did 100 damage!")
        return int(100 * your_damage)

    if item in somewhat_effective and _contains_target(somewhat_effective[item], enemy):
        print("It worked super well! Your attack did 50 damage!")
        return int(50 * your_damage)

    if item in mid_effective and _contains_target(mid_effective[item], enemy):
        print("It worked pretty well! Your attack did 25 damage!")
        return int(25 * your_damage)

    if item in small_effective and _contains_target(small_effective[item], enemy):
        print("It worked sorta well! Your attack did 15 damage!")
        return int(15 * your_damage)

    if item in tiny_effective and _contains_target(tiny_effective[item], enemy):
        print("It worked ok! Your attack did 10 damage!")
        return int(10 * your_damage)

    return 0

# -------------------------
# Combat
# -------------------------

def use_move(enemy_name: str, enemy_health: int) -> tuple[int, int, float, float, float, int, int, int]:
    global HalfDamage
    new_health = enemy_health

    heal = 0
    dodge_multi = 1.0
    damage_multi = 1.0
    defence_multi = 1.0
    disarm = 0
    damage_all = 0
    disarm_all = 0
   
    Move = ""
   
    print("What move would you like to use?\n1: " + Moves[Characters.index(Character)][0] + "\n2: " + Moves[Characters.index(Character)][1] + "\n3: " + Moves[Characters.index(Character)][2] + "\n4: " + Moves[Characters.index(Character)][3])
    while True:
        userinput = input()
        if userinput.isdigit():
            if int(userinput) <= 4 and int(userinput) >= 1:
                Move = Moves[Characters.index(Character)][int(userinput) - 1]
                break
            else:
                print("Please enter a valid response.")
        else:
            print("Please enter a valid response.")
   
    print("You used " + Move + " on " + enemy_name + "!")
   
    if Move == "Sucker Punch":
        print("It did 3 damage.")
        new_health -= 3
   
    if Move == "Omni Kick":
        print("It did 1 damage to all enemies.")
        damage_all = 1
   
    if Move == "Defend":
        print("Next attack does half damage!")
        HalfDamage = 1
   
    if Move == "Concussing Strike":
        if len(CurrentEnemies) > 1:
            print("It stunned the enemy for a turn!")
            disarm = 1
        else:
            print("The enemy dodged it!")
    
    if Move == "Bite":
        print("It did 3 damage.")
        new_health -= 3
    
    if Move == "Absorb":
        print("You absorbed all the Blobs in your inventory!")
        count = len(set(inventory) & set(BLOB_ITEMS))
        for i in range(count):
            Heal += 0.1
        if heal == 0:
            print("But you didn't have any...")
        else:
            print("You healed by " + str(Heal) + " health!")
    
    if Move == "Color Swap":
        pass
   
    if not any(Move in sublist for sublist in Moves):
        print(Move + " did nothing!")

    return new_health, heal, dodge_multi, damage_multi, defence_multi, disarm, damage_all, disarm_all

def attack_enemy(enemy_name: str, enemy_health: int) -> tuple[int, int, float, float, float, int, int, int]:
    global ItemUseScore, LevelBeat, BossLevel, RoomDamage, SkipRoomNow, CurrentEnemies

    new_health = enemy_health

    heal = 0
    dodge_multi = 1.0
    damage_multi = 1.0
    defence_multi = 1.0
    disarm = 0
    damage_all = 0
    disarm_all = 0

    item_idx = inventory_check()

    SlimeGodSpawns = ["Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Pink Slime", "Rainbow Slime"]

    # No item used -> basic attack
    if item_idx == -3:
        print(checks[enemy_bank.index(enemy_name)])
        return new_health, heal, dodge_multi, damage_multi, defence_multi, disarm, damage_all, disarm_all  # type: ignore
    if item_idx == -2:
        return use_move(enemy_name, enemy_health)
    if item_idx == -1:
        input("Press enter to attack!\n")
        new_health -= int(1 * RoomDamage)
        print("you attacked the " + enemy_displays[enemy_bank.index(enemy_name)]+ ".")
        print("it now has " + str(new_health) + " health.")
        tanky = ["Pink Slime", "Rainbow Slime"]
        if enemy_name == "Slime God":
            print("A chunk of the Slime God fell off, and is now a slime!")
            NewEnemy = random.choice(SlimeGodSpawns)
            CurrentEnemies.append(NewEnemy)
            if NewEnemy in tanky:
                CurrentEnemiesHealth.append(random.randint(2, 6))
            else:
                CurrentEnemiesHealth.append(random.randint(1, 3))
            StunnedEnemies.append(0)
            print("a " + enemy_displays[enemy_bank.index(NewEnemy)] + " has spawned!")
            print("it has " + str(CurrentEnemiesHealth[len(CurrentEnemiesHealth) - 1]) + " health.")
       
        if ("Worm Gaurd" in CurrentEnemies and enemy_name == "Dungeon Worm") or "Dungeon Gaurd" in CurrentEnemies:
            print("But the Gaurd blocked some of the attack!")
            print("You only did half damage.")
            new_health = enemy_health - ((enemy_health - new_health) / 2)

        return new_health, heal, dodge_multi, damage_multi, defence_multi, disarm, damage_all, disarm_all  # type: ignore

    ItemUseScore += 2
    item = inventory[item_idx]

    # Flavor text (fixed: use sets instead of reward_bank slices)
    if item in BLOB_ITEMS:
        print("You threw the " + item_displays[reward_bank.index(item)] + " at the " + enemy_displays[enemy_bank.index(enemy_name)] + "!")
    elif item in STICK_ITEMS:
        print("You blew up the " + item_displays[reward_bank.index(item)] + "!")
    elif item in DRINK_ITEMS:
        print("You drank the " + item_displays[reward_bank.index(item)] + "!")
    elif item in JUICE_ITEMS:
        print("You splashed the " + item_displays[reward_bank.index(item)] + " on the " + enemy_displays[enemy_bank.index(enemy_name)] + "!")
    elif item in BOMB_ITEMS:
        print("You executed the " + item_displays[reward_bank.index(item)] + "!")
    elif item in CREEP_ITEMS:
        print("The " + item_displays[reward_bank.index(item)] + " flew out of your hand!")
    elif item in CHEESE_ITEMS:
        print("You tried to use the " + item_displays[reward_bank.index(item)] + ", but you decided otherwise.")
    elif item in MATH_ITEMS:
        print("You used the " + item_displays[reward_bank.index(item)] + "! You hope it works...")
    elif item in CHEAT_ITEMS:
        print("You used the " + item_displays[reward_bank.index(item)] + ", but feel like a cheater... ")
    elif item in WEIRD_ITEMS:
        print("You threw away the " + item_displays[reward_bank.index(item)] + ", and you're pretty glad that it's gone.")
    elif item in DARK_ITEMS:
        print()
    elif item not in reward_bank:
        # Shouldn't happen, but don't crash
        print("you used the " + item_displays[reward_bank.index(item)] + "... It did nothing!")
    else:
        print("you used the " + item_displays[reward_bank.index(item)] + "!")

    # Apply effectiveness
    new_health -= apply_effectiveness(item, enemy_name, RoomDamage)

    if enemy_name == "Slime God" and item not in BLOB_ITEMS:
        print("A chunk of the Slime God fell off, and is now a slime!")
        NewEnemy = random.choice(SlimeGodSpawns)
        CurrentEnemies.append(NewEnemy)
        CurrentEnemiesHealth.append(random.randint(1, 3))
        StunnedEnemies.append(0)
        print("a " + enemy_displays[enemy_bank.index(NewEnemy)] + " has spawned!")
        print("it has " + str(CurrentEnemiesHealth[len(CurrentEnemiesHealth) - 1]) + " health.")

    # Direct effects
    if item == "Dyna-Stick":
        print("It did 10 damage.")
        new_health -= int(10 * RoomDamage)

    elif item == "Dyna-Grenade":
        print("It did 25 damage.")
        new_health -= int(25 * RoomDamage)

    elif item == "Dyna-Bomb":
        print("It did 50 damage.")
        new_health -= int(50 * RoomDamage)

    elif item == "Dyna-Missile":
        print("It did 100 damage.")
        new_health -= int(100 * RoomDamage)

    elif item == "Dyna-Nuke":
        print("It did 200 damage.")
        new_health -= int(200 * RoomDamage)

    elif item == "Dyna-Antimater Bomb":
        print("It did 300 damage.")
        new_health -= int(300 * RoomDamage)

    elif item == "Healing Potion":
        heal = 1
        print("You healed by 1 health.")

    elif item == "Greater Healing Potion":
        heal = 3
        print("You healed by 3 health.")

    elif item == "Heal Concoction":
        heal = 5
        print("You healed by 5 health.")

    elif item == "Heal Totem":
        heal = 10
        print("You healed by 10 health.")

    elif item == ".zip bomb":
        damage_all = int(10 * RoomDamage)
        new_health -= int(5 * RoomDamage)
        print("It dealt 10 damage to all enemies, and 5 bonus damage to the targeted enemy.")

    elif item == ".zip nuke":
        damage_all = int(75 * RoomDamage)
        new_health -= int(25 * RoomDamage)
        print("It dealt 75 damage to all enemies, and 25 bonus damage to the targeted enemy.")

    elif item == "9 ronnabite .zip bomb":
        damage_all = int(150 * RoomDamage)
        new_health -= int(75 * RoomDamage)
        print("It dealt 200 damage to all enemies, and 50 bonus damage to the targeted enemy.")

    elif item == "two billion ronnabite .zip bomb":
        damage_all = int(250 * RoomDamage)
        new_health -= int(100 * RoomDamage)
        print("It dealt 300 damage to all enemies, and 100 bonus damage to the targeted enemy.")

    elif item == "Potion of Orb":
        chaos_multi = random.uniform(1.0, 3.0)
        quarter = random.randrange(0, 4)  # 0..3
        if quarter == 0:
            chaos_multi -= 0.5
        elif quarter == 1:
            chaos_multi -= 0.25
        elif quarter == 2:
            chaos_multi += 0.25
        else:
            chaos_multi += 0.5

        chaos_choice = random.choice(chaos_bank)
        shown = round(chaos_multi, 2)

        if chaos_choice == "Heal":
            heal = max(0, int(round(chaos_multi)))
            print("You were healed by " + str(heal) + ".")

        elif chaos_choice == "Dodge":
            dodge_multi = max(0.1, chaos_multi)
            print("Attacks got x" + str(shown) + " easier or harder.")

        elif chaos_choice == "Damage":
            damage_multi = max(0.1, chaos_multi)
            print("You do x" + str(shown) + " damage.")

        elif chaos_choice == "Defence":
            defence_multi = max(0.1, chaos_multi)
            print("You take /" + str(shown) + " damage.")

    elif item == "Super Potion of Orb":
        chaos_multi = random.uniform(1.5, 5.0)
        quarter = random.randrange(0, 4)
        if quarter == 0:
            chaos_multi -= 0.5
        elif quarter == 1:
            chaos_multi -= 0.25
        elif quarter == 2:
            chaos_multi += 0.25
        else:
            chaos_multi += 0.5

        chaos_choice = random.choice(chaos_bank)
        shown = round(chaos_multi, 2)

        if chaos_choice == "Heal":
            heal = max(0, int(round(chaos_multi)))
            print("You were healed by " + str(heal) + ".")

        elif chaos_choice == "Dodge":
            dodge_multi = max(0.1, chaos_multi)
            print("Attacks got x" + str(shown) + " easier or harder.")

        elif chaos_choice == "Damage":
            damage_multi = max(0.1, chaos_multi)
            print("You do x" + str(shown) + " damage.")

        elif chaos_choice == "Defence":
            defence_multi = max(0.1, chaos_multi)
            print("You take /" + str(shown) + " damage.")

    elif item == "Rage Juice":
        disarm = 1 if BossLevel else 3
        print(("The boss" if BossLevel else "That enemy") + f" is stunned for {disarm} turns!")

    elif item == "Determination Juice":
        disarm = 3 if BossLevel else 9999
        print(("The boss" if BossLevel else "That enemy") + (" is stunned for 3 turns!" if BossLevel else " is stunned for the rest of the room!"))

    elif item == "Pacifist Juice":
        disarm = 5 if BossLevel else 9999
        print(("The boss" if BossLevel else "That enemy") + (" is stunned for 5 turns!" if BossLevel else " is stunned for the rest of the room!"))

    elif item == "Room Creep":
        if not BossLevel:
            print("You can skip the rest of the room.")
            SkipRoomNow = True
        else:
            print("You cannot skip boss rooms.")
            inventory.append("Room Creep")  # refund

    elif item == "Demolisher Creep":
        if not BossLevel:
            print("You dealt 500 damage to all enemies.")
            damage_all = int(500 * RoomDamage)
        else:
            print("The Demolisher Creep doesn't work on boss rooms.")
            inventory.append("Demolisher Creep")  # refund

    elif item == "Item Creep":
        if not BossLevel:
            print("You stole an item from the enemy! It has been added to your inventory.")
            if enemy_name in enemy_bank:
                stolen = reward_bank[enemy_bank.index(enemy_name)]
                if stolen == "Nothing":
                    print("...but the enemy had nothing to steal.")
                    inventory.append("Item Creep")
                elif len(inventory) < MaxInventory:
                    print("...but you had no room.")
                    inventory.append("Item Creep")
                else:
                    inventory.append(stolen)
        else:
            print("You cannot steal items from bosses.")
            inventory.append("Item Creep")  # refund

    elif item in CHEESE_ITEMS or item in DARK_ITEMS:
        inventory.append(item)  # refund

    elif item == "Rainbow Run":
        effect = random.randint(0, 2)
        if effect == 0:
            print("It did nothing, but it looked cool!")
        elif effect == 1:
            print("It healed you for 999 health, but you don't know how!")
            heal = 999
        else:
            print("It did something cool, but you don't know what it was!")
            effect2 = random.randint(0, 2)
            if effect2 == 0:
                damage_all = 999999999
            elif effect2 == 1:
                damage_all = 1
            else:
                new_health = 1

    elif item == "Cat Food":
        print("The enemy ate it.\nIt appreciated the gesture, and healed it by 5 health!")
        new_health += 5

    elif item == "x=2a-b±b2-4ac":
        print("The enemy's health was reduced by 5%!")
        new_health *= 0.95

    elif item == "d=(x2x2)2+(y2-y1)2":
        print("The enemy's health was reduced by 10%!")
        new_health *= 0.90

    elif item == "x=(-b±√(b^2-4ac))/(2a)":
        print("The enemy's health was reduced by 15%!")
        new_health *= 0.85
   
    elif item == "Glowy Malice":
        print("All enemies are stunned for a turn!")
        disarm_all = 1

    elif item == "Glowy Feeling of Unease":
        print("All enemies are stunned for 3 turns!")
        disarm_all = 3
   
    elif item == "Glowy Ultimate Dungeon Prize":
        print("All enemies are stunned for 5 turns!")
        disarm_all = 5
   
    elif item == "Fire Charge":
        print("It did " + str(5 * ((room + 10) * 0.1)) + " damage!")
        new_health -= 5 * ((room + 10) * 0.1)
   
    elif item == "Exploding Spores":
        damage_multi += 0.5
        print("You do more damage!")
   
    elif item == "Gloomper":
        dodge_multi += 0.5
        print("Dodges got easier!")
   
    elif item == "Call to Arms":
        times = random.randint(4, 6)
        for _ in range(times):
            userinput = input('type "attack" to attack! ')
            if userinput != "attack":
                print("You didn't get the attack bonus!")
                print("it now has " + str(new_health) + " health.")
                return new_health, heal, dodge_multi, damage_multi, defence_multi, disarm, damage_all, disarm_all
        print("You successfully attacked!")
        print("It did " + str(10 * ((room + 10) * 0.1)) + " damage.")
        new_health -= 10 * ((room + 10) * 0.1)
   
    elif item == "Arts and Crafts":
        print("It did " + str(25 * ((room + 10) * 0.1)) + " damage!")
        new_health -= 25 * ((room + 10) * 0.1)

    # Consume the used item
    inventory.pop(item_idx)

    # If the item did literally nothing and you didn't skip the room, still bonk for 2
    if new_health == enemy_health and not SkipRoomNow:
        new_health -= int(2 * RoomDamage)
   
    if "Worm Gaurd" in CurrentEnemies and enemy_name == "Dungeon Worm":
        print("But the Worm Gaurd blocked some of the attack!")
        print("You only did half damage.")
        new_health = enemy_health - ((enemy_health - new_health) / 2)

    print("it now has " + str(new_health) + " health.")
    return new_health, heal, dodge_multi, damage_multi, defence_multi, disarm, damage_all, disarm_all  # type: ignore

def enemy_attack(attacker_idx: int, your_life: float, stunned: list[int], enemies: list[str], enemy_health: float) -> float:
    global DodgeScore, RoomDodge, RoomDefence, CurrentEnemiesHealth, SpectatorHits, CauseOfDeath

    def do_simple_dodges(times: int, damage: float) -> float:
        nonlocal new_life
        times = max(1, times)
        for _ in range(times):
            userinput = input('type dodge to dodge! ')
            if userinput != "dodge":
                take_damage(damage)
                print("you failed to dodge... It dealt " + str(float(damage)) + " damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You have dodged all attacks!")
        dodge_success()
        return new_life

    def do_prompt_dodges(times: int, choices: list[str], damage: float) -> float:
        nonlocal new_life
        times = max(1, times)
        for _ in range(times):
            expected = random.choice(choices)
            if (choices != food_1) and (choices != food_1 +food_2) and (choices != food_1 + food_2 + food_3):
                userinput = input("type " + expected + " to dodge! ")
            else:
                userinput = input("NOW SPELL: " + expected + ". ")
            if userinput != expected:
                take_damage(damage)
                print("you failed to dodge... It dealt " + str(float(damage)) + " damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You have dodged all attacks!")
        dodge_success()
        return new_life

    def take_damage(amount: float) -> float:
        nonlocal new_life
        new_life -= amount / max(0.0001, RoomDefence)
        new_life = round(new_life, 2)
        return new_life

    def dodge_success() -> None:
        global DodgeScore
        DodgeScore += 1

    enemy_name = enemies[attacker_idx]

    if stunned[attacker_idx] > 0:
        stunned[attacker_idx] -= 1
        print("\nThe " + enemy_displays[enemy_bank.index(enemy_name)] + " is attacking!\n")
        print("But it's stunned, so it can't attack!")
        return your_life

    new_life = your_life
    print("\nThe " + enemy_displays[enemy_bank.index(enemy_name)] + " is attacking!\n")
    CauseOfDeath = enemy_name

    weak_no_attack = {"Just A Goob", "Generic Goob", "General Goob", "Worm Gaurd"}
    if enemy_name in weak_no_attack:
        print("But it is too weak... It failed to attack.")
        return new_life

    if enemy_name in {"Red Slime", "Orange Slime", "Yellow Slime", "Green Slime", "Blue Slime", "Purple Slime", "Green Flame I"}:
        times = round(random.randint(1, 4) / max(0.25, RoomDodge))
        return do_simple_dodges(times, 1)

    if enemy_name == "Pink Slime":
        times = round(random.randint(2, 6) / max(0.25, RoomDodge))
        return do_simple_dodges(times, 1)

    if enemy_name == "Rainbow Slime":
        times = round(random.randint(1, 4) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, combo_dodges, 1)

    if enemy_name == "Void Slime":
        times = round(random.randint(3, 7) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, combo_dodges, 2)
   
    if enemy_name == "Blue Flame III":
        times = round(random.randint(3, 7) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, combo_dodges, 2)

    if enemy_name == "Moon Slime":
        dodge_type = random.choice(["simple", "prompt"])
        if dodge_type == "simple":
            times = round(random.randint(5, 15) / max(0.25, RoomDodge))
            return do_simple_dodges(times, 4)
        times = round(random.randint(3, 9) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, combo_dodges, 4)

    if enemy_name == "Dyna-Dot":
        times = round(random.randint(1, 3) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, hard_dodges, 2)

    if enemy_name in ["Dyna-Mott", "Red Flame I"]:
        times = round(random.randint(2, 5) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, hard_dodges, 2)

    if enemy_name == ["Dyna-Mite", "Red Flame II"]:
        times = round(random.randint(2, 5) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, harder_dodges, 3)

    if enemy_name == ["Dyna-Mighty", "Red Flame III"]:
        times = round(random.randint(3, 7) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, hardest_dodges, 3)

    if enemy_name == "Dyna-Rex":
        times = round(random.randint(3, 7) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, harderest_dodges, 4)

    if enemy_name == "Dyna-Max":
        times = round(random.randint(4, 8) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, hardererest_dodges, 5)

    if enemy_name == "Concok":
        expected = random.choice(concok_dodge)
        userinput = input("Repeat concok's lecture: " + expected + " ")
        if userinput != expected:
            take_damage(1)
            print("you failed to dodge... It dealt 1 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You have dodged its attack!")
        dodge_success()
        return new_life

    if enemy_name == "Conqua":
        expected = random.choice(concok_dodge)
        userinput = input("Repeat conqua's lecture: " + expected + " ")
        if userinput != expected:
            take_damage(2)
            print("you failed to dodge... It dealt 2 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You have dodged its attack!")
        dodge_success()
        return new_life

    if enemy_name == "Conquaction":
        times = round(random.randint(2, 3) / max(0.25, RoomDodge))
        for _ in range(max(1, times)):
            expected = random.choice(concok_dodge)
            userinput = input("Repeat conquaction's lecture: " + expected + " ")
            if userinput != expected:
                take_damage(3)
                print("you failed to dodge... It dealt 3 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You have dodged its attacks!")
        dodge_success()
        return new_life

    if enemy_name == "Conqueckter":
        times = round(random.randint(3, 5) / max(0.25, RoomDodge))
        for _ in range(max(1, times)):
            expected = random.choice(concok_dodge)
            userinput = input("Repeat conqueckter's lecture: " + expected + " ")
            if userinput != expected:
                take_damage(4)
                print("you failed to dodge... It dealt 4 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You have dodged its attacks!")
        dodge_success()
        return new_life

    if enemy_name in {"Mountain Slime", "Green Flame II"}:
        times = round(random.randint(3, 9) / max(0.25, RoomDodge))
        return do_simple_dodges(times, 2)

    if enemy_name == {"Volcano Slime", "Green Flame III"}:
        times = round(random.randint(4, 12) / max(0.25, RoomDodge))
        return do_simple_dodges(times, 3)

    if enemy_name == "Yellow Flame II":
        input("The Yellow Flame II is charging up...")
        start = time.monotonic()
        userinput = input('You have 5 seconds to type "dodge"!! ')
        elapsed = time.monotonic() - start
        if userinput != "dodge" or elapsed > 5.0:
            take_damage(2)
            print("You failed to dodge... It dealt 2 damage.")
            print("You took " + str(round(elapsed, 3)) + " seconds.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You dodged the attack!")
        dodge_success()
        return new_life
   
    if enemy_name == "Yellow Flame III":
        input("The Yellow Flame III is charging up...")
        start = time.monotonic()
        userinput = input('You have 3 seconds to type "dodge"!! ')
        elapsed = time.monotonic() - start
        if userinput != "dodge" or elapsed > 3.0:
            take_damage(2)
            print("You failed to dodge... It dealt 2 damage.")
            print("You took " + str(round(elapsed, 3)) + " seconds.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You dodged the attack!")
        dodge_success()
        return new_life

    if enemy_name == "Tonadoe":
        input("The Tonadoe is charging up...")
        start = time.monotonic()
        userinput = input('You have 3 seconds to type "dodge"!! ')
        elapsed = time.monotonic() - start
        if userinput != "dodge" or elapsed > 3.0:
            take_damage(2)
            print("You failed to dodge... It dealt 2 damage.")
            print("You took " + str(round(elapsed, 3)) + " seconds.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You dodged the attack!")
        dodge_success()
        return new_life

    if enemy_name == "Typhoonoe":
        input("The Typhoonoe is charging up...")
        start = time.monotonic()
        userinput = input('You have 1.5 seconds to type "dodge"!! ')
        elapsed = time.monotonic() - start
        if userinput != "dodge" or elapsed > 1.5:
            take_damage(3)
            print("You failed to dodge... It dealt 3 damage.")
            print("You took " + str(round(elapsed, 3)) + " seconds.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You dodged the attack!")
        dodge_success()
        return new_life

    if enemy_name == "Hurricaneadoe":
        input("The Hurricaneadoe is charging up...")
        start = time.monotonic()
        userinput = input('You have 0.75 seconds to type "dodge"!! ')
        elapsed = time.monotonic() - start
        if userinput != "dodge" or elapsed > 0.75:
            take_damage(4)
            print("You failed to dodge... It dealt 4 damage.")
            print("You took " + str(round(elapsed, 3)) + " seconds.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You dodged the attack!")
        dodge_success()
        return new_life

    if enemy_name == "Timecreeper":
        pauses = round(random.randint(7, 13) / max(0.25, RoomDodge))
        for _ in range(max(1, pauses)):
            input("it's... not attacking? Press enter to continue.")

        expected = random.choice(hard_dodges)
        start = time.monotonic()
        userinput = input("You have 3 seconds to type " + expected + "!! ")
        elapsed = time.monotonic() - start

        if userinput != expected or elapsed > 3.0:
            take_damage(3)
            print("You failed to dodge... It dealt 3 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life

        print("You have dodged its attacks!")
        dodge_success()
        return new_life

    if enemy_name == "Spacecreeper":
        input("The Spacecreeper is charging up...")
        start = time.monotonic()
        userinput = input('Type "dodge" in exactly 5 seconds! ')
        elapsed = time.monotonic() - start

        in_window = (4.5 - (RoomDodge * 0.05) <= elapsed <= 5.5 + (RoomDodge * 0.05))

        if userinput != "dodge" or not in_window:
            take_damage(3)
            print("You took " + str(round(elapsed, 2)) + " seconds to respond.")
            print("You failed to dodge... It dealt 3 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life

        print("Perfect timing! You dodged the attack!")
        dodge_success()
        return new_life

    if enemy_name == "Deathcreeper":
        for _ in range(round(random.randint(5, 10) / max(0.25, RoomDodge))):
            input("It's... doing something?? Press enter to continue.")
        expected = random.choice(hard_dodges)
        start = time.monotonic()
        userinput = input('QUICK, Type "' + expected + '" in exactly 3 seconds! ')
        elapsed = time.monotonic() - start

        in_window = (2.5 - (RoomDodge * 0.05) <= elapsed <= 3.5 + (RoomDodge * 0.05))

        if userinput != expected or not in_window:
            take_damage(4.9)
            print("You took " + str(round(elapsed, 2)) + " seconds to respond.")
            print("You failed to dodge... It dealt 4.9 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life

        print("Perfect timing! You dodged the attack!")
        dodge_success()
        return new_life

    if enemy_name in ["ORB OF SILLY", "Purple Flame II"]:
        return do_prompt_dodges(1, harderest_dodges, 1)

    if enemy_name in ["ORB OF GOOFY", "Purple Flame III"]:
        return do_prompt_dodges(1, hardererest_dodges, 3)

    if enemy_name == "D-Pad Guy":
        sequences = random.randrange(1, 3)
        for _ in range(sequences):
            length = random.randrange(3, 5)
            expected = "".join(random.choice(["w", "a", "s", "d"]) for _ in range(length))
            userinput = input("Type " + expected + " to dodge! ")
            if userinput != expected:
                take_damage(1)
                print("You failed to dodge... it dealt 1 damage.")
                print("You have " + str(new_life) + " lives left.")
                return new_life
        print("You have dodged all attacks!")
        dodge_success()
        return new_life

    if enemy_name == "D-Pad Man":
        sequences = random.randrange(4, 8)
        for _ in range(sequences):
            length = random.randrange(3, 7)
            expected = "".join(random.choice(["w", "a", "s", "d"]) for _ in range(length))
            userinput = input("Type " + expected + " to dodge! ")
            if userinput != expected:
                take_damage(2)
                print("You failed to dodge... it dealt 2 damage.")
                print("You have " + str(new_life) + " lives left.")
                return new_life
        print("You have dodged all attacks!")
        dodge_success()
        return new_life

    if enemy_name == "D-Pad Sir":
        sequences = random.randrange(8, 15)
        for _ in range(sequences):
            length = random.randrange(4, 8)
            expected = "".join(random.choice(["w", "a", "s", "d", " "]) for _ in range(length))
            userinput = input("Type " + expected + " to dodge! ")
            if userinput != expected:
                take_damage(3)
                print("You failed to dodge... it dealt 3 damage.")
                print("You have " + str(new_life) + " lives left.")
                return new_life
        print("You have dodged all attacks!")
        dodge_success()
        return new_life

    if enemy_name == "D-Pad Person":
        sequences = random.randrange(15, 25)
        for _ in range(sequences):
            length = random.randrange(6, 14)
            expected = "".join(random.choice(["w", "a", "s", "d", " ", "q", "e", "z", "x", "c"]) for _ in range(length))
            userinput = input("Type " + expected + " to dodge! ")
            if userinput != expected:
                take_damage(4)
                print("You failed to dodge... it dealt 4 damage.")
                print("You have " + str(new_life) + " lives left.")
                return new_life
        print("You have dodged all attacks!")
        dodge_success()
        return new_life

    if enemy_name == "Cheese Bro":
        attack_type = random.randrange(0, 3)
        if attack_type == 0:
            times = round(random.randint(2, 6) / max(0.25, RoomDodge))
            return do_simple_dodges(times, 1)
        if attack_type == 1:
            times = round(random.randint(1, 3) / max(0.25, RoomDodge))
            return do_prompt_dodges(times, hard_dodges, 2)
        return do_prompt_dodges(1, harderest_dodges, 2)

    if enemy_name == "Big Cheese":
        attack_type = random.randrange(0, 6)
        if attack_type == 0:
            times = round(random.randint(3, 9) / max(0.25, RoomDodge))
            return do_simple_dodges(times, 2)
        if attack_type == 1:
            times = round(random.randint(2, 5) / max(0.25, RoomDodge))
            return do_prompt_dodges(times, harder_dodges, 2)
        if attack_type == 2:
            return do_prompt_dodges(1, harderest_dodges, 2)
        if attack_type == 3:
            expected = random.choice(concok_dodge)
            userinput = input("Repeat big cheese's lecture: " + expected + " ")
            if userinput != expected:
                take_damage(3)
                print("you failed to dodge... It dealt 3 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You have dodged its attack!")
            dodge_success()
            return new_life
        if attack_type == 4:
            sequences = random.randrange(4, 8)
            for _ in range(sequences):
                length = random.randrange(3, 7)
                expected = "".join(random.choice(["w", "a", "s", "d"]) for _ in range(length))
                userinput = input("Type " + expected + " to dodge! ")
                if userinput != expected:
                    take_damage(2)
                    print("You failed to dodge... it dealt 2 damage.")
                    print("You have " + str(new_life) + " lives left.")
                    return new_life
            print("You have dodged all attacks!")
            dodge_success()
            return new_life
        times = round(random.randint(2, 4) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, combo_dodges, 2)

    if enemy_name == "Golden Big Cheese Bro":
        attack_type = random.randrange(0, 10)
        if attack_type == 0:
            times = round(random.randint(4, 12) / max(0.25, RoomDodge))
            return do_simple_dodges(times, 3)
        if attack_type == 1:
            times = round(random.randint(3, 7) / max(0.25, RoomDodge))
            return do_prompt_dodges(times, hardest_dodges, 2)
        if attack_type == 2:
            return do_prompt_dodges(1, harderest_dodges, 2)
        if attack_type == 3:
            for _ in range(random.randint(1, 3)):
                expected = random.choice(concok_dodge)
                userinput = input("Repeat the golden big cheese bro's lecture: " + expected + " ")
                if userinput != expected:
                    take_damage(3)
                    print("you failed to dodge... It dealt 3 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            print("You have dodged its attacks!")
            dodge_success()
            return new_life
        if attack_type == 4:
            sequences = random.randrange(5, 11)
            for _ in range(sequences):
                length = random.randrange(3, 7)
                expected = "".join(random.choice(["w", "a", "s", "d"]) for _ in range(length))
                userinput = input("Type " + expected + " to dodge! ")
                if userinput != expected:
                    take_damage(2)
                    print("You failed to dodge... it dealt 2 damage.")
                    print("You have " + str(new_life) + " lives left.")
                    return new_life
            print("You have dodged all attacks!")
            dodge_success()
            return new_life
        if attack_type == 5:
            times = round(random.randint(3, 7) / max(0.25, RoomDodge))
            return do_prompt_dodges(times, combo_dodges, 2)
        if attack_type == 6:
            take_damage(0.5)
            print("The golden big cheese bro is trying to be sneaky with a weak attack...")
            print("you failed to dodge... It dealt 0.5 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        if attack_type == 7:
            input("The golden big cheese bro is charging up an attack...")
            start = time.monotonic()
            userinput = input('Type "dodge" in exactly 5 seconds! ')
            elapsed = time.monotonic() - start

            in_window = (4.0 - (RoomDodge * 0.05) <= elapsed <= 6.0 + (RoomDodge * 0.05))
            if in_window and userinput == "dodge":
                print("Perfect timing! You dodged the attack!")
                dodge_success()
                return new_life
            take_damage(3)
            print("You took " + str(round(elapsed, 2)) + " seconds to respond.")
            print("You failed to dodge... It dealt 3 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        if attack_type == 8:
            input("The golden big cheese bro is charging up an attack...")
            start = time.monotonic()
            userinput = input('You have 1.5 seconds to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput == "dodge" and elapsed <= 1.5:
                print("You dodged the attack!")
                dodge_success()
                return new_life
            take_damage(3)
            print("You failed to dodge... It dealt 3 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        pauses = round(random.randint(7, 13) / max(0.25, RoomDodge))
        for _ in range(max(1, pauses)):
            input("it's... not attacking? Press enter to continue.")
        expected = random.choice(hard_dodges)
        start = time.monotonic()
        userinput = input("You have 3 seconds to type " + expected + "!! ")
        elapsed = time.monotonic() - start
        if userinput != expected or elapsed > 3.0:
            take_damage(3)
            print("You failed to dodge... It dealt 3 damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You have dodged its attacks!")
        dodge_success()
        return new_life

    if enemy_name == "Cat":
        if enemy_health > room:
            times = round(random.randint(3, 7) / max(0.25, RoomDodge))
            return do_prompt_dodges(times, ["meow", "purr", "hiss"], 1)
        print("Teh kat reveals iz wrath!!1!1!")
        times = round(random.randint(3, 7) / max(0.25, RoomDodge))
        return do_prompt_dodges(
            times,
            ["meowmeowmeow", "PURR PURR", "hissssih", '<"meow">', "PurR", "#Hiss", "Woem", "PurR!", "hiss??", "MEOW!!!", "Meow'th"],
            3
        )

    if enemy_name == "Math.png":
        Number1 = random.randint(1, 9)
        Number2 = random.randint(1, 9)
        Positive = random.randint(0, 1)
        if Positive == 0:
            userinput = input("What's " + str(Number1) + " + " + str(Number2) + "? ")
            if userinput == str(Number1 + Number2):
                print("You have dodged all attacks!")
                dodge_success()
                return new_life
            print("You failed to dodge... it did 1 damage.")
            print("The correct answer was " + str(Number1 + Number2))
            new_life -= 1
            return new_life
        if Positive == 1:
           userinput = input("What's " + str(Number1) + " - " + str(Number2) + "? ")
           if userinput == str(Number1 - Number2):
                print("You have dodged all attacks!")
                dodge_success()
                return new_life
           print("You failed to dodge... it did 1 damage.")
           print("The correct answer was " + str(Number1 - Number2))
         
           new_life -= 1
           return new_life

    if enemy_name == "Math.wav":
        Number1 = random.randint(1, 9)
        Number2 = random.randint(1, 9)
        userinput = input("What's " + str(Number1) + " * " + str(Number2) + "? ")
        if userinput == str(Number1 * Number2):
            print("You have dodged all attacks!")
            dodge_success()
            return new_life
        print("You failed to dodge... it did 3 damage.")
        print("The correct answer was " + str(round(Number1 * Number2)))
        new_life -= 3
        return new_life
   
    if enemy_name == "Math.mp4":
        Number1 = random.randint(1, 20)
        Number2 = random.randint(1, 20)
        Number3 = random.randint(1, 20)
        userinput = input("What's " + str(Number1) + " + " + str(Number2) + " - " + str(Number3) + "? ")
        if userinput == str(Number1 + Number2 - Number3):
            print("You have dodged all attacks!")
            dodge_success()
            return new_life
        print("You failed to dodge... it did 4 damage.")
        print("The correct answer was " + str(Number1 + Number2 - Number3))
        new_life -= 4
        return new_life

    if enemy_name == "Shiny Gloom":
        times = random.randint(1, 4)
        CurrentEnemies.remove("Shiny Gloom")
        if "Shiny Gloom" in CurrentEnemies:
            CurrentEnemies.append("Shiny Gloom")
            print("The Shiny Gloom calls to the other Shiny Gloom for help!")
            times = max(1, times)
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(1)
                    print("you failed to dodge... It dealt 1 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            input("You have dodged the attack!")
            dodge_success()
            start = time.monotonic()
            userinput = input('You have 3 seconds to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 3.0:
                take_damage(2)
                print("You failed to dodge... It dealt 1 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        elif "Shiny Doom" in CurrentEnemies:
            CurrentEnemies.append("Shiny Gloom")
            print("The Shiny Gloom calls to the Shiny Doom for help!")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(1)
                    print("you failed to dodge... It dealt 1 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            input("You have dodged the attack!")
            dodge_success()
            start = time.monotonic()
            userinput = input('You have 2 seconds to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 2.0:
                take_damage(3)
                print("You failed to dodge... It dealt 3 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        elif "Shiny Terror of the Dungeon" in CurrentEnemies:
            CurrentEnemies.append("Shiny Gloom")
            print("The Shiny Gloom calls to the Shiny Terror of the Dungeon for help!")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(1)
                    print("you failed to dodge... It dealt 1 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            input("You have dodged the attack!")
            dodge_success()
            start = time.monotonic()
            userinput = input('You have 1 second to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 1.0:
                take_damage(4)
                print("You failed to dodge... It dealt 4 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        else:
            print("The Shiny Gloom has no one to help it out!")
            do_simple_dodges(times, 1)

    if enemy_name == "Shiny Doom":
        times = random.randint(2, 5)
        CurrentEnemies.remove("Shiny Doom")
        if "Shiny Gloom" in CurrentEnemies:
            print("The Shiny Gloom calls to the Shiny Gloom for help!")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(2)
                    print("you failed to dodge... It dealt 2 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            start = time.monotonic()
            userinput = input('You have 3 seconds to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 3.0:
                take_damage(2)
                print("You failed to dodge... It dealt 2 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        elif "Shiny Doom" in CurrentEnemies:
            CurrentEnemies.append("Shiny Doom")
            print("The Shiny Gloom calls to the other Shiny Doom for help!")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(2)
                    print("you failed to dodge... It dealt 2 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            start = time.monotonic()
            userinput = input('You have 2 seconds to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 2.0:
                take_damage(3)
                print("You failed to dodge... It dealt 3 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        elif "Shiny Terror of the Dungeon" in CurrentEnemies:
            print("The Shiny Gloom calls to the Shiny Terror of the Dungeon for help!")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(2)
                    print("you failed to dodge... It dealt 2 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            start = time.monotonic()
            userinput = input('You have 1 second to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 1.0:
                take_damage(4)
                print("You failed to dodge... It dealt 4 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        else:
            print("The Shiny Gloom has no one to help it out!")
            do_simple_dodges(times, 2)


    if enemy_name == "Shiny Terror of the Dungeon":
        CurrentEnemies.remove("Shiny Terror of the Dungeon")
        times = random.randint(3, 6)
        if "Shiny Gloom" in CurrentEnemies:
            print("The Shiny Terror of the Dungeon calls to the Shiny Gloom for help!")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(3)
                    print("you failed to dodge... It dealt 3 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            start = time.monotonic()
            userinput = input('You have 3 seconds to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 3.0:
                take_damage(2)
                print("You failed to dodge... It dealt 2 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        elif "Shiny Doom" in CurrentEnemies:
            print("The Shiny Terror of the Dungeon calls to the Shiny Doom for help!")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(3)
                    print("you failed to dodge... It dealt 3 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            start = time.monotonic()
            userinput = input('You have 2 seconds to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 2.0:
                take_damage(3)
                print("You failed to dodge... It dealt 3 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        elif "Shiny Terror of the Dungeon" in CurrentEnemies:
            print("The Shiny Terror of the Dungeon calls to the other Shiny Terror of the Dungeon for help!")
            CurrentEnemies.append("Shiny Terror of the Dungeon")
            for _ in range(times):
                userinput = input('type dodge to dodge! ')
                if userinput != "dodge":
                    take_damage(3)
                    print("you failed to dodge... It dealt 3 damage.")
                    print("you have " + str(new_life) + " life left.")
                    return new_life
            start = time.monotonic()
            userinput = input('You have 1 second to type "dodge"!! ')
            elapsed = time.monotonic() - start
            if userinput != "dodge" or elapsed > 1.0:
                take_damage(4)
                print("You failed to dodge... It dealt 4 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            print("You dodged the attack!")
            dodge_success()
            return new_life
        else:
            print("The Shiny Terror of the Dungeon has no one to help it out!")
            do_simple_dodges(times, 3)

    if enemy_name == "Holy Microwave":
        times = round(random.randint(1, 2) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, food_1, 2)

    if enemy_name == "Holy Grill":
            times = round(random.randint(2, 4) / max(0.25, RoomDodge))
            return do_prompt_dodges(times, food_1 + food_2, 3)

    if enemy_name == "Holy Oven":
            times = round(random.randint(3, 6) / max(0.25, RoomDodge))
            return do_prompt_dodges(times, food_1 + food_2 + food_3, 4)

    if enemy_name == "Flameboi":
        times = round(random.randint(1, 2) / max(0.25, RoomDodge))
        return do_simple_dodges(times, 1)
   
    if enemy_name == "Exploding Mush":
        times = round(random.randint(1, 2) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, hard_dodges, 1.5)
   
    if enemy_name == "Gloompy":
        times = round(random.randint(1, 2) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, harder_dodges, 2)
   
    if enemy_name == "Voice From Above":
        times = round(random.randint(1, 2) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, hardest_dodges, 2.5)

    if enemy_name == "Googly Eye Storm":
        times = round(random.randint(1, 2) / max(0.25, RoomDodge))
        return do_prompt_dodges(times, harderest_dodges, 3)
   
    if enemy_name == "Orange Flame III":
        times = round(random.randint(11, 30) / max(0.25, RoomDodge))
        do_prompt_dodges(times, easy_dodges, 2)

    if enemy_name == "Rainbow Flame":
        print("■ ■ ■ ■ ■ ■ ■")
        for _ in range(7):
            userinput = input('type dodge to dodge! ')
            if userinput != "dodge":
                take_damage(2)
                print("you failed to dodge... It dealt " + str(float(2)) + " damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You dodged the first attack!")
        dodge_success()
        print("■ ■ ■ ■ ■ ■ □")
        for _ in range(4):
            expected = random.choice(hardest_dodges)
            userinput = input("type " + expected + " to dodge! ")
            if userinput != expected:
                take_damage(2)
                print("you failed to dodge... It dealt " + str(float(2)) + " damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You dodged the second attack!")
        dodge_success()
        print("■ ■ ■ ■ ■ □ □")
        input("The Rainbow Flame is charging up...")
        start = time.monotonic()
        userinput = input('You have 3 seconds to type "dodge"!! ')
        elapsed = time.monotonic() - start
        if userinput != "dodge" or elapsed > 3.0:
            take_damage(2)
            print("You failed to dodge... It dealt 2 damage.")
            print("You took " + str(round(elapsed, 3)) + " seconds.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You dodged the third attack!")
        dodge_success()
        print("■ ■ ■ ■ □ □ □")
        expected = random.choice(hardererest_dodges)
        userinput = input("type " + expected + " to dodge! ")
        if userinput != expected:
            take_damage(2)
            print("you failed to dodge... It dealt " + str(float(2)) + " damage.")
            print("you have " + str(new_life) + " life left.")
            return new_life
        print("You dodged the fourth attack!")
        dodge_success()
        print("■ ■ ■ □ □ □ □")
        for _ in range(4):
            expected = random.choice(combo_dodges)
            userinput = input("type " + expected + " to dodge! ")
            if userinput != expected:
                take_damage(2)
                print("you failed to dodge... It dealt " + str(float(2)) + " damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You dodged the fifth attack!")
        dodge_success()
        print("■ ■ □ □ □ □ □")
        for _ in range(25):
            expected = random.choice(easy_dodges)
            userinput = input("type " + expected + " to dodge! ")
            if userinput != expected:
                take_damage(2)
                print("you failed to dodge... It dealt " + str(float(2)) + " damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("You dodged the fifth attack!")
        dodge_success()
        print("■ □ □ □ □ □ □")
        print("The Rainbow Flame heals the Dungeon Worm by 25 HP!")
        CurrentEnemiesHealth[0] += 25

    if enemy_name == "Presuiter":
        Grid = [["□", "□", "□", "□", "□"], ["□", "■", "□", "□", "□"], ["□", "□", "□", "□", "□"], ["□", "□", "□", "▲", "□"], ["□", "□", "□", "□", "□"]]
        PlayerLocation = [1, 1]
        PresuiterLocation = [3, 3]

        print("Run away from the presuiter! Use WASD.")

        for Turns in range(10):
            print(str(Turns) + " / 10")
            userinput = input(" ".join(Grid[0]) + "\n" + " ".join(Grid[1]) + "\n" + " ".join(Grid[2]) + "\n" + " ".join(Grid[3]) + "\n" + " ".join(Grid[4]) + "\n").lower()
            print("\033[F"*1, end="")
            print(" "*len(userinput))
            print("\033[F"*1, end="")
            TurnTaken = False
            while TurnTaken == False:
                if userinput in ["w", "a", "s", "d"]:
                    if userinput == "w":
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "□"
                        PlayerLocation[1] = (PlayerLocation[1] - 1) % 5
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "■"
                    if userinput == "a":
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "□"
                        PlayerLocation[0] = (PlayerLocation[0] - 1) % 5
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "■"
                    if userinput == "s":
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "□"
                        PlayerLocation[1] = (PlayerLocation[1] + 1) % 5
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "■"
                    if userinput == "d":
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "□"
                        PlayerLocation[0] = (PlayerLocation[0] + 1) % 5
                        Grid[PlayerLocation[1]][PlayerLocation[0]] = "■"
                    if PresuiterLocation[0] < PlayerLocation[0]:
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "□"
                        PresuiterLocation[0] = (PresuiterLocation[0] + 1) % 5
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "▲"
                    if PresuiterLocation[0] > PlayerLocation[0]:
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "□"
                        PresuiterLocation[0] = (PresuiterLocation[0] - 1) % 5
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "▲"
                    if PresuiterLocation[1] < PlayerLocation[1]:
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "□"
                        PresuiterLocation[1] = (PresuiterLocation[1] + 1) % 5
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "▲"
                    if PresuiterLocation[1] > PlayerLocation[1]:
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "□"
                        PresuiterLocation[1] = (PresuiterLocation[1] - 1) % 5
                        Grid[PresuiterLocation[1]][PresuiterLocation[0]] = "▲"
                    TurnTaken = True
                else:
                    print("Please enter a valid response.")
                    userinput = input("")
                    print("\033[F"*2, end="")
                    print("                              \n" + " "*len(userinput))
                    print("\033[F"*2, end="")
            print("\033[F"*6, end="")
            if PresuiterLocation == PlayerLocation:
                print("         \n"*6, end="")
                print("\033[F"*6, end="")
                print("You failed to dodge... it did 3 damage.")
                take_damage(3)
                print("you have " + str(new_life) + " life left.")
                return new_life
        print("         \n"*6, end="")
        print("\033[F"*6, end="")
        print("You dodged the attack!")
        dodge_success()
        return new_life

    if enemy_name == "Screamer":
        return do_prompt_dodges(1, scream_dodges, 3)
   
    if enemy_name == "Gazer":
        expected = "dodge"
        for i in range(random.randint(5, 7)):
            userinput = input('type ' + expected + ' to dodge! ')
            if userinput != expected:
                take_damage(3)
                print("you failed to dodge... It dealt 3 damage.")
                print("you have " + str(new_life) + " life left.")
                return new_life
            expected += " dodge"
        dodge_success()
        print("You have dodged all attacks!")
        return new_life

    if enemy_name == "Spectator":
        times = random.randint(2, 5)
        for _ in range(times):
            userinput = input('type dodge to dodge! ')
            if userinput != "dodge":
                SpectatorHits += 1
                if SpectatorHits >= 5:
                    take_damage(99999)
                    print("You failed to dodge... it did 99999 damage.")
                    return new_life
        dodge_success()
        print("You have dodged all attacks!")
        return new_life

    if enemy_name == "Slime God":
        if CurrentEnemiesHealth[0] > 100:
            attack_type = random.randint(0, 2)
            if attack_type == 0:
                times = round(random.randint(5, 7) / max(0.25, RoomDodge))
                return do_simple_dodges(times, 2)
            elif attack_type == 1:
                times = round(random.randint(2, 3) / max(0.25, RoomDodge))
                return do_prompt_dodges(times, combo_dodges, 2)
            elif attack_type == 2:
                times = round(random.randint(7, 10) / max(0.25, RoomDodge))
                print("The Slime God starts to grow...")
                input("press enter super fast to dodge!")
                start = time.monotonic()
                for i in range(times):
                    input("Hit enter!")
                    elapsed = time.monotonic() - start
                    if elapsed > 3.0:
                        print("You failed to dodge... It dealt 3 damage.")
                        take_damage(3)
                        print("you have " + str(new_life) + " life left.")
                        return new_life
                print("You dodged the attack!")
                dodge_success()
                return new_life
        elif CurrentEnemiesHealth[0] > 50:
            attack_type = random.randint(0, 3)
            if attack_type == 0:
                times = round(random.randint(7, 9) / max(0.25, RoomDodge))
                return do_simple_dodges(times, 2.5)
            elif attack_type == 1:
                times = round(random.randint(4, 5) / max(0.25, RoomDodge))
                return do_prompt_dodges(times, combo_dodges, 2.5)
            elif attack_type == 2:
                times = round(random.randint(12, 15) / max(0.25, RoomDodge))
                input("The Slime God starts to grow...")
                input("press enter super fast to dodge!")
                start = time.monotonic()
                for i in range(times):
                    input("Hit enter!")
                    elapsed = time.monotonic() - start
                    if elapsed > 3.0:
                        print("You failed to dodge... It dealt 3.5 damage.")
                        take_damage(3.5)
                        print("you have " + str(new_life) + " life left.")
                        return new_life
                print("You dodged the attack!")
                dodge_success()
                return new_life
            elif attack_type == 3:
                input("The Slime God is bouncing around rapidly!")
                alphebet_choice = random.choice(alphebet)
                start = time.monotonic()
                userinput = input("Quick, type " + alphebet_choice + " to dodge!")
                elapsed = time.monotonic() - start
                if userinput != alphebet_choice or elapsed > 3.0:
                    print("You failed to dodge... It dealt 3.5 damage.")
                    take_damage(3.5)
                    print("you have " + str(new_life) + " life left.")
                    return new_life
                else:
                    print("You dodged the attack!")
                    dodge_success()
                    return new_life
        elif CurrentEnemiesHealth[0] <= 50:
            attack_type = random.randint(0, 4)
            if attack_type == 0:
                times = round(random.randint(9, 11) / max(0.25, RoomDodge))
                return do_simple_dodges(times, 3)
            elif attack_type == 1:
                times = round(random.randint(6, 7) / max(0.25, RoomDodge))
                return do_prompt_dodges(times, combo_dodges, 3)
            elif attack_type == 2:
                times = round(random.randint(17, 20) / max(0.25, RoomDodge))
                input("The Slime God starts to grow...")
                input("press enter super fast to dodge!")
                start = time.monotonic()
                for i in range(times):
                    input("Hit enter!")
                    elapsed = time.monotonic() - start
                    if elapsed > 3.0:
                        print("You failed to dodge... It dealt 4 damage.")
                        take_damage(4)
                        print("you have " + str(new_life) + " life left.")
                        return new_life
                print("You dodged the attack!")
                dodge_success()
                return new_life
            elif attack_type == 3:
                input("The Slime God is bouncing around rapidly!")
                alphebet_choice = random.choice(alphebet)
                start = time.monotonic()
                userinput = input("Quick, type " + alphebet_choice + " to dodge!")
                elapsed = time.monotonic() - start
                if userinput != alphebet_choice or elapsed > 2.5:
                    print("You failed to dodge... It dealt 4 damage.")
                    take_damage(4)
                    print("you have " + str(new_life) + " life left.")
                    return new_life
                else:
                    print("You dodged the attack!")
                    dodge_success()
                    return new_life
            elif attack_type == 4:
                input("The Slime God is returning the slimes to its body...")
                count = len(set(CurrentEnemies) & set(SLIME_ENEMIES))
                if count > 0:
                    print("you have 5 seconds to dodge!")
                    start = time.monotonic()
                    for i in range(count):
                        times = round(random.randint(1, 4) / max(0.25, RoomDodge))
                        for i in range(times):
                            userinput = input("Type 'dodge' to dodge!")
                            elapsed = time.monotonic() - start
                            if userinput != "dodge" or elapsed > 3.0:
                                print("You failed to dodge... It dealt 4 damage.")
                                take_damage(4)
                                print("you have " + str(new_life) + " life left.")
                                return new_life
                        print("You dodged the attack!")
                        dodge_success()
                        return new_life
                else:
                    print("But there were no slimes to return!")
                    return new_life

    WormSpawns1 = ["Red Flame I", "Green Flame I", "Worm Gaurd"]
    WormSpawns2 = ["Red Flame II", "Green Flame II", "Purple Flame II", "Yellow Flame II", "Worm Gaurd", "Worm Gaurd"]
    WormSpawns3 = ["Red Flame III", "Green Flame III", "Purple Flame III", "Yellow Flame III", "Blue Flame III", "Orange Flame III", "Rainbow Flame", "Worm Gaurd", "Worm Gaurd", "Worm Gaurd",]

    if enemy_name == "Dungeon Worm":
        if CurrentEnemiesHealth[0] > 200:
            print("The dungeon worm summons a minion!")
            CurrentEnemies.append(random.choice(WormSpawns1))
            CurrentEnemiesHealth.append(random.randint(10, 13))
            StunnedEnemies.append(0)
            print("a " + enemy_displays[enemy_bank.index(str(CurrentEnemies[len(CurrentEnemies) - 1]))] + " has spawned!")
            print("it has " + str(CurrentEnemiesHealth[-1]) + " health.")
            return new_life
        elif CurrentEnemiesHealth[0] > 100:
            print("The dungeon worm summons a minion!")
            CurrentEnemies.append(random.choice(WormSpawns2))
            CurrentEnemiesHealth.append(random.randint(10, 13))
            StunnedEnemies.append(0)
            print("a " + enemy_displays[enemy_bank.index(str(CurrentEnemies[len(CurrentEnemies) - 1]))] + " has spawned!")
            print("it has " + str(CurrentEnemiesHealth[-1]) + " health.")
            return new_life
        elif CurrentEnemiesHealth[0] > 100:
            print("The dungeon worm summons a minion!")
            CurrentEnemies.append(random.choice(WormSpawns3))
            CurrentEnemiesHealth.append(random.randint(10, 13))
            StunnedEnemies.append(0)
            print("a " + enemy_displays[enemy_bank.index(str(CurrentEnemies[len(CurrentEnemies) - 1]))] + " has spawned!")
            print("it has " + str(CurrentEnemiesHealth[-1]) + " health.")
            return new_life
        elif CurrentEnemiesHealth[0] <= 25:
            print("The dungeon worm summons a minion!")
            CurrentEnemies.append("Rainbow Flame")
            CurrentEnemiesHealth.append(random.randint(10, 13))
            StunnedEnemies.append(0)
            print("a " + enemy_displays[enemy_bank.index(str(CurrentEnemies[len(CurrentEnemies) - 1]))] + " has spawned!")
            print("it has " + str(CurrentEnemiesHealth[-1]) + " health.")
            return new_life
           

    print("But someone forgot to code the " + enemy_name + "... it failed to attack.")
    return new_life

def apply_aoe_and_cleanup(enemies: list[str], healths: list[int], stunned: list[int]) -> None:
    global KillScore, CurrentEnemiesHealth, LevelBeat
    for i in range(len(enemies) - 1, -1, -1):
        if healths[i] <= 0:
            slain = enemies[i]
            KillScore += 1
            if slain in SLIME_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " turns to a puddle!")
            if slain in SMOKE_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " disappears in a puff of smoke!")
            if slain in PHASE_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " phases out of reality!")
            if slain in AWKWARD_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " is still just... there.")
            if slain in REVIVAL_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " is no longer reanimated!")
            if slain in MUSICAL_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " shuts up!")
            if slain in EXPLOSIVE_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " makes an explosive exit!")
            if slain in WIND_ENEMIES:
                print("the " + enemy_displays[enemy_bank.index(slain)] + " blows out of battle!")
            print("You beat the " + enemy_displays[enemy_bank.index(slain)] + "!")
            if slain in worm_summons:
                print("The " + slain + " blows up!")
                print(RED+"It did 25 damage to the Dungeon Worm."+RESET)
                CurrentEnemiesHealth[0] -= 25
            if slain in bosses:
                LevelBeat = True
            else:
                grant_reward(slain)
            AchivementsFile = open('Achivements.json')
            data = json.load(AchivementsFile)
            for achievement in data["achivements"]:
                if slain == "Slime God":
                    if achievement["goaltype"] == "slimeGodKill":
                        achievement["progress"] += 1
                if slain == "Dungeon Worm":
                    if achievement["goaltype"] == "dungeonWormKill":
                        achievement["progress"] += 1
                if slain == "Astral Reflection":
                    if achievement["goaltype"] == "astralReflectionKill":
                        achievement["progress"] += 1
                if slain == "Dungeonemus Maximus":
                    if achievement["goaltype"] == "dmKill":
                        achievement["progress"] += 1
                if slain == "The Legend of Worm-Cat":
                    if achievement["goaltype"] == "wormCatBeat":
                        achievement["progress"] += 1
            enemies.pop(i)
            healths.pop(i)
            stunned.pop(i)

# -------------------------
# NPCs / upgrades
# -------------------------
def PermUpgrade():
    global MaxLife, MetaDamage, MetaDefence, MetaDodge, YourLife
    while True:
        userinput = input("Choose an upgrade! ").strip()
        if userinput == "1":
            MaxLife += 0.1
            YourLife += 0.1
            print("Your max life increased!")
            return
        if userinput == "2":
            MetaDamage += 0.1
            print("Your damage increased!")
            return
        if userinput == "3":
            MetaDefence += 0.1
            print("Your defence increased!")
            return
        if userinput == "4":
            MetaDodge += 0.1
            print("Your dodge power increased!")
            return
        print("Please enter a valid response.")

def get_upgrade_cost(item: str):
    if item not in upgrades:
        return None
    if item in NPCItems1:
        return 5
    if item in NPCItems2:
        return 10
    if item in NPCItems3:
        return 20
    if item in NPCItems4:
        return 30
    if item in NPCItems5:
        return 50
    return None

def Trader(Mode, Trades):
    global inventory, NPCScore, trades, Gold
    current_trades = {}

    trade_keys = list(trades.keys())
    take = min(len(trade_keys), random.randrange(7, 12))
    for k in random.sample(trade_keys, take):
        current_trades[k] = trades[k]

    if Mode == 0:
        return current_trades
   
    current_trades = Trades

    print("\nAvailable trades:")
    for i, (give, get) in enumerate(current_trades.items()):
        print(f"{i + 1}: {give} for {get}")
    print("")

    while True:
        if inventory:
            tier_order = reward_bank
            order_lookup = {item: i for i, item in enumerate(tier_order)}
            inventory.sort(key=lambda item: order_lookup.get(item, 9999))
            inventory[:] = [x for x in inventory if x != "Nothing"]
            print("inventory: " + ", ".join(inventory))
        else:
            print("you have nothing in your inventory.")

        print("you have " + str(Gold) + " gold.\n")
        userinput = input("Choose a trade by number, type 0 to leave, or type 'cheddar' for a chest: ").strip().lower()
        print()

        if userinput == "0":
            print("You leave the trader.")
            return

        if not inventory:
            print("You have no items to trade.")
            return

        if userinput.isdigit():
            trade_index = int(userinput) - 1
            items_list = list(current_trades.items())
            if 0 <= trade_index < len(items_list):
                give, get = items_list[trade_index]
                if give in inventory:
                    inventory.remove(give)
                    inventory.append(get)
                    NPCScore += 10
                    print(f"You traded {give} for {get}!")
                else:
                    print(f"You don't have {give} to trade.")
            else:
                print("Invalid trade number.")
            continue

        if userinput == "cheddar":
            if "Cheddar" in inventory:
                print("You traded a Cheddar for a chest!")
                inventory.remove("Cheddar")
                special_trade = random.choice(Chests2)
                print(f"You got a special trade: {special_trade}!")
                Chest(1, special_trade)
                NPCScore += 10
                continue
            if "Big Cheddar" in inventory:
                print("You traded a Big Cheddar for a chest!")
                inventory.remove("Big Cheddar")
                special_trade = random.choice(Chests4)
                print(f"You got a special trade: {special_trade}!")
                Chest(3, special_trade)
                NPCScore += 10
                continue
            if "Golden Cheddar" in inventory:
                print("You traded a Golden Cheddar for a chest!")
                inventory.remove("Golden Cheddar")
                special_trade = random.choice(Chests6)
                print(f"You got a special trade: {special_trade}!")
                Chest(5, special_trade)
                NPCScore += 10
                continue
            print("You don't have any cheddar!!")
            continue

        print("Please enter a valid response.")

def Merchant(Mode, Options):
    global Gold, NPCScore, inventory, room, TotalGold

    ItemPool: dict[str, int] = {}

    if room < 10:
        pools = [(NPCItems1, (1, 2)), (NPCItems2, (2, 6))]
        ItemPool[random.choice(Chests2)] = random.randint(30, 50)
    elif room < 25:
        pools = [(NPCItems2, (2, 6)), (NPCItems3, (4, 12))]
        ItemPool[random.choice(Chests3)] = random.randint(50, 75)
    elif room < 40:
        pools = [(NPCItems3, (4, 12)), (NPCItems4, (6, 15))]
        ItemPool[random.choice(Chests4)] = random.randint(75, 150)
    elif room < 75:
        pools = [(NPCItems4, (6, 15)), (NPCItems5, (15, 50))]
        ItemPool[random.choice(Chests5)] = random.randint(150, 300)
    else:
        pools = [(NPCItems5, (15, 50)), (NPCItems6, (30, 100))]
        ItemPool[random.choice(Chests6)] = random.randint(300, 500)

    for item_list, (lo, hi) in pools:
        for _ in range(random.randrange(4, 7)):
            item = random.choice(item_list)
            ItemPool[item] = random.randint(lo, hi)

    if Mode == 0:
        return ItemPool
   
    ItemPool = Options

    while True:
        print("Available items for sale:")
        items_list = list(ItemPool.items())
        for i, (item, price) in enumerate(items_list):
            print(f"{i + 1}: {item} - {price} gold")
        print()

        if inventory:
            tier_order = reward_bank
            order_lookup = {item: i for i, item in enumerate(tier_order)}
            inventory.sort(key=lambda item: order_lookup.get(item, 9999))
            inventory[:] = [x for x in inventory if x != "Nothing"]
            print("inventory: " + ", ".join(inventory))
        else:
            print("you have nothing in your inventory.")

        print("you have " + str(Gold) + " gold.\n")
        userinput = input("Choose a buy number, type 0 to leave, or type 'sell' to sell cheddar: ").strip().lower()
        print()

        if userinput == "0":
            print("You leave the merchant.")
            return

        if userinput.isdigit():
            idx = int(userinput) - 1
            if 0 <= idx < len(items_list):
                item, price = items_list[idx]
                if Gold >= price:
                    Gold -= price
                    if item in loot_bank:
                        inventory.append(item)
                    NPCScore += price
                    print(f"You bought {item} for {price} gold.")
                    if item in Chests2:
                        Chest(1, item)
                    if item in Chests3:
                        Chest(2, item)
                    if item in Chests4:
                        Chest(3, item)
                    if item in Chests5:
                        Chest(4, item)
                    if item in Chests6:
                        Chest(5, item)
                else:
                    print("You don't have enough gold.")
            else:
                print("Invalid item number.")
            continue

        if userinput == "sell":
            if "Cheddar" in inventory:
                print("You sold your cheddar!")
                inventory.remove("Cheddar")
                Gold += 15
                TotalGold += 15
                NPCScore += 15
                continue
            if "Big Cheddar" in inventory:
                print("You sold your big cheddar!")
                inventory.remove("Big Cheddar")
                Gold += 35
                TotalGold += 35
                NPCScore += 35
                continue
            if "Golden Cheddar" in inventory:
                print("You sold your golden cheddar!")
                inventory.remove("Golden Cheddar")
                Gold += 65
                TotalGold += 65
                NPCScore += 65
                continue
            print("You don't have any cheddar!!")
            continue

        print("Please enter a valid response.")

def Wizard(Mode, Options):
    global inventory, Gold, NPCScore, TotalGold

    if not inventory:
        print("You have no items to upgrade.")
        return
    if Gold < 1:
        print("You don't have any gold to pay for upgrades.")
        return

    inventory[:] = [x for x in inventory if x != "Nothing"]
    tier_order = reward_bank
    order_lookup = {item: i for i, item in enumerate(tier_order)}
    inventory.sort(key=lambda item: order_lookup.get(item, 9999))

    while True:
        print("Inventory:")
        if not inventory:
            print("(empty)")
        else:
            for item in inventory:
                cost = get_upgrade_cost(item)
                if cost is None:
                    print(item)
                else:
                    print(f"{item} ({cost} Upgrade cost)")
        print(f"You have {Gold} Gold.\n")

        userinput = input("Type the number of the item to upgrade, or 0 to leave: ").strip()
        print()

        if userinput.lower() == "0":
            print("You leave the wizard.")
            return

        if userinput.lower() == "sell":
            if "Cheddar" in inventory:
                print("You sold your cheddar!")
                inventory.remove("Cheddar")
                Gold += 15
                TotalGold += 15
                NPCScore += 15
            elif "Big Cheddar" in inventory:
                print("You sold your big cheddar!")
                inventory.remove("Big Cheddar")
                Gold += 35
                TotalGold += 35
                NPCScore += 35
            elif "Golden Cheddar" in inventory:
                print("You sold your golden cheddar!")
                inventory.remove("Golden Cheddar")
                Gold += 65
                TotalGold += 65
                NPCScore += 65
            else:
                print("You don't have any cheddar!!")
            print()
            continue

        if not 1 <= int(userinput) < len(inventory):
            print("Please enter a valid item number from your inventory.\n")
            continue

        if userinput in NPCBlacklist:
            print("The wizard is horrified by your offer, and refuses to upgrade it.")
            continue
       
        if userinput not in upgrades and userinput not in CHEESE_ITEMS:
            print("That item cannot be upgraded.\n")
            continue

        cost = get_upgrade_cost(userinput)
        if cost is None:
            print("This item is already at the highest upgrade level (or has no upgrade price).\n")
            continue

        upgraded = upgrades[userinput]

        if Gold < cost:
            print(f"You don't have enough gold to upgrade this item. (Need {cost}, have {Gold})\n")
            continue

        inventory.remove(userinput)
        if item in CHEESE_ITEMS:
            if item == "Cheddar":
                print("You upgraded the Cheddar to a Cheddar Chest!")
                Chest(1, "Cheddar Chest")
            if item == "Big Cheddar":
                print("You upgraded the Big Cheddar to a Big Cheddar Chest!")
                Chest(3, "Big Cheddar Chest")
            if item == "Golden Cheddar":
                print("You upgraded the Big Cheddar to a Golden Cheddar chest!")
                Chest(5, "Golden Cheddar Chest")
        else:
            inventory.append(upgraded)
            Gold -= cost
            NPCScore += cost

            order_lookup = {item: i for i, item in enumerate(reward_bank)}
            inventory.sort(key=lambda item: order_lookup.get(item, 9999))

            print(f"You upgraded {userinput} to {upgraded} for {cost} gold!\n")

def Medic(Mode, Options):
    global Gold, YourLife, MaxLife, NPCScore
    if YourLife >= MaxLife:
        print("You're already at full health.")
        print("You leave the medic.")
        return
    if Gold < math.ceil(10 + room * 0.5):
        print("You don't have enough gold to pay the medic.")
        print("You leave the medic.")
        return
    print("A medic offers to heal you to full health for " + str(math.ceil(10 + room * 0.5)) + " gold per health point.")
    while True:
        print(f"Life: {YourLife}/{MaxLife} | Gold: {Gold}")
        userinput = input("Press enter to heal or 0 to leave: ").strip().lower()
        if userinput == "0":
            print("You leave the medic.")
            return
        if userinput == "":
            needed = max(0, math.ceil(MaxLife - YourLife))
            cost = needed * 10
            if needed == 0:
                print("You're already full.")
                continue
            if Gold < cost:
                print(f"Not enough gold. You need {cost}.")
                continue
            Gold -= cost
            YourLife = MaxLife
            NPCScore += 10 * needed
            print(f"You healed to full for {cost} gold.")
            continue
        print("Please enter a valid response.")

def Gambler(Mode, Stats):
    global Gold, NPCScore, TotalGold

    if Mode == 0:
        Rewarded = 0
        GoldEarned = 0
        return {Rewarded, GoldEarned}

    Dice1 = 0
    Dice2 = 0
    Roll1 = 0
    Roll2 = 0
    Print = ""
    color = ""
    MidWage = 5
    Turns = 0
    Rewarded = Stats[0]
    GoldEaned = Stats[1]

    if Gold < 5:
        print("You don't have enough money to gamble.")
        print("You leave the gambler.")
        return

    print("The gambler offers to play a dice game with you for gold.")
    print("Here are the rules:")
    input("Roll a " + RED + "2, 3, 8, or 12 " + RESET + " to lose twice your bet.")
    input("Roll a " + YELLOW + " 4, 5, or 6 " + RESET + " to lose your bet.")
    input("Roll a " + GREEN + " 9, 10 or 11 " + RESET + " to earn your bet.")
    input("Roll a " + BOLDGREEN + " 7 " + RESET + " to earn twice your bet.")

    print("You have " + str(Gold) + " gold.")

    while True:
        bet = input("How much do you want to bet? The midimum wage is " + str(MidWage) + ". You earned " + str(GoldEarned) + " gold. Type 0 to leave. ")
        if bet == "0":
            print("You leave the gambler.")
            return
        if Gold < MidWage:
            print("You don't have enough money to gamble.")
            print("You leave the gambler.")
            return
        if bet.isdigit():
            if int(bet) >= MidWage and int(bet) <= Gold:
                Turns += 1
                NPCScore += MidWage / 5

                Roll1 = random.randint(15, 30)
                Roll2 = random.randint(15, 30)
                print("Rolling!\n")

                for i in range(max(Roll1, Roll2)):
                    if Roll1 >= i:
                        Dice1 = random.randint(1, 6)
                    if Roll2 >= i:
                        Dice2 = random.randint(1, 6)
                   
                    if Dice1 == 1:
                        Print = "⚀"
                    if Dice1 == 2:
                        Print = "⚁"
                    if Dice1 == 3:
                        Print = "⚂"
                    if Dice1 == 4:
                        Print = "⚃"
                    if Dice1 == 5:
                        Print = "⚄"
                    if Dice1 == 6:
                        Print = "⚅"
                   
                    if Dice2 == 1:
                        Print += "⚀"
                    if Dice2 == 2:
                        Print += "⚁"
                    if Dice2 == 3:
                        Print += "⚂"
                    if Dice2 == 4:
                        Print += "⚃"
                    if Dice2 == 5:
                        Print += "⚄"
                    if Dice2 == 6:
                        Print += "⚅"
                   
                    print(Print, end="\r")
                    time.sleep(0.1)
                time.sleep(1)
               
                if Dice1 + Dice2 in [2, 3, 8, 12]:
                    color = RED
                if Dice1 + Dice2 in [4, 5, 6]:
                    color = YELLOW
                if Dice1 + Dice2 in [9, 10, 11]:
                    color = GREEN
                if Dice1 + Dice2 == 7:
                    color = BOLDGREEN
               
                print(color + Print + RESET)

                time.sleep(2)

                if Dice1 + Dice2 in [2, 3, 8, 12]:
                    Gold -= int(bet) * 2
                    GoldEarned -= int(bet) * 2
                    print("You lost " + str(int(bet) * 2) + " gold.")
                    print("You have " + str(Gold) + " left.")
                if Dice1 + Dice2 in [4, 5, 6]:
                    Gold -= int(bet)
                    GoldEarned -= int(bet)
                    print("You lost " + bet + " gold.")
                    print("You have " + str(Gold) + " left.")
                if Dice1 + Dice2 in [9, 10, 11]:
                    Gold += int(bet)
                    TotalGold += int(bet)
                    GoldEarned += int(bet)
                    print("You got " + bet + " gold!")
                    print("You have " + str(Gold) + " in total.")
                if Dice1 + Dice2 == 7:
                    Gold += int(bet) * 2
                    TotalGold += int(bet) * 2
                    GoldEarned += int(bet) * 2
                    print("You got " + str(int(bet) * 2) + " gold!")
                    print("You have " + str(Gold) + " in total.")
               
                print(str(Rewarded))
               
                if Rewarded == 0 and GoldEarned >= 150:
                    print("The gambler gives you a prize for earning 150 gold!")
                    print("You got 100 gold!")
                    Gold += 100
                    TotalGold += 100
                    Rewarded = 1
               
                if Rewarded == 1 and GoldEarned >= 300:
                    print("The gambler gives you a prize for earning 300 gold!")
                    if room < 10:
                        Item = random.choice(NPCItems2)
                    elif room < 25:
                        Item = random.choice(NPCItems3)
                    elif room < 40:
                        Item = random.choice(NPCItems4)
                    elif room < 75:
                        Item = random.choice(NPCItems5)
                    else:
                        Item = random.choice(NPCItems6)
                    print("You got a " + Item + "!")
                    Rewarded = 2

                if Turns % 5 == 0:
                    print("The midimum wage increases!")
                    MidWage += 5

# -------------------------
# Game loop helpers
# -------------------------
def print_inventory():
    if inventory:
        for idx, item in enumerate(inventory, start=1):
            print(f"{idx}: {item_displays[reward_bank.index(item)]}")
    else:
        print("you have nothing in your inventory.")

def reset_room_multipliers():
    global RoomDodge, RoomDamage, RoomDefence, MetaDodge, MetaDamage, MetaDefence, TurnsTaken
    RoomDodge = MetaDodge
    RoomDamage = MetaDamage
    RoomDefence = MetaDefence
    TurnsTaken = 0

def do_death_messages(current_room, enemy):
    color_enemy = enemy_displays[enemy_bank.index(enemy)] + RED

    options = death_messages1 + death_messages2 + death_messages3 + death_messages4
   
    if room > 50:
        options += death_messages5 + death_messages6 + death_messages7 + death_messages8

    if enemy in elite_enemies + bosses:
        options = death_messages9
   
    if enemy in DARK_ENEMIES:
        options = death_messages10
    
    if enemy == "Washing Machine Monster":
        options = [" was thrown into a washing machine by "]

    message = random.choice(options)
    messageprint = ""
    if message in death_messages1 + death_messages5 + [" was thrown into a washing machine by "]:
        messageprint = (RED + Name + message + "by " + color_enemy + "." + RESET)
    elif message in death_messages2 + death_messages6:
        messageprint = (RED + color_enemy + message + Name + "." + RESET)
    elif message in death_messages3 + death_messages7:
        messageprint = (RED + Name + message + "." + RESET)
    elif message in death_messages4 + death_messages8:
        messageprint = (RED + message + Name + "." + RESET)
    elif message in death_messages9 + death_messages10:
        messageprint = (RED + Name + message + color_enemy + "." + RESET)
    print(messageprint)
    MessageList.append([messageprint, room, (WinBonus + LifeLeftScore + ItemUseScore + BossScore + DodgeScore + KillScore + NPCScore + TotalGold)])
    print()
    try:
        with open('MessageList.json', 'r') as file:
            ExistingData = json.load(file)
    except FileNotFoundError:
        ExistingData = []
    with open('MessageList.json', 'w') as file:
        json.dump(ExistingData + MessageList, file, indent=2)

def do_win_messages():
    options = win_messages1 + win_messages2
   
    if YourLife >= 5.0 and Saves == 2 and HealUsed == False:
        options = win_messages3
   
    message = random.choice(options)
    if message in win_messages1:
        messageprint = (GREEN + Name + message + "." + RESET)
    if message in win_messages2:
        messageprint = (GREEN + message + Name + "." + RESET)
    if message in win_messages3:
        messageprint = (BOLDGREEN + Name + message + "." + RESET)
    print(messageprint)
    MessageList.append([messageprint, room, (WinBonus + LifeLeftScore + ItemUseScore + BossScore + DodgeScore + KillScore + NPCScore + TotalGold)])
    print()
    try:
        with open('MessageList.json', 'r') as file:
            ExistingData = json.load(file)
    except FileNotFoundError:
        ExistingData = []
    with open('MessageList.json', 'w') as file:
        json.dump(ExistingData + MessageList, file, indent=2)

# Mimics?
def Chest(Level, Name):
    global inventory

    loot = ""
    color = ""
    if Level == 0:
        color = BOLDWHITE
        loot = random.choice(Loot1)
    if Level == 1:
        color = BOLDGREEN
        loot = random.choice(Loot2)
    if Level == 2:
        color = BOLDBLUE
        loot = random.choice(Loot3)
    if Level == 3:
        color = BOLDPURPLE
        loot = random.choice(Loot4)
    if Level == 4:
        color = BOLDYELLOW
        loot = random.choice(Loot5)
    if Level == 5:
        color = BOLDRED
        loot = random.choice(Loot6)

    print("It's a " + color + Name + RESET + "!")
    input("Press enter to open!")
    for i in range(random.randint(3, 6)):
        input("...")
        time.sleep(0.1)
   
    print("You opened the chest!")
    input("Inside was...")
    print("A " + loot_displays[loot_bank.index(loot)] + "!")
    if loot in Scarfs:
        if len(ScarfInventory) < MaxScarfInventory:
                ScarfInventory.append(loot)
                print("It was added to your scarfs.")
        else:
            while True:
                for idx, item in enumerate(ScarfInventory, start=1):
                    print(f"{idx}: {loot_displays[loot_bank.index(item)]}")
                print("Your can't carry any more scarves!")
                userinput = ("Choose something to replace, or 0 not to replace it with anything.")
                if userinput == 0:
                    print("You didn't take the scarf.")
                    return
                if userinput.isdigit():
                    if int(userinput) < 31 and int(userinput) > 0:
                        inventory.append(loot)
                        print(f"You dropped the {loot_displays[loot_bank.index(ScarfInventory[int(userinput) + 1])]} for the {loot}.")
                        ScarfInventory.remove(ScarfInventory[int(userinput) + 1])
                        return
                    else:
                        print("please enter a valid response.")
                else:
                    print("please enter a valid response.")
    elif loot in Rings:
        if len(RingInventory) < MaxRingInventory:
                RingInventory.append(loot)
                print("It was added to your rings.")
        else:
            while True:
                for idx, item in enumerate(RingInventory, start=1):
                    print(f"{idx}: {loot_displays[loot_bank.index(RingInventory[int(userinput) + 1])]}")
                print("Your can't carry any more rings!")
                userinput = ("Choose something to replace, or 0 not to replace it with anything.")
                if userinput == 0:
                    print("You didn't take the ring.")
                    return
                if userinput.isdigit():
                    if int(userinput) < 31 and int(userinput) > 0:
                        inventory.append(loot)
                        print(f"You dropped the {loot_displays[loot_bank.index(RingInventory[int(userinput) + 1])]} for the {loot}.")
                        RingInventory.remove(RingInventory[int(userinput) + 1])
                        return
                    else:
                        print("please enter a valid response.")
                else:
                    print("please enter a valid response.")
    elif loot in Bottles:
        if len(BottleInventory) < MaxBottleInventory:
                BottleInventory.append(loot)
                print("It was added to your bottles.")
        else:
            while True:
                for idx, item in enumerate(RingInventory, start=1):
                    print(f"{idx}: {loot_displays[loot_bank.index(BottleInventory[int(userinput) + 1])]}")
                print("Your can't carry any more bottles!")
                userinput = ("Choose something to replace, or 0 not to replace it with anything.")
                if userinput == 0:
                    print("You didn't take the bottle.")
                    return
                if userinput.isdigit():
                    if int(userinput) < 31 and int(userinput) > 0:
                        inventory.append(loot)
                        print(f"You dropped the {loot_displays[loot_bank.index(BottleInventory[int(userinput) + 1])]} for the {loot}.")
                        BottleInventory.remove(BottleInventory[int(userinput) + 1])
                        return
                    else:
                        print("please enter a valid response.")
                else:
                    print("please enter a valid response.")

def StarterCheatCodes():
    global YourLife, MaxLife, Gold, inventory, MetaDamage, MetaDefence, MetaDodge, Saves, Hardmode
    while True:
        input_str = input()
        if input_str == "LOLBetaaing":
            YourLife = 999
            MaxLife = 999
            print("God mode activated!")
        elif input_str == "imunstuck":
            MetaDamage += 10
            MetaDefence += 10
            MetaDodge += 10
            MaxLife += 10
            YourLife += 10
            print("You feel much more powerful!")
        elif input_str == "saveme":
            Saves += 5
            print("5 extra saves added!")
        elif input_str == "tooeasy":
            Hardmode = True
            print("good luck, gonna need it")
        elif input_str == "IStealCheeseCantCatchMe":
            inventory.append("Cheddar")
            inventory.append("Big Cheddar")
            inventory.append("Golden Cheddar")
            print("You stole some cheese! It has been added to your inventory.")
        elif input_str == "KnowlegeBook":
            print("GET GOOD BOZO")
            print("lolgloleloltloltlolrlololollloleloldlolblolololzlolololhlolalolhlolalol")
        elif input_str == "gettrolledbozohaha":
            input("You open the Real Knowledge Book™ and gain some REAL knowledge!")
            input("- The game was made in Python over quite some time by a single person and with the help of The Coder School!")
            input("- You know that you can just copy paste concok lectures, right?")
            input("- The cheat code 'IStealCheeseCantCatchMe' is a reference, can you guess to what?")
            input("- Some people complain that no one knows what the items do, but that's kind of the point... it's like a real roguelike where you have to experiment and learn what things do on your own. Where's the fun in just being told everything?")
            input("- Nevermind lol the cheat code to find out the items in your inventory is actually \"Y'all Suckers\"")
            input("- If you're reading this, you should know that that the final boss is actually gaurded by super tough enemies.")
            input("- You should also know that there is actually a secret post-win area with some fun stuff to find if you can get there :)")
            input("- The game is not actually supposed to be that hard, it's just that the dodge prompts can be pretty unforgiving if you mess up even once. If you're struggling, try to focus on dodging and don't worry too much about strategy.")
            input("- That being said, strategy can still be helpful! Some items are really good and can make the game much easier if you know how to use them. And of course, learning enemy patterns and how to dodge effectively is key to winning.")
            input("- There are more items, enemies, and even mechanics that aren't mentioned in the Real Knowledge Book™. Part of the fun is discovering them on your own!")
            input("- But, if you are just too curious (or impatient), you can type \"PlayerManual\" for a detailed player manual.")
            input("- Thanks for reading! I hope you enjoy the game :)")
        elif input_str == "SuperSecretCheatCode":
            print("Here are some post-win cheat codes to mess around with:")
            print("- 'LOLBetaTesting' for god mode (999 life)")
            print("- 'imunstuck' for a big boost to all stats")
            print("- 'saveme' for 5 extra saves")
            print("- 'tooeasy' to make the game \"easier\"")
        elif input_str == "NoobManual":
            input("This is the beginner's manual! It contains some tips and information about the game. Enjoy!")
            input("- The game is a 100 room roguelike where you fight enemies and get upgrades to try to make it to the end.")
            input("- Each room has 1-5 enemies with different attack patterns that you have to learn to dodge. If you fail to dodge an attack, you take damage.")
            input("- After each room, you get to choose a permanent upgrade to increase your stats. Every 10 rooms, you also get to visit a shopkeeper for more upgrades and items.")
            input("- Your goal is to make it through all 100 rooms. If you die before that, your score will be based on how far you got and how well you did.")
            input("- There are many different items and upgrades that can help you on your journey. Some are straightforward while others are more mysterious and require experimentation to understand.")
            input("- The game is meant to be challenging but fair. Learning enemy patterns and how to effectively use your upgrades is key to success.")
            input("- Don't be afraid to experiment and try different strategies! Part of the fun is discovering what works best for you.")
            print("Have fun!!")
        else:
            break
    return

def MidgameCheatInput():
    global YourLife, MaxLife, Gold, inventory, MetaDamage, MetaDefence, MetaDodge, Saves, Hardmode
    global descriptions
    global room, BossLevel
    global CurrentEnemies, CurrentEnemiesHealth, StunnedEnemies
    global KillScore, TotalGold, DodgeScore, BossScore, LifeLeftScore, NPCScore, ItemUseScore, Score

    while True:
        input_str = input()
        if input_str == "Y'all Suckers":
            print("Your inventory contains:")
            if inventory:
                for item in inventory:
                    if item in reward_bank:
                        desc = descriptions[reward_bank.index(item)]
                    else:
                        desc = "No description available."
                    print("- " + desc)
            else:
                print("- Nothing")

        elif input_str == "NoobManual":
            input("This is the beginner's manual! It contains some tips and information about the game. Enjoy!")
            input("- The game is a 100 room roguelike where you fight enemies and get upgrades to try to make it to the end.")
            input("- Each room has 1-5 enemies with different attack patterns that you have to learn to dodge. If you fail to dodge an attack, you take damage.")
            input("- As well as that, the dungeon will try to hurry you up by putting more enemies in your room, so don't take too long!")
            input("- After each room, you get to choose a permanent upgrade to increase your stats. Every 10 rooms, you also get to visit a shopkeeper for more upgrades and items.")
            input("- Your goal is to make it through all 100 rooms. If you die before that, your score will be based on how far you got and how well you did.")
            input("- There are many different items and upgrades that can help you on your journey. Some are straightforward while others are more mysterious and require experimentation to understand.")
            input("- The game is meant to be challenging but fair. Learning enemy patterns and how to effectively use your upgrades is key to success.")
            input("- Don't be afraid to experiment and try different strategies! Part of the fun is discovering what works best for you.")
            print("Have fun!!")

        elif input_str == "imunstuck":
            MetaDamage += 10
            MetaDefence += 10
            MetaDodge += 10
            print("You feel much more powerful!")

        elif input_str == "saveme":
            Saves += 5
            print("5 extra saves added!")

        elif input_str == "IStealCheeseCantCatchMe":
            inventory.append("Cheddar")
            inventory.append("Big Cheddar")
            inventory.append("Golden Cheddar")
            print("You stole some cheese! It has been added to your inventory.")

        elif input_str == "RainbowRun":
            inventory.append("Rainbow Run")
            print("You got the rare Rainbow Run item! It has been added to your inventory.")

        elif input_str == "moonlord":
            inventory.extend(["Moon Blob"] * 5)
            print("You got 5 Moon Blobs! They have been added to your inventory.")

        elif input_str == "RevivalOfOrgin":
            print("Cats are invading!")
            reset_room_multipliers()
            get_enemy_options(room)
            CurrentEnemies, CurrentEnemiesHealth = spawn_enemy(room, 1)
            StunnedEnemies = [0 for _ in range(len(CurrentEnemies))]

        elif input_str == "MOREOFTHEM??":
            print("Concocs have spawned!")
            reset_room_multipliers()
            get_enemy_options(room)
            CurrentEnemies, CurrentEnemiesHealth = spawn_enemy(room, 2)
            StunnedEnemies = [0 for _ in range(len(CurrentEnemies))]

        elif input_str == "KnowlegeBook":
            input("You open the Real Knowledge Book™ and gain some REAL knowledge!")
            input("- Chapter 1 of 1: The Real Knowledge Book™\n")
            input("- You know that you can just copy paste concok lectures, right?")
            input("- The cheat code 'IStealCheeseCantCatchMe' is a reference, can you guess to what?")
            input("- Some people complain that no one knows what the items do, but that's kind of the point... it's like a real roguelike where you have to experiment and learn what things do on your own. Where's the fun in just being told everything?")
            input("- Nevermind lol the cheat code to find out the items in your inventory is actually \"Y'all Suckers\"")
            input("- If you're reading this, you should know that that the final boss is actually gaurded by super tough enemies.")
            input("- You should also know that there is actually a secret post-win area with some fun stuff to find if you can get there :)")
            input("- The game is not actually supposed to be that hard, it's just that the dodge prompts can be pretty unforgiving if you mess up even once. If you're struggling, try to focus on dodging and don't worry too much about strategy.")
            input("- That being said, strategy can still be helpful! Some items are really good and can make the game much easier if you know how to use them. And of course, learning enemy patterns and how to dodge effectively is key to winning.")
            input("- There are more items, enemies, and even mechanics that aren't mentioned in the Real Knowledge Book™. Part of the fun is discovering them on your own!")
            input("- But, if you are just too curious (or impatient), you can type \"PlayerManual\" for a detailed player manual.")
            input("- Thanks for reading! I hope you enjoy the game :)")
            input("That's all.")

        elif input_str == "PlayerManual":
            input("Table of contents:")
            input("\"NoobManual\" - A beginner's manual with tips and information about the game")
            input("\"walldoge\" - Tips for dodging effectively")
            input("\"itemhelp\" - Tips for using items effectively")
            input("\"enemyinfo\" - Information about the different enemies and their attack patterns")
            input("\"battletactics\" - Tips for when you are in battle")
            input("\"NoobManualV2\" - An updated beginner's manual with more detailed tips and strategies")
            input("\"behindthescenes\" - Tips and strategies to maximize your score")
            input("That's all.")

        elif input_str == "NoobManualV2":
            input("Here are some tips and strategies for doing the game better:")
            input("- Focus on learning how to dodge effectively. This is the most important skill in the game.")
            input("- Pay attention to enemy attack patterns and try to predict what they will do next.")
            input("- Experiment with different items and upgrades to find what works best for you.")
            input("- Don't be afraid to take risks and try new strategies!")
            input("- If you're struggling, try to focus on surviving and dodging rather than dealing damage. You can always come back and try to optimize your strategy later.")
            input("- Remember that the game is meant to be challenging, so don't get discouraged if you die a lot. Just keep practicing and learning from your mistakes!")
            input("- Speedrunning the game can be a fun way to challenge yourself once you're comfortable with it. Try to beat your best time!")
            input("- Also, another way to challenge yourself is to try to get a high score rather than just winning. Try to maximize your score!")
            input("That's all.")
       
        elif input_str == "behindthescenes":
            input("Here are some tips to get your score up:")
            input("- Your score goes up every time you sucessfuly dodge. That's important!")
            input("- Also, your score goes up for every time you beat an enemy.")
            input("- Bosses can get you a ton of points, and they give you more for how fast you beat it.")
            input("- Using items in their correct ways also awards points.")
            input("- The ammount of lives and saves you have if you win adds on to your points as well.")
            input("- NPCs are greatful to have you. You even get points for interacting with them!")
            input("- All the gold you get is counted. For each gold, that's a point!")
            input("- Finaly, you get a bonus 1000 points for winning.")
            input("- You can use the code \"DidIWin??\" to check your scores.")
            input("That's all.")

        elif input_str == "DidIWin??":

            TempKillScore = KillScore * 3
            LifeLeftScore = int(YourLife * 10) + (Saves * 50)
         
            print("your score for kills is " + str(TempKillScore) + ".")
            print("your score for dodges is " + str(DodgeScore) + ".")
            print("your score for killing bosses is " + str(BossScore) + ".")
            print("your score for remaining lives and saves is " + str(LifeLeftScore) + ".")
            print("your score for NPC interactions is " + str(NPCScore) + ".")
            print("your score for using items is " + str(ItemUseScore) + ".")
            print("your score for gold ammassed is " + str(TotalGold) + ".")
            print("your total score so far is " + str(WinBonus + LifeLeftScore + ItemUseScore + BossScore + DodgeScore + KillScore + NPCScore + TotalGold) + ".")

        else:
            break
    return

def attacks_this_turn(room: int, enemy_count: int) -> int:
    if room < 10:
        return min(enemy_count, random.randint(1, 2))
    elif room < 25:
        return min(enemy_count, random.randint(1, 3))
    elif room < 50:
        return min(enemy_count, random.randint(2, 3))
    elif room < 75:
        return min(enemy_count, random.randint(3, 4))
    else:
        return min(enemy_count, random.randint(4, 5))

while True:
    # -------------------------
    # Main Menu
    # -------------------------
    Print = [
    " _    _       _   _ _   _          _   _____                                        _____                      ",
    "| |  | |     | | (_) | | |        | | |  __ \                                      / ____|                     ",  # type: ignore
    "| |  | |_ __ | |_ _| |_| | ___  __| | | |  | |_   _ _ __   __ _  ___  ___  _ __   | |  __  __ _ _ __ ___   ___ ",
    "| |  | | '_ \| __| | __| |/ _ \/ _` | | |  | | | | | '_ \ / _` |/ _ \/ _ \| '_ \  | | |_ |/ _` | '_ ` _ \ / _ \ ", # type: ignore
    "| |__| | | | | |_| | |_| |  __/ (_| | | |__| | |_| | | | | (_| |  __/ (_) | | | | | |__| | (_| | | | | | |  __/",
    " \____/|_| |_|\__|_|\__|_|\___|\__,_| |_____/ \__,_|_| |_|\__, |\___|\___/|_| |_|  \_____|\__,_|_| |_| |_|\___|",  # type: ignore
    "                                                           __/ |                                               ",
    "                                                          |___/                                                ",
    ]

    for i in range(len(Print)):
        print(Print[i])
    choosing = True
    print("* 0: Exit\n* 1: Start Run\n* 2: View Achivements\n* 3: View Messages\n* 4: View Stats\n* 5: Shop\n")
    while choosing:
        userinput = input()
        if userinput == "0":
            exit()
        elif userinput == "1":
            choosing = False
        elif userinput == "2":
            AchivementsFile = open('Achivements.json')
            data = json.load(AchivementsFile)
            for i in data["achivements"]:
                if i["progress"] >= i["require"]:
                    print(GREEN+f'{i["name"]}: {i["description"]} {i["require"]} / {i["require"]}'+RESET)
                elif i["hidden"] == False:
                    print(f'{i["name"]}: {i["description"]} {i["progress"]} / {i["require"]}')
                else:
                    print(f'?????: ??????????? {i["progress"]} / {i["require"]}')
                print()
            AchivementsFile.close()
        elif userinput == "3":
            data = []
            if os.path.isfile("MessageList.json"):  
                MessagesFile = open('MessageList.json')
                data = json.load(MessagesFile)
                MessagesFile.close()
            if len(data) != 0:
                for message in data:
                    print(message[0] + " (room " + str(message[1]) + ", " + str(message[2]) + " points)")
            else:
                print("You have no messages.")

        else:
            print("Please enter a valid response.")
   
    choosing = True
    achivements_reward()
    while choosing:
        print("Pick a character!")
        for character in range(len(UnlockedCharacters)):
            print("* " + str(character) + ": " + UnlockedCharacters[character])
        userinput = input()
        if userinput.isdigit():
            if int(userinput) >= 0 and int(userinput) <= len(UnlockedCharacters) - 1:
                Character = UnlockedCharacters[int(userinput)]
                choosing = False
            else:
                print("Please enter a valid response.")
        else:
            print("Please enter a valid response.")

    # -------------------------
    # Game Setup
    # -------------------------
    Name = input("Before we get started, what's your name? ")
    skipinput = input("Okay, " + Name + ". How about I tell you what's goint on? (type anything other than enter to skip)")
    if skipinput == "":
        input("What you are about to see might just be the most puzzling thing that we have discovered in human history.")
        input("More confusing than the Bermuda Triangle, Area 51, and pinapple on pizza combine.")
        input("And trust me " + Name + ", it's not something we share with everyone.")
        input("We like to call it... the dungeon, a massive structure of bricks and endless rooms, all filled with strange species.")
        input("It showed up undergound one day in northern Michigan about a week ago.")
        input("We tried sending in a few cameras, but these... things, inside of it destroyed them instantly.")
        input("You, and about a couple of other people we found to be strong, brave, greedy, or powerful enough to be sent in there.")
        print("We did gather some information, so you can type 'NoobManual' right below here to read.")
    else:
        print("Type 'NoobManual' for starter information.")

    StarterCheatCodes()
    print("************\n")

    reset_room_multipliers()

    # Initialize room enemies
    get_enemy_options(room)
    CurrentEnemies, CurrentEnemiesHealth = spawn_enemy(room, 0)
    StunnedEnemies = [0 for _ in range(len(CurrentEnemies))]

    # -------------------------
    # Main Loop
    # -------------------------

    while running:
        SkipRoomNow = False  # reset per room-turn usage

        print("\n************\n")
        print("it is room " + str(room) + ".\n")

        print("Points: " + str(WinBonus + LifeLeftScore + ItemUseScore + BossScore + DodgeScore + KillScore + NPCScore + TotalGold) + "\n")

        inventory = sorted(inventory, key=reward_bank.index)
        print_inventory()
        
        print("you have " + str(Gold) + " gold.\n")

        print("You have taken " + str(TurnsTaken) + " turns.")

        # -------------------------
        # Player turn
        # -------------------------

        print("You are attacking.\n")

        if len(CurrentEnemies) > 1:
            print(str(len(CurrentEnemies)))
            for i, e in enumerate(CurrentEnemies):
               print(f"{i + 1}: {enemy_displays[enemy_bank.index(e)]} ({CurrentEnemiesHealth[i]} hp)")
            print()
            target_idx = attack_check(CurrentEnemies)
        elif len(CurrentEnemies) == 1:
            print(f"1: {enemy_displays[enemy_bank.index(CurrentEnemies[0])]} ({CurrentEnemiesHealth[0]} hp)\n")
            target_idx = 0

        temp_disarm_all = 0

    # new health, heal, dodge multi, damage multi, defence multi, disarm, damage all, disarm all

        if CurrentEnemies:
            new_hp, heal, dodge_multi, dmg_multi, def_multi, disarm, damage_all, temp_disarm_all = attack_enemy(
                CurrentEnemies[target_idx],
                CurrentEnemiesHealth[target_idx],  # type: ignore
            )
            CurrentEnemiesHealth[target_idx] = new_hp

        disarm_all += temp_disarm_all

        # AoE damage
        if damage_all != 0:
            for i in range(len(CurrentEnemiesHealth)):
                CurrentEnemiesHealth[i] -= damage_all

        # Apply room multipliers
        RoomDodge *= dodge_multi
        RoomDamage *= dmg_multi
        RoomDefence *= def_multi

        # Apply stuns
        if disarm > 0 and target_idx < len(StunnedEnemies):
            StunnedEnemies[target_idx] = max(StunnedEnemies[target_idx], disarm)

        # Cleanup dead enemies + rewards
        apply_aoe_and_cleanup(CurrentEnemies, CurrentEnemiesHealth, StunnedEnemies) # type: ignore

        # Apply healing
        while heal > 0 and YourLife < MaxLife:
            YourLife = min(MaxLife, round(YourLife + 1.0, 2))
            heal -= 1
            HealUsed = True

        # Room clear check (FIXED: include SkipRoomNow)
        if SkipRoomNow or not CurrentEnemies:
            LevelBeat = True
        else:
            LevelBeat = False

        # -------------------------
        # Enemy turn
        # -------------------------

        def pressure_dodges(times: int, choices: list[str], damage: float):
            times = max(1, times)
            for _ in range(times):
                expected = random.choice(choices)
                userinput = input("type " + expected + " to dodge! ")
                if userinput != expected:
                    take_damage(damage)
                    print("you failed to dodge... It dealt " + str(float(damage)) + " damage.")
                    print("you have " + str(YourLife) + " life left.")
                    break

        def take_damage(amount):
            global YourLife
            new_life = YourLife
            new_life -= amount / max(0.0001, RoomDefence)
            YourLife = round(new_life, 2)

        if not LevelBeat:
            if disarm_all <= 0:
                attacker_idx = random.randrange(len(CurrentEnemies))
                enemy_hp = CurrentEnemiesHealth[attacker_idx]
                attack_count = attacks_this_turn(room, len(CurrentEnemies))
                attackers = random.sample(range(len(CurrentEnemies)), attack_count)
                for enemy in CurrentEnemies:
                    if enemy in bosses and CurrentEnemies.index(enemy) not in attackers:
                        attackers.append(CurrentEnemies.index(enemy))
                        break
                for attacker_idx in attackers:
                    if attacker_idx < len(CurrentEnemies) and YourLife > 0:
                        YourLife = enemy_attack(
                            attacker_idx,
                            YourLife,
                            StunnedEnemies,
                            CurrentEnemies,
                            CurrentEnemiesHealth[attacker_idx]
                        )
                if "Flameboi" in CurrentEnemies:
                    pressure_dodges(1, easy_dodges, 1)
                    CauseOfDeath = "Flameboi"
                if "Exploding Mush" in CurrentEnemies:
                    if room % 2 == 0:
                        print("The Exploding Mush is boosting the attack power of all its teammates!")
                        RoomDodge -= 0.1
                if "Gloompy" in CurrentEnemies:
                    if room % 2 == 1:
                        print("The Gloompy is boosting the damage of all its teammates!")
                        RoomDefence -= 0.1
                if "Voice From Above" in CurrentEnemies:
                    if room % 5 == 0:
                        CurrentEnemies.append(random.choice(enemy_types1))
                        CurrentEnemiesHealth.append(random.randint(0, 3))
                        StunnedEnemies.append(0)
                        print("The Voice From Above commands more enemies into the room!")
                        print("a " + enemy_displays[enemy_bank.index(str(CurrentEnemies[len(CurrentEnemies) - 1]))] + " has spawned!")
                        print("it has " + str(CurrentEnemiesHealth[-1]) + " health.")
                if "Googly Eye Storm" in CurrentEnemies:
                    pressure_dodges(1, hardererest_dodges, 3)
                    CauseOfDeath = "Googly Eye Storm"
            if YourLife <= 0:
                if Saves == 0:
                    death = True
                    running = False
                    print("\nYou have died. \n\n")
                    do_death_messages(room, CauseOfDeath)
                else:
                    Saves -= 1
                    print("You have died...")
                    print("But you must keep going!")
                    print("You can die " + str(Saves) + " more times.\n*************\n")
                    YourLife = MaxLife
                    reset_room_multipliers()
                    get_enemy_options(room)
                    CurrentEnemies, CurrentEnemiesHealth = spawn_enemy(room, 0)
                    StunnedEnemies = [0 for _ in range(len(CurrentEnemies))]
        elif disarm_all != 0:
            print("All enemies are distracted and cannot attack this turn!")
            print("You get to go again!")
            disarm_all -= 1
       
        if room < 10:
            base_life = math.ceil(room / 2)
        elif room < 25:
            base_life = math.ceil(room / 1.5)
        elif room < 40:
            base_life = room
        elif room < 75:
            base_life = math.ceil(room * 1.5)
        else:
            base_life = math.ceil(room * 2)

        if not LevelBeat and running and not BossLevel:
            if TurnsTaken == 3:
                CurrentEnemies.append("Flameboi")
                CurrentEnemiesHealth.append(int(base_life + random.randint(0, 3)))
                StunnedEnemies.append(0)
                print("Enemies call for backup!")
                print("a " + enemy_displays[enemy_bank.index("Flameboi")] + " has spawned!")
                print("it has " + str(CurrentEnemiesHealth[len(CurrentEnemiesHealth) - 1]) + " health.")
            elif TurnsTaken == 5:
                CurrentEnemies.append("Exploding Mush")
                CurrentEnemiesHealth.append(int(base_life + random.randint(0, 3)))
                StunnedEnemies.append(0)
                print("You're taking too long!")
                print("a " + enemy_displays[enemy_bank.index("Exploding Mush")] + " has spawned!")
                print("it has " + str(CurrentEnemiesHealth[len(CurrentEnemiesHealth) - 1]) + " health.")
            elif TurnsTaken == 7:
                CurrentEnemies.append("Gloompy")
                CurrentEnemiesHealth.append(int(base_life + random.randint(0, 3)))
                StunnedEnemies.append(0)
                print("You need to hurry up!")
                print("a " + enemy_displays[enemy_bank.index("Gloompy")] + " has spawned!")
                print("it has " + str(CurrentEnemiesHealth[len(CurrentEnemiesHealth) - 1]) + " health.")
            elif TurnsTaken == 9:
                CurrentEnemies.append("Voice From Above")
                CurrentEnemiesHealth.append(int(base_life + random.randint(0, 3)))
                StunnedEnemies.append(0)
                print("Cracks form in the walls!")
                print("a " + enemy_displays[enemy_bank.index("Voice From Above")] + " has spawned!")
                print("it has " + str(CurrentEnemiesHealth[len(CurrentEnemiesHealth) - 1]) + " health.")
            elif TurnsTaken == 11:
                CurrentEnemies.append("Googly Eye Storm")
                CurrentEnemiesHealth.append(int(base_life + random.randint(0, 3)))
                StunnedEnemies.append(0)
                print("The dungeon grows mad!")
                print("a " + enemy_displays[enemy_bank.index("Googly Eye Storm")] + " has spawned!")
                print("it has " + str(CurrentEnemiesHealth[len(CurrentEnemiesHealth) - 1]) + " health.")

            TurnsTaken += 1

        # -------------------------
        # Room cleared / progression
        # -------------------------

        if LevelBeat and running:
            SpectatorHits = 0

            if room != 100:
                print("\nYou have cleared the room!\n")

                print("1: Max life, 2: Attack power, 3: Defence, 4: Dodge power")
                PermUpgrade()
                print()

                ChestName = ""
               
                if RoomType in [1, 3, 4, 5, 13]:
                    print("You find a chest!")
                    if room <= 10:
                        ChestName = random.choice(Chests1)
                        Chest(0, ChestName)
                    elif room <= 25:
                        ChestName = random.choice(Chests2)
                        Chest(1, ChestName)
                    elif room <= 40:
                        ChestName = random.choice(Chests3)
                        Chest(2, ChestName)
                    elif room <= 75:
                        ChestName = random.choice(Chests4)
                        Chest(3, ChestName)
                    elif room <= 90:
                        ChestName = random.choice(Chests5)
                        Chest(4, ChestName)
                    elif room <= 100:
                        ChestName = random.choice(Chests2)
                        Chest(1, ChestName)
                    ChestMercy = 5
                else:
                    ChestMercy -= 1
               
                if RoomType in [4, 5, 13]:
                    print("You find another chest!")
                    if room <= 10:
                        ChestName = random.choice(Chests1)
                        Chest(0, ChestName)
                    elif room <= 25:
                        ChestName = random.choice(Chests2)
                        Chest(1, ChestName)
                    elif room <= 40:
                        ChestName = random.choice(Chests3)
                        Chest(2, ChestName)
                    elif room <= 75:
                        ChestName = random.choice(Chests4)
                        Chest(3, ChestName)
                    elif room <= 90:
                        ChestName = random.choice(Chests5)
                        Chest(4, ChestName)
                    elif room <= 100:
                        ChestName = random.choice(Chests2)
                        Chest(1, ChestName)
                    ChestMercy = 5

                if RoomType == 2:
                    Shopping = True
                    print("Some shopkeepers appear!\n")
                    ShopKeeperType1 = random.randrange(0, 4)
                    ShopKeeperType2 = random.randrange(0, 4)
                    ShopKeeperType3 = random.randrange(0, 4)
                    ShopKeeperRef1:callable = lambda:None  # type: ignore
                    ShopKeeperRef2:callable = lambda:None  # type: ignore
                    ShopKeeperRef3:callable = lambda:None  # type: ignore
                    ShopKeeperInventory1 = None
                    ShopKeeperInventory2 = None
                    ShopKeeperInventory3 = None
                    if ShopKeeperType1 == 0:
                        print("The first shopkeeper is a trader! They will trade you an item for an item.")
                        ShopKeeperRef1 = Trader
                        ShopKeeperInventory1 = Trader(0, None)
                    elif ShopKeeperType1 == 1:
                        print("The first shopkeeper is a merchant! They will sell you an item for gold.")
                        ShopKeeperRef1 = Merchant
                        ShopKeeperInventory1 = Merchant(0, None)
                    elif ShopKeeperType1 == 2:
                        print("The first shopkeeper is a wizard! They will upgrade your items for a price.")
                        ShopKeeperRef1 = Wizard
                    elif ShopKeeperType1 == 3:
                        print("The first shopkeeper is a gambler! They will have you gamble for money.")
                        ShopKeeperRef1 = Gambler(0, None)
                    elif ShopKeeperType1 == 4:
                        print("The first shopkeeper is a medic! They will heal you for a price.")
                        ShopKeeperRef1 = Medic
                    print("")
                    if ShopKeeperType2 == 0:
                        print("The second shopkeeper is a trader! They will trade you an item for an item.")
                        ShopKeeperRef2 = Trader
                        ShopKeeperInventory2 = Trader(0, None)
                    elif ShopKeeperType2 == 1:
                        print("The second shopkeeper is a merchant! They will sell you an item for gold.")
                        ShopKeeperRef2 = Merchant
                        ShopKeeperInventory2 = Merchant(0, None)
                    elif ShopKeeperType2 == 2:
                        print("The second shopkeeper is a wizard! They will upgrade your items for a price.")
                        ShopKeeperRef2 = Wizard
                    elif ShopKeeperType2 == 3:
                        print("The second shopkeeper is a gambler! They will have you gamble for money.")
                        ShopKeeperRef2 = Gambler(0, None)
                    elif ShopKeeperType2 == 4:
                        print("The second shopkeeper is a medic! They will heal you for a price.")
                        ShopKeeperRef2 = Medic
                    print("")
                    if ShopKeeperType3 == 0:
                        print("The third shopkeeper is a trader! They will trade you an item for an item.")
                        ShopKeeperRef3 = Trader
                        ShopKeeperInventory3 = Trader(0, None)
                    elif ShopKeeperType3 == 1:
                        print("The third shopkeeper is a merchant! They will sell you an item for gold.")
                        ShopKeeperRef3 = Merchant
                        ShopKeeperInventory3 = Merchant(0, None)
                    elif ShopKeeperType3 == 2:
                        print("The third shopkeeper is a wizard! They will upgrade your items for a price.")
                        ShopKeeperRef3 = Wizard
                    elif ShopKeeperType3 == 3:
                        print("The third shopkeeper is a gambler! They will have you gamble for money.")
                        ShopKeeperRef3 = Gambler(0, None)
                    elif ShopKeeperType3 == 4:
                        print("The third shopkeeper is a medic! They will heal you for a price.")
                        ShopKeeperRef3 = Medic
                    print("")
                    while Shopping == True:
                        userinput = input("What shopkeeper will you go to? Type the number of the shopkeeper, or 0 to leave. ")
                        if userinput == "1":
                            ShopKeeperRef1(1, ShopKeeperInventory1)
                        elif userinput == "2":
                            ShopKeeperRef2(1, ShopKeeperInventory2)
                        elif userinput == "3":
                            ShopKeeperRef3(1, ShopKeeperInventory3)
                        elif userinput == "0":
                            Shopping = False
                        else:
                            print("Please print a valid response.")

            if room == 10:
                print("You found a book! Type KnowlegeBook to read.")

            room += 1

            reset_room_multipliers()
            get_enemy_options(room)
            if not room == 100:
                if room % 25 == 0:
                    BossLevel = True
                    if room == 25:
                        RoomType = 7
                    if room == 50:
                        RoomType = 8
                    if room == 75:
                        RoomType = 9
                    if room == 100:
                        RoomType = 10
                    CurrentEnemies, CurrentEnemiesHealth = spawn_enemy(room, 3)
                else:
                    BossLevel = False
                    RoomRNG = random.random()
                    if room == 99:
                        RoomType = 13
                    elif room in [1, 2, 3, 4, 5]:
                        RoomType = 0
                    elif RoomRNG <= MallRoomChance or room % 10 == 1:
                        RoomType = 2
                    elif RoomRNG <= MallRoomChance + ChestRoomChance or ChestMercy <= 0:
                        RoomType = 1
                    elif RoomRNG <= MallRoomChance + ChestRoomChance + CalmingRoomChance:
                        RoomType = 3
                    elif RoomRNG <= MallRoomChance + ChestRoomChance + CalmingRoomChance + ThroneRoomChance:
                        RoomType = 4
                    elif RoomRNG <= MallRoomChance + ChestRoomChance + CalmingRoomChance + ThroneRoomChance + HordeRoomChance:
                        RoomType = 5
                    elif RoomRNG <= MallRoomChance + ChestRoomChance + CalmingRoomChance + ThroneRoomChance + HordeRoomChance + DarkRoomChance:
                        RoomType = 6
                    else:
                        RoomType = 0
                    CurrentEnemies, CurrentEnemiesHealth = spawn_enemy(room, 0)
            StunnedEnemies = [0 for _ in range(len(CurrentEnemies))]

            HordeRoomChance += 0.01
            ThroneRoomChance += 0.01

            if room >= 75:
                DarkRoomChance += 0.1

            if room > 100:
                running = False
                print("YOU BEAT THE DUNGEON!!")
                do_win_messages()
                break
       
        elif running:
            print("Press enter to continue.")
            MidgameCheatInput()
           
    # -------------------------
    # End / scoring
    # -------------------------
    print("\n************\n")

    if death:
        print("You ended up dying before finishing room 100. Here is your score...")
    else:
        print("Nice job on finishing room 100! Here is your score...")

    WinBonus = 1000 if (not death and room > 100) else 0

    KillScore *= 3
    LifeLeftScore = int(YourLife * 10) + (Saves * 50)

    input("your score for kills is " + str(KillScore) + ".")
    input("your score for dodges is " + str(DodgeScore) + ".")
    input("your score for killing bosses is " + str(BossScore) + ".")
    input("your score for remaining lives and saves is " + str(LifeLeftScore) + ".")
    input("your score for NPC interactions is " + str(NPCScore) + ".")
    input("your score for using items is " + str(ItemUseScore) + ".")
    input("your score for gold ammassed is " + str(TotalGold) + ".")
    input("your bonus for winning is " + str(WinBonus) + ".")
    print("\n************\n")
    input("your total score is...")
    input("...")
    print(str(WinBonus + LifeLeftScore + ItemUseScore + BossScore + DodgeScore + KillScore + NPCScore + TotalGold) + "!! Nice Job!")