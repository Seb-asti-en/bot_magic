class Board:

    #Constructeur
    def __init__(self,deck):
        self.__deck = deck
        self.__hand = []
        self.__battle_zone = []
        self.__land_zone = []
        self.__graveyard = []
        self.__exile = []

    #Getters
    def get_deck(self):
        return self.__deck
    
    def get_hand(self):
        return self.__hand

    def get_battle_zone(self):
        return self.__battle_zone
    
    def get_land_zone(self):
        return self.__land_zone
    
    def get_graveyard(self):
        return self.__graveyard

    def get_exile(self):
        return self.__exile

    #Setters
    def set_deck(self,deck):
        self.__deck = deck
    
    def set_hand(self,hand):
        self.__hand = hand

    def set_battle_zone(self,battle_zone):
        self.__battle_zone = battle_zone
    
    def set_land_zone(self,land_zone):
       self.__land_zone = land_zone
    
    def set_graveyard(self,graveyard):
        self.__graveyard = graveyard

    def set_exile(self,exile):
       self.__exile = exile