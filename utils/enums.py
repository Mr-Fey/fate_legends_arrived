from enum import Enum 


class CharacterRarity(Enum): 
    common = "common" 
    notcommon = "not-common"
    grand = "grand"
    rare = notcommon


class ItemRarity(Enum): 
    common = "common" 
    rare = "rare" 
    epic = "epic"
    legendary = "legendary"
    limited = "limited" 
    event = limited