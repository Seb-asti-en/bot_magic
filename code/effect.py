
class Effect:
	
	############################ constructeur ############################
	def __init__(self,list_effects):
		self.__list_effects	= list_effects
	

	############################ Getter ############################
	def get_list_effects(self):
		return self.__list_effects


	############################ Methodes ############################

	##
	# Envoi une Créature au cimetière qu’importe l’endurance de la créature
	# @param Card_target carte ciblé
	##
	def deathtouch(self,Card_target):
		Card_target.set_life(-999999)
	
	##
	# Octroie un montant de point vie égal au dégâts infliger
	# @param Player_source joueur incarné
	# @param Card la carte source
	##
	def lifelink(self,Player_source, Card_source):
	 	Player_source.set_life(Player_source.get_life()+Card_source.get_damage())

	##
	# Le surplu de dégâts est infligé au joueur directement
	# @param Player_target le joueur ciblé
	# @param Card_target la carte ciblé
	##
	def trample(self,Player_target,Card_target):
		if Card_target.get_life() <0:
			Player_target.set_life(Player_target.get_life() + Card_target.get_life())

	##
	# fait les effets apres la blessure
	# @param Player_target Player ciblé
	# @param Card_target Card ciblé
	# @param Player_source Player incarné
	# @param Card_source carte incarné
	##
	@staticmethod
	def end_battle_phase(Player_target, Card_target,Player_source,Card_source):		
		#effects carte Source
		if "lifelink" in Card_source.get_effect().get_list_effects():
			Card_source.get_effect().lifelink(Player_source,Card_source)
		if "trample" in Card_source.get_effect().get_list_effects():
			Card_source.get_effect().trample(Player_target,Card_target)
		if "deathtouch" in Card_source.get_effect().get_list_effects():
			Card_source.get_effect().deathtouch(Card_target)

		#effects carte Target
		if "lifelink" in Card_target.get_effect().get_list_effects():
			Card_target.get_effect().lifelink(Player_target,Card_target)
		if "deathtouch" in Card_target.get_effect().get_list_effects():
			Card_target.get_effect().deathtouch(Card_source)

	##
	# Attaquer ne fait pas s'engager une Créature avec Vigilance
	# @param Card_target carte ciblé
	##
	def vigilance(self,Card_target):
		Card_target._isengaged = False	
	
	##
	# Ne possède pas de mal d'invocation 
	# @param Card_target carte ciblé
	##	
	def haste(Card):
		Card._issummoning_sickness = True

	# def defender(self):
	# 	pass
	
	# def double_strike(self):
	# 	pass
	
	# def first_strike(self):
	# 	pass
	
	# def flash(self):
	# 	pass
	
	# def flying(self):
	# 	pass
	
	
	# def hexproof(self):
	# 	pass
	
	# def indestructible(self):
	# 	pass

	# def menace(self):
	# 	pass
	
	# def protection(self):
	# 	pass
	
	# def reach(self):
	# 	pass
	


	
	#faire une verif a chaque sort
	# def prowess(self,Card):
	# 	Card.buf_damage(1)
	# 	Card.buf_life(1)
	# 	Card._tmp_end_Game_life += 1
	# 	Card._tmp_end_Game_damage += 1	

	# def skulk(self):
	# 	pass