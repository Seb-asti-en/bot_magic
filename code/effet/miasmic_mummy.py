from effect import Effect

class MiasmicMummy(Effect):

  def __init__(self,name,target,temporality):
    super().__init__(name,target,temporality)


  def effect(self, players, indices):

  	for i in range(len(players)):

  		players[i].move("HAND",indices[i],"GRAVEYARD")

    # for player in all_player:
    #   player.move("HAND", i, "GRAVEYARD")