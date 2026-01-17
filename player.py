# import files
from items import *
from map import *

# the player starts with nothing in their inventory
inventory = []

# the player cannot carry more items than 1 kilogram's worth of items
maximum_mass = 1
items_mass = 0

# start game in the player's cell
current_room = rooms["your cell"]