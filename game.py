# importing functions from other files
from map import *
from player import *
from items import *
from gameparser import *

# importing libraries
import time
import os
from random import randint
from colorama import Fore, Style

def introduction():
    """""""introduction text to set the scene for the game"""
    
    slow_print("\n=========================================")
    slow_print("          Welcome to Prison Break      ")
    slow_print("=========================================")
    slow_print("\nYou find yourself in the cold, dark confines of HMP Cardiff.")
    slow_print("You've been imprisoned for life, and the only chance of revenge is escape.")
    slow_print("\nTime is running out! The guards are on high alert, and the clock is ticking.")
    slow_print("Gather your courage, make strategic choices, and use your wits to navigate through the dangers ahead.")
    slow_print("\nWill you manage to break free, or will you be caught in the act?")
    slow_print("Your choices will determine your fate.")
    slow_print("\nGood luck, prisoner. Your escape begins now!")
    slow_print("\n[press enter to start]")
    input()


def execute_go(direction: str) -> None:
    """This function, given the direction (e.g. "south") updates the current room
    to reflect the movement of the player if the direction is a valid exit
    (and prints the name of the room into which the player is
    moving). Otherwise, it prints "You cannot go there."
    """
    global current_room, current_turn, total_turns

    # check if the exit exists
    if direction in current_room["exits"]:

        # get the exit room's dictionary
        new_room_name = current_room["exits"][direction]
        new_room = rooms[new_room_name]

        # check if the room is restricted (or if you have access to the room with a key)
        if (new_room["restricted"] == False or item_key in inventory):
            # only show the escape tunnels if the player has finished digging / unscrewed the toilet
            if (new_room == room_escape_tunnel and not room_escape_tunnel["shown"]) or (new_room == room_freedom and not room_freedom["shown"]):
                slow_print(Fore.RED + "Cannot go there." + Style.RESET_ALL)
                return
            else:
                # only go to new room if it is not turning night time (as the user is returned to their cell instead)
                if current_turn < 6:
                    current_room = new_room
                    slow_print(f"""Going to {current_room["name"]}""")
                current_turn += 1
                total_turns += 1
        else:
            slow_print(Fore.RED +"That room is restricted."+ Style.RESET_ALL)
            return


    else:
        slow_print(Fore.RED +"You cannot go there." + Style.RESET_ALL)


def execute_take(item_id: str) -> None:
    """This function takes an item_id as an argument and moves this item from the
    list of items in the current room to the player's inventory. However, if
    there is no such item in the room, this function prints
    "You cannot take that."
    """
    global items_mass, current_turn, total_turns

    # cycles through items in the room
    for item in current_room["items"]:
        if (item["id"] == item_id) and (item["id"] != "key"):
            # ensures that the item is not too heavy
            if (items_mass + item["mass"] < maximum_mass):
                inventory.append(item)
                current_room["items"] = remove_from_list(item_id, current_room["items"])
                slow_print(f"""You have taken {item_id}.""")
                items_mass = round(sum([item["mass"] for item in inventory]), 2)
                current_turn += 1
                total_turns += 1
                return
            else:
                slow_print(Fore.RED +f"""Too heavy! You have to drop something before picking {item["name"]} up."""+ Style.RESET_ALL)
                return
    slow_print(Fore.RED +"You cannot take that."+ Style.RESET_ALL)


def execute_drop(item_id: str) -> None:
    """This function takes an item_id as an argument and moves this item from the
    player's inventory to list of items in the current room. However, if there is
    no such item in the inventory, this function prints "You cannot drop that."
    """
    global items_mass, current_turn, total_turns

    # cycles through inventory items
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            items_mass = round(sum([item["mass"] for item in inventory]), 2)
            current_turn += 1
            total_turns += 1
            if item_id == "key":
                item_key["on guard"] = True
                slow_print(Fore.MAGENTA + "GUARD: Oh, it looks like I dropped this! Lucky I found it just in time." + Style.RESET_ALL)
                return
            current_room["items"].append(item)
            slow_print(f"""you have dropped {item_id}""")
            return

    slow_print(Fore.RED+"You cannot drop that"+Style.RESET_ALL)
    
    
def execute_hide(item_id: str) -> None:
    """This function takes an idem_id as an argument and moves this item from the player's
    inventory to list of items in his cell that are hidden."""

    global items_mass, current_turn, total_turns

    # checks that the user is in their cell
    if current_room["name"] != "your cell":
        slow_print("You cannot hide items here.")
        return

    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            room_player_cell["hidden_items"].append(item)
            
            slow_print(f"""You have hidden {item_id}.""")
            items_mass = round(sum([item["mass"] for item in inventory]), 2)
            current_turn += 1
            total_turns += 1
            return


def execute_unhide(item_id: str) -> None:
    """
    Allows the player to remove items from the hidden compartment in their cell.
    """

    global items_mass, current_turn, total_turns
    
    # checks that the user is in their cell
    if current_room["name"] != "your cell":
        slow_print("You cannot remove hidden items from here.")
        return

    for item in room_player_cell["hidden_items"]:
        if (item["id"] == item_id):
            if (items_mass + item["mass"] < maximum_mass):
                inventory.append(item)
                room_player_cell["hidden_items"] = remove_from_list(item_id, room_player_cell["hidden_items"])
                slow_print(f"""You have removed {item_id} from the hidden compartment.""")
                items_mass = round(sum([item["mass"] for item in inventory]), 2)
                current_turn += 1
                total_turns += 1
                return
            else:
                slow_print(Fore.RED+f"""Too heavy! You have to drop something before picking {item["name"]} up."""+Style.RESET_ALL)
                return
    slow_print("You cannot take that.")


def execute_steal() -> None:
    """
    This function is called when the player attempts to steal the guard's key. There is a 1 in 3 chance of being caught.
    If the player is caught, it calls the execute_catch() function, if not the key is added to the player's inventory.
    """
    global current_turn, items_mass, total_turns

    # checks that the user is in the great hall
    if current_room == room_great_hall and item_key["on guard"]:
        
        if items_mass + item_key["mass"] <= maximum_mass:
            inventory.append(item_key)
            items_mass = round(sum([item["mass"] for item in inventory]), 2)

            probability  = randint(1, 10)
            if probability <= 3:
                item_key["on guard"] = True
                search_player(theft=True)
            else:
                item_key["on guard"] = False
                slow_print("You have stolen the key!")

            current_turn += 1
            total_turns += 1
        else:
            slow_print(Fore.RED+f"""Too heavy! You have to drop something before stealing the key."""+Style.RESET_ALL)


def execute_unscrew() -> None:
    """
    This function tells the player that they are escaping and unveils the escape tunnel (and freedom).
    """
    global current_turn, total_turns

    slow_print("You successfully unscrew the toilet, revealing a passageway through the sewers.")
    room_escape_tunnel["shown"] = True
    room_escape_tunnel["restricted"] = False
    room_freedom["restricted"] = False
    room_freedom["shown"] = True

    current_turn += 1
    total_turns += 1


def execute_dig() -> None:
    """
    This function adds one to the number of digs with the spoon that the player has done.
    If the player reaches 30 digs, they will have dug enough to create a hole to escape.
    """
    global dig_count, current_turn, total_turns

    # total number of digs needed before being able to escape
    digs_needed = 5
    dig_count += 1
    current_turn += 1
    total_turns += 1
    # check if the player has digged enough
    if dig_count >= digs_needed:
        slow_print("You have dug out a large enough hole to escape.")
        room_freedom["restricted"] = False
        room_freedom["shown"] = True
    else:
        # update the player on the distance left to dig
        slow_print(f"You are {int((dig_count / digs_needed)*100)}% of the way there...")

def execute_hint() -> None:
    global total_hints
    total_hints += 1

    # player has spoon and is in the yard
    if item_spoon in inventory and current_room["name"] == "yard":
        slow_print(Fore.YELLOW + "It may take a while to dig a hole large enough to escape." + Style.RESET_ALL)
    # player has the screwdriver
    if item_screwdriver in inventory:
        slow_print(Fore.YELLOW + "Take the screwdriver to your cell and see what happens." + Style.RESET_ALL)
        return
    # player has the spoon, but is not in the yard
    if item_spoon in inventory:
        slow_print(Fore.YELLOW + "Take the spoon to the yard and see what happens." + Style.RESET_ALL)
        return
    # player has the key, but not the screwdriver
    if item_key in inventory:
        slow_print(Fore.YELLOW + "The key opens restricted rooms (red rooms on the map)" + Style.RESET_ALL)
        return
    # player has nothing
    if item_spoon not in inventory and item_screwdriver not in inventory:
        slow_print(Fore.YELLOW + "Have a look around and see which objects could help you to escape." + Style.RESET_ALL)

def execute_command(command: list) -> None:
    """This function takes a command (a list of words as returned by
    normalise_input) and, depending on the type of action (the first word of
    the command: "go", "take", or "drop"), executes either execute_go,
    execute_take, or execute_drop, supplying the second word as the argument.

    """

    if len(command) == 0:
        return

    if command[0] == "go":
        if len(command) == 2:
            execute_go(command[1])
        # checks if the direction includes 2 words (i.e. north west or north east)
        elif len(command) > 2:
            execute_go(command[1] + " " + command[2])
        else:
            slow_print(Fore.YELLOW + "Go where?" + Style.RESET_ALL)

    elif command[0] == "take":

        if len(command) > 1:
            execute_take(command[1])
        else:
            slow_print(Fore.YELLOW + "Take what?" + Style.RESET_ALL)

    elif command[0] == "drop":
        if len(command) > 1:
            execute_drop(command[1])
        else:
            slow_print(Fore.YELLOW + "Drop what?" + Style.RESET_ALL)

    elif command[0] == "steal":
        if len(command) > 1:
            print("stealing...")
            execute_steal()
        else:
            slow_print(Fore.YELLOW + "Steal what?" + Style.RESET_ALL)

    elif command[0] == "hide":
            if len(command) > 1:
                execute_hide(command[1])
            else:
                slow_print(Fore.YELLOW + "Hide what?" + Style.RESET_ALL)

    elif command[0] == "remove":
            if len(command) > 1:
                execute_unhide(command[1])
            else:
                slow_print(Fore.YELLOW + "Remove what?" + Style.RESET_ALL)

    elif command[0] == "unscrew":
            if current_room == room_player_cell and item_screwdriver in inventory:
                execute_unscrew()
            else:
                print(Fore.YELLOW + "This makes no sense." + Style.RESET_ALL)
    elif command[0] == "dig":
            if current_room == room_yard and item_spoon in inventory:
                execute_dig()
            else:
                print(Fore.YELLOW + "This makes no sense." + Style.RESET_ALL)

    elif command[0] == "hint":
        execute_hint()

    elif command[0] == "show" or command[0] == "map":
        # changes the colour of the restricted rooms on the map if the player has the key
        if item_key in inventory:
            slow_print(layout_unlocked)
        else:
            slow_print(layout)

    else:
        print("This makes no sense.")


# initialise key variables
current_turn = 0
total_turns = 0
curr_time = "day"
dig_count = 0
turns_per_day = 6
total_hints = 0
total_catches = 0


def turn() -> str:
    """
    This function checks which turn the player is on, and if it is the end of the night/day, it updates the current time.
    If it is the end of the day, the player is moved to their cell.
    If it is the start of the day, there is an announcement by the warden and a possibility of a random warden inspection.
    Halfway through the day, there is the possibility of a random search by the guard.
    Each player action (e.g. move, take, drop...) counts as a turn if the command is valid (successfully executed)
    """
    global current_room, curr_time, total_turns, current_turn
    
    # switch to night time after a certain amount of days (turns_per_day) have passed
    if current_turn == turns_per_day and curr_time == "day":
        curr_time = switch_time(curr_time)
        # reset the current_turn
        current_turn = 0

        # return (escort) the user back to their cell for the night
        if current_room != rooms["your cell"]:
            current_room = rooms["your cell"]

    # if the night has passed (1 day), switch the time back to day
    if current_turn == 1 and curr_time == "night":
        curr_time = switch_time(curr_time)
        current_turn = 0
        # 50% chance of a cell search every morning (after switch from night to day)
        search_cell()

    probability = randint(1, 10)
    if current_room != rooms["escape tunnel"] and probability <= 2 and current_turn > 3:
        # 20% chance of a random player inspection in the afternoon (turn 3 or later)
        search_player(random_inspection=True)

    # display a random warden announcement every morning
    if current_turn == 1:
        randomizer = randint(1, 4)
        slow_print(Fore.BLUE + Style.BRIGHT +"Warden's Announcements: " + announcements[randomizer] + Style.RESET_ALL + "\n")

    # inform the user on how many turns are left before night time
    if current_turn != 0 and curr_time == "day":
        slow_print(f"You have {turns_per_day - current_turn} turn{"s" if turns_per_day - current_turn != 1 else ""} left until night time")

    return curr_time


def switch_time(curr_time: str) -> str:
    """switch between night and day and display an appropriate message"""
    if curr_time == "day":
        slow_print(Fore.BLUE + "It is now night time (you have been escorted back to your cell)." + Style.RESET_ALL)
        return "night"
    slow_print(Fore.YELLOW + Style.BRIGHT + "It is now day time." + Style.RESET_ALL)
    slow_print()
    return "day"


def slow_print(text: str="", *argv) -> None:
    """This function slows the text when it is being printed."""

    for item in argv:
        text += " " + str(item)

    for char in text + "\n":
        print(char, end="", flush=True)
        time.sleep(0.003)


def list_of_items(items: dict) -> list:
    """This function takes a list of items and
    returns a comma-separated list of item names (as a string).
    """

    item_list = ""
    for item in items:
        item_list += item["name"] + ", "

    return item_list[:-2]


def print_room_items(room: dict) -> None:
    """This function takes a room as an input and nicely displays a list of items
    found in this room (followed by a blank line). If there are no items in
    the room, nothing is printed. See map.py for the definition of a room, and
    items.py for the definition of an item. This function uses list_of_items()
    to produce a comma-separated list of item names.
    """
    global current_room, curr_time
    # convert the list of items in the room to a string of items (separated by commas)
    room_items = list_of_items(room["items"])
    if room_items:
        slow_print(Fore.CYAN + Style.BRIGHT + f"""There is {room_items} here."""+ Style.RESET_ALL)
        slow_print()


def print_inventory_items(items: list) -> None:
    """This function takes a list of inventory items and displays it nicely, in a
    manner similar to print_room_items(). The only difference is in formatting:
    print "You have ..." instead of "There is ... here.". For example:
    """
    global current_room, curr_time
    # ensure that the items list is not empty 
    if items:
        slow_print(Fore.CYAN + Style.BRIGHT + f"""You have {list_of_items(items)}."""+Style.RESET_ALL)
        slow_print()


def print_room(room: dict) -> None:
    """This function takes a room as an input and nicely displays its name
    and description. The room argument is a dictionary with entries "name",
    "description" etc. (see map.py for the definition). The name of the room
    is printed in all capitals and framed by blank lines. Then follows the
    description of the room and a blank line again. If there are any items
    in the room, the list of items is printed next followed by a blank line
    (use print_room_items() for this).
    """
    global current_room, curr_time
    # Display room name
    print()
    slow_print(room["name"].upper())
    print()
    # Display room description
    slow_print(room["description"])
    # check if the user has escaped
    is_room_freedom()
    print()
    # print a list of the items in the current room
    print_room_items(room)


def is_room_freedom() -> None:
    """
    Checks if the current 'room' is freedom. If it is, display the win screen
    """
    global current_room
    if current_room["name"] == "freedom":
        win()


def exit_leads_to(exits: dict, direction: str) -> str:
    """This function takes a dictionary of exits and a direction (a particular
    exit taken from this dictionary). It returns the name of the room into which
    this exit leads.
    """
    return rooms[exits[direction]]["name"]


def print_exit(direction: str, leads_to: str) -> None:
    """This function prints a line of a menu of exits. It takes a direction (the
    name of an exit) and the name of the room into which it leads (leads_to),
    and should print a menu line in the following format:
    GO <EXIT NAME UPPERCASE> to <where it leads>.
    """

    # highlight the statement in green if the exit is an escape tunnel (or 'freedom')
    if leads_to == "freedom" or leads_to == "escape tunnel":
        slow_print(Fore.GREEN + Style.BRIGHT + "GO " + direction.upper() + " to " + leads_to + "." + Style.RESET_ALL)
    else:
        slow_print("GO " + direction.upper() + " to " + leads_to + ".")


def print_menu(exits: dict, room_items: list, inv_items: list) -> None:
    """This function displays the menu of available actions to the player. The
    argument exits is a dictionary of exits as exemplified in map.py. The
    arguments room_items and inv_items are the items lying around in the room
    and carried by the player respectively. The menu should, for each exit,
    call the function print_exit() to print the information about each exit in
    the appropriate format. The room into which an exit leads is obtained
    using the function exit_leads_to(). Then, it should print a list of commands
    related to items: for each item in the room print

    "TAKE <ITEM ID> to take <item name>."

    and for each item in the inventory print

    "DROP <ITEM ID> to drop <item name>."
    """
    global current_room, curr_time
    slow_print("You can:")
    
    #  Iterate over available exits
    for direction in exits:
        next_room = exit_leads_to(exits, direction)

        # ensure that the escape tunnel / freedom is only shown if it has been discovered (by digging or unscrewing the toilet)
        if (next_room != "freedom" or room_freedom["shown"]) and (next_room != "escape tunnel" or room_escape_tunnel["shown"]):
            #  Print the exit name and where it leads to
            print_exit(direction, exit_leads_to(exits, direction))

    # taking items
    for item in room_items:
        if item["id"] != "key":
            slow_print(f"""TAKE {item["id"].upper()} to take {item["name"]}.""")

    # un-hiding items
    if current_room["name"] == "your cell":
        for item in room_player_cell["hidden_items"]:
            slow_print(f"""REMOVE {item["id"].upper()} to take {item["name"]} from hidden compartment.""")

    # dropping items
    for item in inv_items:
        slow_print(f"""DROP {item["id"].upper()} to drop {item["name"]}.""")

    # hiding items
    if current_room == room_player_cell:
        for item in inventory:
            slow_print(f"""HIDE {item["id"].upper()} to hide {item["name"]} in the hidden compartment.""")

    # stealing items
    if current_room == room_great_hall and item_key not in inventory and item_key["on guard"]:
        slow_print(f"""STEAL {item_key["id"].upper()} to steal {item_key["name"]}.""")

    # unscrewing
    if current_room == room_player_cell and item_screwdriver in inventory:
        slow_print("UNSCREW toilet to escape.")

    # digging
    if current_room == room_yard and item_spoon in inventory:
        slow_print("DIG with spoon to escape.")

    # useful commands - do not use a turn
    slow_print("SHOW MAP to view the map.")
    slow_print("HINT to get a clue on what to do next.")

    slow_print("What do you want to do?")


def remove_from_list(item_id: str, items_list: list) -> list:
    """
    This function removes a given item from a given list based on the item's id.
    """
    global current_room, curr_time

    new_list = []

    for item in items_list:

        if item["id"] != item_id:

            new_list.append(item)

    return new_list


def menu(exits: dict, room_items: list, inv_items: list) -> list:
    """This function, given a dictionary of possible exits from a room, and a list
    of items found in the room and carried by the player, prints the menu of
    actions using print_menu() function. It then prompts the player to type an
    action. The players's input is normalised using the normalise_input()
    function before being returned."""

    global current_room, curr_time

    #  Display the user's options (e.g. drop, take, etc.)
    print_menu(exits, room_items, inv_items)

    #  Read player's input
    user_input = input(Fore.YELLOW + "> " + Style.RESET_ALL)

    #  Normalise the input - remove unnecessary words, punctuation, and whitespace
    normalised_user_input = normalise_input(user_input)

    return normalised_user_input


def move(exits: dict, direction: str) -> dict:
    """This function returns the room into which the player will move if, from a
    dictionary "exits" of avaiable exits, they choose to move towards the exit
    with the name given by "direction".
    """
    global current_room, curr_time
    #  Next room to go to
    return rooms[exits[direction]]


def return_to_origin(item: dict) -> None:
    """
    returns an item to the room they started in - used for contraband that needs
    to be returned after a room or player search.
    """

    origin_id = item["origin"]

    # check that the item has an origin and was not stolen
    if origin_id:
        origin = rooms[origin_id]
        origin["items"].append(item)


def empty_inv() -> bool:
    """
    This function is used when the player is caught. They lose all the contraband
    in their inventory (refer to contraband_list in gameparser.py).
    """
    global items_mass
    carrying_contraband = False

    # cycles through inventory items
    for item in inventory:

        item_id = item["id"]

        # checks whether the item is contraband
        if item_id in contraband_list_ids:
            if item == item_key:
                item_key["on guard"] = True
            inventory.remove(item)
            # returns the item to where it was at the beginning of the game (its origin)
            return_to_origin(item)
            carrying_contraband = True

    if inventory:
        last_item = inventory[-1]
        if last_item["id"] in contraband_list_ids:
            if last_item == item_key:
                item_key["on guard"] = True
            inventory.remove(last_item)
            return_to_origin(last_item)
            carrying_contraband = True

    items_mass = round(sum([item["mass"] for item in inventory]), 2)
    # return whether or not contraband was found on the player
    return carrying_contraband


def empty_cell() -> list:
    """
    This function is used when the player's call is inspected.
    They lose all items in their room's inventory that would be seen as contraband.
    returns a list of the contraband found in the cell
    """
    # initialise a list of contraband
    contraband = []

    # cycle through items in the player's cell
    for item in room_player_cell["items"]:
        if item["id"] in contraband_list_ids:
            if item == item_key:
                item_key["on guard"] = True
            # add the contraband to the list if it has not already been added
            if item["id"] not in contraband: contraband.append(item["id"])
            room_player_cell["items"].remove(item)
            return_to_origin(item)
    
    if room_player_cell["items"]:
        last_item = room_player_cell["items"][-1]
        if last_item["id"] in contraband_list_ids:
            if last_item == item_key:
                item_key["on guard"] = True
            contraband.append(last_item)
            room_player_cell["items"].remove(item)
            return_to_origin(item)

    # returns a list of contraband found in the cell
    return contraband

def search_cell() -> None:
    """ A random cell is chosen each day to be inspected (50% chance)"""
    
    cell_chosen = randint(1, 2)
    if cell_chosen == 1 and current_room != room_freedom and current_room != room_escape_tunnel:
        slow_print(Fore.RED + "Your cell was selected to be randomly inspected." + Style.RESET_ALL)
        
        # get the list of contraband found in the room
        contraband = empty_cell()
        # if the list is not empty then punish the player
        if contraband:
            slow_print(Fore.RED + f"The guards found contraband ({", ".join(contraband)}) in your room." + Style.RESET_ALL)
            punish()
        else:
            slow_print(Fore.GREEN + "The guards did not find any contraband in your room." + Style.RESET_ALL)

    else:
        slow_print(Fore.GREEN + "Your cell is safe from inspection today." + Style.RESET_ALL)


def search_player(theft: bool=False, random_inspection: bool=False) -> None:
    """
    This function gives a probability of 20% that the player will be searched by a guard.
    Any items considered contraband would be removed from their inventory.
    The player is informed of what has happened.
    """
    global items_mass, current_room, current_turn, total_turns

    if current_room != room_escape_tunnel and current_room != room_freedom:
        # checks if the player has any contraband on them (and returns contraband to their origin room)
        found_contraband = empty_inv()

        if found_contraband == True:
            # checks whether the search is from a random inspection or from a theft (stealing the key)
            if random_inspection:
                slow_print(Fore.RED + "The guards have randomly searched you and found contraband." + Style.RESET_ALL)
            elif theft:
                slow_print(Fore.RED + "The guard caught you stealing their key." + Style.RESET_ALL)

            punish()        

        else:
            slow_print(Fore.GREEN + "\nThe guards have searched you and found nothing.\n" + Style.RESET_ALL)


def punish() -> None:
    """
    Gives the player a 2 turn penalty, and returns (escorts) them back to their cell
    """
    global current_turn, total_turns, current_room, total_catches

    slow_print(Fore.RED + "They put you in the hole for 2 turns." + Style.RESET_ALL)
    slow_print()
    # check whether there is an overlap with the turns (if the 2 turn penalty exceeds the number of turns per day
    # then the penalty should carry on to the next day cycle)
    if current_turn + 2 >= turns_per_day:
        current_turn -= 4
    else:
        current_turn += 2
    total_turns += 2
    total_catches += 1
    # return the user to their cell
    current_room = rooms["your cell"]
    print()
    slow_print("You are now in", room_player_cell["name"])


def win() -> None:
    """
    Function executed after the player has escaped, and displays
    the number of turns taken, hints used, and times caught.
    """
    global current_turn, total_turns, curr_time, dig_count, total_hints, current_room, inventory, items_mass

    slow_print("\n" + divider + "\n")
    slow_print(Fore.GREEN + "Congratulations, you have escaped!" + Style.RESET_ALL)
    slow_print(Fore.GREEN + f"""You escaped in {total_turns} turns, used {total_hints} hint{"s" if total_hints != 1 else ""}, and were caught {total_catches} time{"s" if total_catches != 1 else ""}.""" + Style.RESET_ALL)
    slow_print()
    slow_print("Type restart to play again, or quit to exit the game.")

    while True:

        user_input = normalise_input(input(Fore.YELLOW + "> " + Style.RESET_ALL), win=True)
        if user_input == "restart" or user_input== "r":
            
            # reset all variables to their original values
            current_turn = 0
            total_turns = 0
            curr_time = "day"
            dig_count = 0
            total_hints = 0
            current_room = room_player_cell

            # reset the player's inventory
            inventory = []
            items_mass = round(sum([item["mass"] for item in inventory]), 2)

            # return all items to their original rooms
            for room in rooms.values():
                room["items"] = room["original items"]

            # reset escape routes
            room_escape_tunnel["shown"] = False
            room_escape_tunnel["restricted"] = True
            room_freedom["shown"] = False
            room_freedom["restricted"] = True

            # re-run the main loop
            main()

        # quit the game
        elif user_input == "quit" or user_input=="q":
            quit()
        
        else:
            slow_print(Fore.RED + "Invalid command." + Style.RESET_ALL)


#  This is the entry point of our program
def main() -> None:
    """main game loop"""
    global current_room

    # display the introduction sequence to set the scene of the game
    introduction()
    # display the map
    slow_print(layout)

    while True:
        # Display game status (room description, inventory etc.)
        turn()
        print_room(current_room)
        print_inventory_items(inventory)
        slow_print(f"""Your items weigh: {items_mass}kg (maximum: {maximum_mass}kg).""")
        print()

        # Show the menu with possible actions and ask the player
        command = menu(current_room["exits"], current_room["items"], inventory)

        # Execute the player's command
        execute_command(command)
        
        # Check if the user has escaped
        if current_room == room_freedom:
            win()

        # Add a divider to separate turns
        slow_print(f"\n{divider}\n")


# run main() if it is being executed from this script
if __name__ == "__main__":
    main()