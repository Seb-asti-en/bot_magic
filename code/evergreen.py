
class Evergreen:

	def __init__(self,name):
		self.__permanent_evergreen = name
		self.__tmp_evergreen = []

		
	def get_permanent_evergreen(self):
		return self.__permanent_evergreen

	def get_tmp_evergreen(self):
		return self.__tmp_evergreen

	def clear_tmp(self):
		self.__tmp_evergreen.clear()

	def append_tmp_evergreen(self,evergreen):
		self.__tmp_evergreen.append(evergreen)

    ##
	# Attaque deux fois, une fois en même temps que les Créatures First strike 
	#		et une fois avec toute les autres Créatures
	# @param Card_target carte ciblé
	# @param Card_source carte utilisé
	##
	def double_strike(self,Card_target,Card_source):
		#la carte ciblé se prend le coup
		Card_target.set_life(Card_target.get_life() - Card_source.get_damage())

		if  Card_target.get_life() >= 0:
			#la carte source se prend le coup
			Card_source.set_life(Card_source.get_life() - Card_target.get_damage())
			#la carte target se prend le coup
			Card_target.set_life(Card_target.get_life() - Card_source.get_damage())

	##
	# Ajoute une phase d'attaque avant celle des autre autrement dit,
	#		attaque avant les autres créature qui n'ont pas first strike
	# @param Card_target carte ciblé
	# @param Card_source carte utilisé
	##
	def first_strike(self,Card_target,Card_source):
		#la carte ciblé se prend le coup
		Card_target.set_life(Card_target.get_life() - Card_source.get_damage())

		if  Card_target.get_life() >= 0:
			#la carte source se prend le coup
			Card_source.set_life(Card_source.get_life() - Card_target.get_damage())

	##
	# fait les effets avant la blessure
	# @param Card_target Card ciblé
	# @param Card_source carte utiliser
	# @return retourne TRUE si un effet est utilisé sinon return FALSE
	##
	@staticmethod
	def early_battle_phase(Card_target,Card_source):
		b = False		
		
		if "double" in Card_source.get_evergreen().get_list_effects():
			Card_source.get_evergreen().double_strike(Card_target,Card_source)
			b = True
		elif "first" in Card_source.get_evergreen().get_list_effects():
			Card_source.get_evergreen().first_strike(Card_target,Card_source)
			b = True

		return b

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
	# @param Card_source carte utiliser
	##
	@staticmethod
	def end_battle_phase(Player_target, Card_target,Player_source,Card_source):		
		#effects carte Source
		if "lifelink" in Card_source.get_evergreen().get_list_effects():
			Card_source.get_evergreen().lifelink(Player_source,Card_source)
		if "trample" in Card_source.get_evergreen().get_list_effects():
			Card_source.get_evergreen().trample(Player_target,Card_target)
		if "deathtouch" in Card_source.get_evergreen().get_list_effects():
			Card_source.get_evergreen().deathtouch(Card_target)

		#effects carte Target
		if "lifelink" in Card_target.get_evergreen().get_list_effects():
			Card_target.get_evergreen().lifelink(Player_target,Card_target)
		if "deathtouch" in Card_target.get_evergreen().get_list_effects():
			Card_target.get_evergreen().deathtouch(Card_source)

	##
	# Ne possède pas de mal d'invocation 
	# @param Card_target carte ciblé
	##	
	def haste(Card):
		Card._issummoning_sickness = False



	##
	# verifie les effets avant le choix  d'attaque
	# @param Card_source carte utilisé
	# @return True si on peut attaquer sinon FALSE
	##
	@staticmethod
	def early_choice_attack(Card_source):
		b = True

		if "hast" in Card_source.get_evergreen().get_list_effects():
			Card_source.get_evergreen().haste(Card_source)			

		if "defender" in Card_source.get_evergreen().get_list_effects():
			b = False
		
		return b

	##
	# permet de savoir si la creature source  a vol ou non
	# @param Card_source carte Utiliser
	# @return True si la creature vol
	##
	def flying(self,Card_source):
		b = False
		if "flying" in Card_source.get_evergreen().get_list_effects():
			b = True
		return b

	##
	# permet de savoir si la creature source a reach ou non
	# @param Card_source carte Utiliser
	# @return True si la creature a reach
	##
	def reach(self,Card_source):
		b = False
		if "reach" in Card_source.get_evergreen().get_list_effects():
			b = True
		return b

	##
	# Une carte avec Skulk ne peut être bloquée que par une carte avec une puissance supérieure à la sien
	# @param Card_target carte  ciblé
	# @param Card_source carte Utilisé
	# @return True si on peut bloquer
	##
	def skulk(self,Card_target,Card_source):
		b = False
		if Card_target.get_damage() < Card_source.get_damage():
			b = True
		return b

	##
	# verifie les effets avant le choix  de blockage
	# @param Card_target carte ciblé
	# @param Card_source carte Utilisé
	# @return True si on peut blocker sinon FALSE
	##
	@staticmethod	
	def early_choice_block(Card_target,Card_source):
		b = True		
		if "flying" in Card_target.get_evergreen().get_list_effects():
			b = (Card_source.get_evergreen().flying(Card_source) or Card_source.get_evergreen().reach(Card_source))
				
		if "skulk"  in Card_target.get_evergreen().get_list_effects():
			b = Card_source.get_evergreen().skulk(Card_target,Card_source)

		return b




	# def flash(self):
	# 	pass

	# def indestructible(self):
	# 	pass

	# def hexproof(self):
	# 	pass

	##
	#TODO: faire l'engagement
	# Attaquer ne fait pas s'engager une Créature avec Vigilance
	# @param Card_target carte ciblé
	##
	def vigilance(self,Card_target):
		Card_target._isengaged = False	

	# def menace(self):
	# 	pass

	# def protection(self):
	# 	pass

	#faire une verif a chaque sort
	# def prowess(self,Card):
	# 	Card.buf_damage(1)
	# 	Card.buf_life(1)
	# 	Card._tmp_end_Game_life += 1
	# 	Card._tmp_end_Game_damage += 1	

