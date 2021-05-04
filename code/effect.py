
class Effect:
	
	def __init__(self,name):
		self.__name	= name
		
	@staticmethod
	def deathtouch(Card):
		Card.set_life(-999999)
	
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
	
	def haste(self,Card):
		Card._issummoning_sickness = True
	
	# def hexproof(self):
	# 	pass
	
	# def indestructible(self):
	# 	pass
	
	def lifelink(self,Player,Card):
	 	Player.set_life(Player.get_life()+Card.get_damage())
	
	# def menace(self):
	# 	pass
	
	# def protection(self):
	# 	pass
	
	# def reach(self):
	# 	pass
	
	def trample(self,Player_target,Card_attk,Card_def):
		res = Card_attk.get_damage() - Card_def.get_life()
		if res >=0:
			Player_target.set_life(Playet_target.get_life()-res)

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