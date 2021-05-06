############################ Import ############################
import re
import effect_enum as enum
from effect import Effect


class Card:

	############################ Constructeur ############################
	def __init__(self, card):

		self._id			= card["Id"]
		self._name			= card["Name"]
		self._supertype		= card["Supertype"]
		self._type 			= card["Type"]
		self._subtype		= card["Subtype"]
		self._mana_cost 	= self.init_mana_cost(card)
		self._colors		= self.init_colors(card)
		self._identity		= self.init_identity(card)
		self._text			= card["Text"]
		self._effect		= Effect(self.init_effect(card))
		self._collection 	= ""
		self._isengaged 	= False
		self._istarget		= False
		
		self._isblocked 	= False
		self._isattack 		= False
		self._issummoning_sickness = False
# =============================================================================
# 		self._tmp_end_Game_life = 0
# 		self._tmp_end_Game_damage = 0
# =============================================================================
		
		
	############################ Getters ############################
	def get_id(self):
		return self._id
		
	def get_name(self):
		return self._name

	def get_supertype(self):
		return self._supertype

	def get_type(self):
		return self._type

	def get_subtype(self):
		return self._subtype
	
	def get_mana_cost(self):
		return self._mana_cost
	
	def get_colors(self):
		return self._colors

	def get_identity(self):
		return self._identity
	
	def get_text(self):
		return self._text

	def get_effect(self):
		return self._effect

	def get_isblocked(self):
		return self._isblocked

	def get_isattack(self):
		return self._isattack 

	def get_isengaged(self):
		return self._isengaged 
	
	def get_istarget(self):
		return self._istarget


	############################ Setters ############################
	def set_id(self, ids):
		self._id = ids
	
	def set_name(self, name):
		self._name = name

	def set_supertype(self, supertype):
		self._supertype = supertype
	
	def set_type(self, types):
		self._type = types
	
	def set_subtype(self, subtype):
		self._subtype = subtype

	def set_isattack(self,bool):
		self._isattack = bool

	def set_isblocked(self,bool):
		self._isblocked = bool
	
	def set_isengaged(self,bool):
		self._isengaged = bool

	def set_istarget(self,bool):
		self._istarget = bool


	############################ Méthode ############################
	##
	# Reset les valeurs possiblement changer des booleen a false
	##
	def reset_bool(self):
		self._isblocked 	= False
		self._isattack 		= False
		self._isengaged 	= False
		self._istarget		= False	

	##
	# Initialise le cout en mana d'une carte
	# @param card 	la carte qu'il faut initialiser
	##
	def init_mana_cost(self, card):
		self._mana_cost = {'X' : 0,'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		temp = card["Mana_cost"]
		res = temp.strip('}{').split('}{')
		if(res[0].isnumeric()):
			self._mana_cost['X'] = int(res[0])
			res.remove(res[0])
		for x in res:
			try:
				self._mana_cost[x] = self._mana_cost[x] + 1
			except:
				self._mana_cost[x] = 1
		return self._mana_cost
	
	##
	# Initialise la couleur d'une carte
	# @param card 	la carte qu'il faut initialiser
	##
	def init_colors(self, card):
		self._colors = {'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		temp = card["Colors"]
		res = temp.split(';')
		for x in res:
			if(x == ''):	
				self._colors['C'] = 1
			else:
				self._colors[x] = 1
		return self._colors
	
	##
	# Initialise l'identitée d'une carte
	# @param card 	la carte qu'il faut initialiser
	##
	def init_identity(self, card):
		self._identity = {'C' : 0, 'W' : 0, 'B' : 0, 'R' : 0, 'G' : 0, 'U' : 0}
		temp = card["Identity"]
		res = temp.split(';')
		for x in res:
			if(x == ''):	
				self._identity['C'] = 1
			else:
				self._identity[x] = 1
		return self._identity

	##
	# Récupère les effets evergreen d'une carte par rapport a son texte
	# @param card 	la carte qu'il faut analyser
	##
	def init_effect(self, card):
		effects = []
		effect_tampon = []
		for i in enum.Effect:
			effect_tampon.append(i.name)
		temp = re.split('\n| strike|, | \(', card["Text"])
		for eff in temp:
			if eff.lower() in effect_tampon:
				effects.append(eff.lower())
		return effects
		
	##
	# Méthode qui retourne l'affichage d'une carte
	##
	def to_string(self):

		string = ""
		
		string += "CARD TYPE : " + str(self._type) + " \n" 
		string += "ID : " + str(self._id) + " \n" 
		string += "COLLECTION : " + str(self._collection) + "\n"
		string += "NAME : " + self._name + "\n"
		if(self._supertype != None):
			string += "SUPERTYPE : " + self._supertype + "\n"
		if(self._subtype != None):
			string += "SUBTYPE : " + str(self._subtype) + "\n"
		
		string += "COLOR : "
		if (self._colors['C'] == 1):
			string += "Incolore"
		else :
			if (self._colors['W'] == 1):
				string += "Blanc "
			
			if (self._colors['R'] == 1):
				string += "Rouge "
			
			if (self._colors['G'] == 1):
				string += "Vert "
			
			if (self._colors['U'] == 1):
				string += "Bleu "
			
			if (self._colors['B'] == 1):
				string += "Noir"

		string += "\n"
		
		string += "MANA COST : "
		if (self._mana_cost['X'] > 0):
			string += str(self._mana_cost['X']) + "(Mana) "
			
		if (self._mana_cost['C'] > 0):
			string += str(self._mana_cost['C']) + "(Incolore) "

		if (self._mana_cost['W'] > 0):
			string += str(self._mana_cost['W']) + "(Blanc) "

		if (self._mana_cost['R'] > 0):
			string += str(self._mana_cost['R']) + "(Rouge) "

		if (self._mana_cost['G'] > 0):
			string += str(self._mana_cost['G']) + "(Vert) "

		if (self._mana_cost['U'] > 0):
			string += str(self._mana_cost['U']) + "(Bleu) "

		if (self._mana_cost['B'] > 0):
			string += str(self._mana_cost['B']) + "(Noir)"
		
		string += "\n"
		
		
		string += "IDENTITY : "
		if (self._identity['C'] == 1):
			string += "Incolore"
		else :
			if (self._identity['W'] == 1):
				string += "Blanc "
			
			if (self._identity['R'] == 1):
				string += "Rouge "
			
			if (self._identity['G'] == 1):
				string += "Vert "
			
			if (self._identity['U'] == 1):
				string += "Bleu "
			
			if (self._identity['B'] == 1):
				string += "Noir"

		string += "\n"
		
		if(self._text != None):
			string += "TEXT : " + self._text + "\n"
		if(self._effects != []):
			string += "EFFECT : " + str(self._effects) + "\n"
			
		return string

class EnchantmentCard(Card):

	def __init__(self, card):
		super().__init__(card)
	
	def to_string(self):
		string = super().to_string()
		return string