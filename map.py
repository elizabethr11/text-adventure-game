from items import *
from colorama import Fore, Style

# map layout - locked rooms in red for when the player does not have the key
layout = f"""
+-----------+--------+--------+
|  {Fore.RED}WARDEN'S{Style.RESET_ALL} |  YOUR  | OTHER  |    
|   {Fore.RED}OFFICE{Style.RESET_ALL}  |  CELL  |  CELL  |  
|           |        |        |    
+----   ----+---  ---+--  ----+
|           |                 |
|              GREAT          |      N
|   YARD       HALL  +--------+    W + E
|           |                 |      S
|           |         KITCHEN |
+----   ----+---   --+        |
|	    |        +---   --+
| INFIRMARY | {Fore.RED}GUARD{Style.RESET_ALL}  |{Fore.RED}UTILITY{Style.RESET_ALL} |
|           |  {Fore.RED}ROOM{Style.RESET_ALL}  |  {Fore.RED}ROOM{Style.RESET_ALL}  |
+-----------+--------+--------+
"""

# map layout - locked rooms in green for when the player has the key
layout_unlocked = f"""
+-----------+--------+--------+
|  {Fore.GREEN}WARDEN'S{Style.RESET_ALL} |  YOUR  | OTHER  |    
|   {Fore.GREEN}OFFICE{Style.RESET_ALL}  |  CELL  |  CELL  |  
|           |        |        |    
+----   ----+---  ---+--  ----+
|           |                 |
|              GREAT          |      N
|   YARD       HALL  +--------+    W + E
|           |                 |      S
|           |         KITCHEN |
+----   ----+---   --+        |
|	    |        +---   --+
| INFIRMARY | {Fore.GREEN}GUARD{Style.RESET_ALL}  |{Fore.GREEN}UTILITY{Style.RESET_ALL} |
|           |  {Fore.GREEN}ROOM{Style.RESET_ALL}  |  {Fore.GREEN}ROOM{Style.RESET_ALL}  |
+-----------+--------+--------+
"""

room_player_cell = {
    "name": "your cell",
    "description": "The small, concrete-walled cell holds a single bed with worn-out sheets.\n"
                   "The bars separating you from freedom are cold to the touch,\n"
                   "and a tiny barred window allows in just enough light to keep the gloom at bay.\n"
                   "Your fellow prisoners groan from nearby cells,\n"
                   "occasionally exchanging whispers or the sound of footsteps pacing the limited space.",
    "items": [item_toothbrush, item_soap, item_comb, item_toothpaste, item_socks],
    "original items": [item_toothbrush, item_soap, item_comb, item_toothpaste, item_socks],
    "restricted": False,
    "exits": {
        "south": "great hall",
        "north": "escape tunnel"
    },
    "hidden_items": []
}

room_other_cell = {
    "name": "another cell",
    "description": "The small, concrete-walled cell holds a single bed with worn-out sheets.\n"
                   "The bars separating you from freedom are cold to the touch,\n"
                   "and a tiny barred window allows in just enough light to keep the gloom at bay.\n"
                   "Your fellow prisoners groan from nearby cells,\n"
                   "occasionally exchanging whispers or the sound of footsteps pacing the limited space.",
    "items": [item_toothbrush, item_soap, item_comb, item_toothpaste, item_socks],
    "original items": [item_toothbrush, item_soap, item_comb, item_toothpaste, item_socks],
    "restricted": False,
    "exits": {
        "south": "great hall"
    }
}

room_great_hall = {
    "name": "great hall",
    "description": "You stand in the Great Hall, the central hub of the prison.\n"
                   "The air is thick with a damp chill,\n"
                   "and the flickering fluorescent light overhead casts eerie shadows across the cracked tiles underfoot.\n"
                   "The walls are made of cold, unyielding stone,\n"
                   "with patches of moss creeping in from the corners,\n"
                   "a reminder of the years that have passed.\n"
                   "A guard is here.",
    "items": [],
    "original items": [],
    "restricted": False,
    "exits": {
        "north west": "your cell",
        "north east": "another cell",
        "east": "kitchen",
        "south": "guard room",
        "west": "yard"
    }
}

room_kitchen = {
    "name": "kitchen",
    "description": "The kitchen is a chaotic mess.\n"
                   "Pots clatter, dishes pile up, and steam rises from huge industrial-sized stoves.\n"
                   "The chef barks orders while chopping vegetables with a large, sharpened knife.\n"
                   "Near the sinks, utensils—including a spoon that could be useful—are left unsupervised during busy shifts.",
    "items": [item_spoon, item_food],
    "original items": [item_spoon, item_food],
    "restricted": False,
    "exits": {
        "west": "great hall",
        "south": "utility room"
    }
}

room_guard = {
    "name": "guard room",
    "description": "The guard room smells of stale coffee and sweat.\n"
                   "A small table with scattered paperwork, half-eaten snacks,\n"
                   "and a few weapons within arm’s reach sits in the center.\n"
                   "Security monitors flicker on one wall, showing live feeds from the various parts of the prison.\n"
                   "Guards patrol this area regularly.",
    "items": [],
    "original items": [],
    "restricted": True,
    "exits": {
        "north": "great hall"
    }
}

room_utility = {
    "name": "utility room",
    "description": "This small, dim room is a mess of cleaning supplies and old equipment.\n"
                   "The smell of bleach and chemicals lingers in the air.\n"
                   "In one corner, a rusty toolbox rests on a shelf—its contents largely forgotten by the guards but useful to the desperate.",
    "items": [item_screwdriver, item_batteries],
    "original items": [item_screwdriver, item_batteries],
    "restricted": True,
    "exits": {
        "north": "kitchen"
    }
}

room_yard = {
    "name": "yard",
    "description": "The prison yard is a wide, open space surrounded by towering fences topped with razor wire.\n"
                   "Concrete benches and a few patches of scraggly grass offer the only spots to sit.\n"
                   "Prisoners mill about, forming cliques as guards keep a close watch from elevated towers.\n"
                   "Weights and rusted exercise equipment line one side,\n"
                   "while on the other, a cracked basketball court sees occasional use.\n"
                   "The air smells faintly of sweat and damp concrete,\n"
                   "and there’s always a tension in the air, as if trouble could break out at any moment.\n"
                   "Beneath the surface, it’s a hub for trading favors, information, and contraband.",
    "items": [],
    "original items": [],
    "restricted": False,
    "exits": {
        "east": "great hall",
        "south": "infirmary",
        "north": "warden's office",
        "west": "freedom"
    }
}

room_warden = {
    "name": "warden's office",
    "description": "The warden’s office is a stark contrast to the cold, unforgiving prison.\n"
                   "It is furnished with dark wood, with a large, imposing desk that dominates the center.\n"
                   "The walls are lined with bookshelves, and security plans hang on a bulletin board.\n"
                   "The warden rarely visits this office but keeps it locked up when not in use.",
    "items": [],
    "original items": [],
    "restricted": True,
    "exits": {
        "south": "yard"
    }
}

room_infirmary = {
    "name": "infirmary",
    "description": "The infirmary is pristine compared to the rest of the prison.\n"
                   "A single nurse hovers over medical supplies while prisoners with injuries wait in uncomfortable chairs.\n"
                   "The smell of antiseptic fills the room,\n"
                   "and the cabinets are stocked with medications that could come in handy for bribing or healing.",
    "items": [item_medicine],
    "original items": [item_medicine],
    "restricted": False,
    "exits": {
        "north": "yard"
    }
}

room_escape_tunnel = {
    "name": "escape tunnel",
    "description": "The escape tunnel winds through the damp, dimly lit sewers beneath the prison,\n"
                   "its walls slick with moisture and lined with crumbling bricks.",
    "items": [],
    "original items": [],
    "restricted": True,
    "shown": False,
    "exits": {
        "north": "freedom",
        "south": "your cell"
    }
}

room_freedom = {
    "name": "freedom",
    "description": "You have finally achieved what you have been working for all this time: freedom.",
    "items": [],
    "original items": [],
    "restricted": True,
    "shown": False,
    "exits": {}
}

# dictionary of rooms - used to find the room dictionary from the room's name
rooms = {
    "your cell": room_player_cell,
    "another cell": room_other_cell,
    "great hall": room_great_hall,
    "kitchen": room_kitchen,
    "utility room": room_utility,
    "guard room": room_guard,
    "yard": room_yard,
    "warden's office": room_warden,
    "infirmary": room_infirmary,
    "escape tunnel": room_escape_tunnel,
    "freedom": room_freedom
}

# dictionary of possible warden announcements in the morning (turn 1 of the day cycle)
announcements = {
    1: "Attention, Inmates!\n"
       "Wake up and prepare yourselves for the day ahead.\n"
       "There’s no room for weakness here.",

    2: "Your personal area must be kept spotless!\n"
       "A dirty space reflects poorly on all of us.\n"
       "Report any disturbances to the staff immediately—\n"
       "failure to do so will not be tolerated.",

    3: "Hydration is critical for your survival!\n"
       "Water stations are available, and you must stay alert.\n"
       "Don’t let dehydration slow you down.",

    4: "Remember! This is a place of order.\n"
       "Follow the rules, respect your fellow inmates,\n"
       "and know that any disruption will have serious consequences."
}

