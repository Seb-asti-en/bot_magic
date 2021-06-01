
class Effect:

	############################ constructeur ############################
	def __init__(self,name,target,temporality):
		self.__name = name
		self.__target = target
		#self.__activable = Activable("lirejson","lirejson")
		#self.__nb_target = nb_target
		self.__temporality = temporality



	############################ Getter ############################
	def get_name(self):
		return self.__name

	def get_target(self):
		return self.__target

	def get_cost(self):
		return self.__cost

	def get_temporality(self):
		return self.__temporality

	def get_description(self):
		return self.__description

	def get_activable(self):
		return self.__activable

