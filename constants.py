"""Constants needed for Mc Giver Labyrinth game"""

#Window parameter:
SPRITES_NUMBER = 15
SPRITE_SIZE = 30
WINDOW_SIZE = SPRITES_NUMBER * SPRITE_SIZE
WINDOW_WIDE = SPRITES_NUMBER * SPRITE_SIZE
WINDOW_LENGTH = WINDOW_WIDE + 60

#Images:
ETHER_IMAGE = "sources/images/ether.png"
FLOOR_IMAGE = "sources/images/floor1.png"
WARDEN_IMAGE = "sources/images/guardian.png"
MACGYVER_IMAGE = "sources/images/macgyver.png"
NEEDLE_IMAGE = "sources/images/needle.png"
ROD_IMAGE = "sources/images/rod.png"
WALL_IMAGE = "sources/images/wall.png"

#map:
MAP1 = "sources/map1.txt"
MAP2 = "sources/map2.txt"

#Tool's dictionary:

TOOL_LIST = {"ether": ETHER_IMAGE, "needle": NEEDLE_IMAGE, "rod": ROD_IMAGE}

#SOUNDS:

WIN_SOUND = "sources/sound/win_sound.wav"
GAME_OVER_SOUND = "sources/sound/game_over_sound.wav"
TOOLS_SOUND = "sources/sound/tools_sound.wav"

#COLORS:
COLOR_WIN = (9, 119, 146)
COLOR_LOSE = (146, 9, 35)
