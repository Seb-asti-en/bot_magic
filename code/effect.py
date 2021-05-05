
class Effect:
	
	def __init__(self,list_effects):
		self.__list_effects	= list_effects
	


	def get_list_effects(self):
		return self.__list_effects


	def deathtouch(player_target, Card_target,Player_source, Card_def):
		Card_target.set_life(-999999)
	

	def end_battle_phase(effect,Player_target, Card_target,Player_source,card_def):
		switcher = {
			"deathtouch": deathtouch,
			# "lifelink": lifelink,
			# "trample": trample
		}
		# Get the function from switcher dictionary
		func = switcher.get(effect, lambda player_target, Card_target,Player_source, card_def: "Invalid effect")
		# Execute the function
		func(player_target, Card_target,Player_source, Card_def)



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
	
	def haste(Card):
		Card._issummoning_sickness = True
	
	# def hexproof(self):
	# 	pass
	
	# def indestructible(self):
	# 	pass
	
	def lifelink(player_target, Card_target,Player_source, Card_def):
	 	Player_source.set_life(Player_source.get_life()+Card_def.get_damage())
	
	# def menace(self):
	# 	pass
	
	# def protection(self):
	# 	pass
	
	# def reach(self):
	# 	pass
	
	def trample(player_target, Card_target,Player_source, Card_def):
		res = Card_attk.get_damage() - tmp_ennemi_life
		if res >=0:
			Player_target.set_life(Player_target.get_life() - res)

	def vigilance(self,Card):
		Card._isengaged = False
	
	#faire une verif a chaque sort
	# def prowess(self,Card):
	# 	Card.buf_damage(1)
	# 	Card.buf_life(1)
	# 	Card._tmp_end_Game_life += 1
	# 	Card._tmp_end_Game_damage += 1	

	# def skulk(self):
	# 	pass