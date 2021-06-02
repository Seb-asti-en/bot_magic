
class Activable:

	############################ constructeur ############################
	def __init__(self,activable):
		self.__dico_cost = self.init_dico(activable)

	############################ GETTERS ############################

	def get_cost(self):
		return self.__dico_cost

	############################ Methodes ############################

	##
	# Initialise le dicotionaire de cout
	##
	def init_dico(self, activable):
		dico = {}
		if len(activable["Cost_name"]) == len(activable["Cost_quantity"]):
			for i in range(len(activable["Cost_name"])):
				dico[ activable["Cost_name"][i] ] = activable["Cost_quantity"][i]
		return dico
