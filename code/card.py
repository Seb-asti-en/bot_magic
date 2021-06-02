############################ Import ############################
from effet.blight_keeper import BlightKeeper
from effet.bloodlust_inciter import BloodlustInciter
from effet.blossom_dryad import BlossomDryad
from effet.by_force import ByForce
from effet.cancel import Cancel
from effet.charging_monstrosaur import ChargingMonstrosaur
from effet.crash_the_ramparts import CrashTheRamparts
from effet.crushing_canopy import CrushingCanopy
from effet.cycling import Cycling
from effet.demolish import Demolish
from effet.demystify import Demystify
from effet.desperate_castaways import DesperateCastaways
from effet.dual_shot import DualShot
from effet.electrify import Electrify
from effet.essence_scatter import EssenceScatter
from effet.fan_bearer import FanBearer
from effet.galestrike import Galestrike
from effet.impeccable_timing import ImpeccableTiming
from effet.jungle_delver import JungleDelver
from effet.legions_judgment import LegionsJudgment
from effet.lightning_strike import LightningStrike
from effet.march_of_the_drowned import MarchOfTheDrowned
from effet.mark_of_the_vampire import MarkOfTheVampire
from effet.miasmic_mummy import MiasmicMummy
from effet.mighty_leap import MightyLeap
from effet.minotaur_sureshot import MinotaurSureshot
from effet.one_with_the_wind import OneWithTheWind
from effet.painful_lesson import PainfulLesson
from effet.pious_interdiction import PiousInterdiction
from effet.pull_from_tomorrow import PullFromTomorrow
from effet.ritual_of_rejuvenation import RitualOfRejuvenation
from effet.rummaging_goblin import RummagingGoblin
from effet.run_aground import RunAground
from effet.skittering_heartstopper import SkitteringHeartstopper
from effet.slash_of_talons import SlashOfTalons
from effet.slice_in_twain import SliceInTwain
from effet.sparring_mummy import SparringMummy
from effet.splendid_agony import SplendidAgony
from effet.sure_strike import SureStrike
from effet.spreading_rot import SpreadingRot
from effet.unfriendly_fire import UnfriendlyFire
from effet.vanquish_the_weak import VanquishTheWeak
from effet.verdant_suns_avatar import VerdantSunsAvatar
from effet.walk_the_plank import WalkThePlank
from effet.draw_card  import DrawCard



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
		self._effect		= self.init_effect(card)


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

	############################ Setters ############################

	def set_id(self, id):
		self._id = id

	def set_name(self, name):
		self._name = name

	def set_supertype(self, supertype):
		self._supertype = supertype

	def set_type(self, types):
		self._type = types

	def set_subtype(self, subtype):
		self._subtype = subtype

	############################ Méthode ############################

	##
	# Fonction qui accorde au effet la bonne classe fille
	# @param	effet	L'effet qui doit etre convertie
	# @return	retour	La classe fille ainsi créer
	##
	def parse(self, effet):
		retour = None

		if effet["Name"] == "blight_keeper":
			retour = BlightKeeper(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "draw_card":
			retour = DrawCard(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"], effet["Nb_draw_card"])

		elif effet["Name"] == "bloodlust_inciter":
			retour = BloodlustInciter(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "blossom_dryad":
			retour = BlossomDryad(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "by_force":
			retour = ByForce(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "cancel":
			retour = Cancel(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "charging_monstosaur":
			retour = ChargingMonstrosaur(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "cash_the_ramparts":
			retour = CrashTheRamparts(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "crushing_canopy":
			retour = CrushingCanopy(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "cycling":
			retour = Cycling(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"], effet["Nb_draw_card"])

		elif effet["Name"] == "demolish":
			retour = Demolish(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "demystify":
			retour = Demystify(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "desperate_castaway":
			retour = DesperateCastaways(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "dual_shot":
			retour = DualShot(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "electrify":
			retour = Electrify(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "essence_scatter":
			retour = EssenceScatter(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "fan_bearer":
			retour = FanBearer(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "galestrike":
			retour = Galestrike(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "impeccable_timing":
			retour = ImpeccableTiming(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "jungle_delver":
			retour = JungleDelver(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "legions_judgment":
			retour = LegionsJudgment(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "lightning_strike":
			retour = LightningStrike(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "march_of_the_drowned":
			retour = MarchOfTheDrowned(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "mark_of_the_vampire":
			retour = MarkOfTheVampire(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "miasmic_mummy":
			retour = MiasmicMummy(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "mighty_leap":
			retour = MightyLeap(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "minotaur_sureshot":
			retour = MinotaurSureshot(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "one_with_the_wind":
			retour = OneWithTheWind(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "painful_lesson":
			retour = PainfulLesson(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "pious_interdiction":
			retour = PiousInterdiction(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "pull_from_tomorrow":
			retour = PullFromTomorrow(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "ritual_of_rejuvenation":
			retour = RitualOfRejuvenation(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "rummaging_goblin":
			retour = RummagingGoblin(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "run_aground":
			retour = RunAground(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "skittering_heartstopper":
			retour = SkitteringHeartstopper(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "slash_of_talons":
			retour = SlashOfTalons(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "slice_in_twain":
			retour = SliceInTwain(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "sparring_mummy":
			retour = SparringMummy(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "splendid_agony":
			retour = SplendidAgony(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "sure_strike":
			retour = SureStrike(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "spreading_rot":
			retour = SpreadingRot(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "unfriendly_fire":
			retour = UnfriendlyFire(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "vanquish_the_weak":
			retour = VanquishTheWeak(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "verdant_suns_avatar":
			retour = VerdantSunsAvatar(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		elif effet["Name"] == "walk_the_plank":
			retour = WalkThePlank(effet["Name"], effet["Target"], effet["Temporality"], effet["Activable"])

		return retour


	##
	# Initialise le cout en mana d'une carte
	# @param 	card 	la carte qu'il faut initialiser
	##
	def init_mana_cost(self, card):
		self._mana_cost = {}
		temp = card["Mana_cost"]
		if(temp != ''):
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
		self._colors = []
		temp = card["Colors"]
		res = temp.split(';')
		for x in res:
			if(x == ''):
				self._colors.append('C')
			else:
				self._colors.append(x)
		return self._colors

	##
	# Initialise l'identitée d'une carte
	# @param card 	la carte qu'il faut initialiser
	##
	def init_identity(self, card):
		self._identity = []
		temp = card["Identity"]
		res = temp.split(';')
		for x in res:
			if(x == ''):
				self._identity.append['C']
			else:
				self._identity.append(x)
		return self._identity

	##
	# Récupère les effets evergreen d'une carte par rapport a son texte
	# @param card 	la carte qu'il faut analyser
	##
	def init_effect(self, card):
		self._effect = []
		for effets in card["Effect"]:
			self._effect.append(self.parse(effets))
		return self._effect

class EnchantmentCard(Card):

	def __init__(self, card):
		super().__init__(card)
