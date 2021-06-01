
class Activable:
	
	############################ constructeur ############################
	def __init__(self,name,cost_quantity):
		self.__name = name
		self.__cost_quantity = cost_quantity
		

	############################ GETTERS ############################
    def get_name(self):
        return self.__name

	def get_cost_quantity(self):
		return self.cost_quantity

	############################ Methodes ############################

	def isActivable(self,player):
		if __name = "mana"
			#verif si on a assez de mana disponible
			player.get_mana_pool()[]
			return True
		elif __name = "creature"
			#verifier si on a assez de creature disponible 
			if len(player.get_board().get_battle_zone()) >= self.__cost_quantity	
				return True		
		return False 
	