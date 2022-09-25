import pygame
from constant import *
from objects import *

import enum

# Fuentes
ATWRITER_20=pygame.font.Font('resources/fonts/atwriter.ttf',20)
SHERWOOD_15=pygame.font.Font('resources/fonts/SHERWOOD.TTF',15)
SHERWOOD_20=pygame.font.Font('resources/fonts/SHERWOOD.TTF',20)
CALIBRI_40=pygame.font.SysFont("Calibri", 40)
CALIBRI_20=pygame.font.SysFont("Calibri", 20)
CALIBRI_15=pygame.font.SysFont("Calibri", 15)
CALIBRI_10=pygame.font.SysFont("Calibri", 10)
IMPACT_15=pygame.font.SysFont("Impact", 15)
COMIC_40=pygame.font.SysFont("Monaco",40)
COMIC_30=pygame.font.SysFont("Monaco",30)
COMIC_20=pygame.font.SysFont("Monaco",20)

ENERGY='energy'

PYKEYS={
	'0':pygame.K_0,'1':pygame.K_1,'2':pygame.K_2,'3':pygame.K_3,'4':pygame.K_4,'5':pygame.K_5,'6':pygame.K_6,'7':pygame.K_7,'8':pygame.K_8,'9':pygame.K_9,
	'w':pygame.K_w,'s':pygame.K_s,'a':pygame.K_a,'d':pygame.K_d,
	'UP':pygame.K_UP,'DOWN':pygame.K_DOWN,'LEFT':pygame.K_LEFT,'RIGHT':pygame.K_RIGHT,
	'q':pygame.K_q,'i':pygame.K_i,'r':pygame.K_r,'e':pygame.K_e,'g':pygame.K_g,'m':pygame.K_m,'n':pygame.K_n,'o':pygame.K_o,'p':pygame.K_p,'z':pygame.K_z,
	'ESC':pygame.K_ESCAPE,'SPACE':pygame.K_SPACE,'RSHIFT':pygame.K_RSHIFT,'LSHIFT':pygame.K_LSHIFT,
}

ENEMY_PLAYERS=[TypeObjects.ZOMBIES.name,TypeObjects.OBJECTS.name]
ENEMY_ZOMBIES=[TypeObjects.PLAYERS.name,TypeObjects.BUILDINGS.name]

PLAYERS = {
	0:{
		'image':'player0', # Imagen
		'hand':'hand0', # Imagen manos
		'speed':360/FRAMES, # Velocidad
		'life':2000, # Vida máxima
		'shield':2000, # Escudo máximo
		'hurt':4, # Daño
		'enemy':ENEMY_PLAYERS, # Enemigos
		ENERGY:100,
		'sound_kill':None, # Sonido al morir
		'sound_wound':None, # Sonido al ser herido
	},
	1:{
		'image':'player1',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	2:{
		'image':'player2',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	3:{
		'image':'player3',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	4:{
		'image':'player4',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	5:{
		'image':'player5',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	6:{
		'image':'player6',
		'hand':'hand1',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	7:{
		'image':'player7',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	8:{
		'image':'player8',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
	9:{
		'image':'player9',
		'hand':'hand0',
		'speed':360/FRAMES,
		'life':2000,
		'shield':2000,
		'hurt':4,
		'enemy':ENEMY_PLAYERS,
		ENERGY:100,
		'sound_kill':None,
		'sound_wound':None,
	},
}

ZOMBIES ={
	0:{
		'image':'zombie0', # Imagen
		'hand':'hand2', # Imagen manos
		'speed':180/FRAMES, # Velocidad media
		'life':800, # Vida máxima
		'shield':500, # Escudo máximo
		'hurt':3, # Daño
		'enemy':ENEMY_ZOMBIES, # Enemigos
		ENERGY:100,
		'radius_search':1000, # Radio de busqueda
		'radius_shot':350, # Distancia de disparo
		'probability_armory':(0.4,0.2,0.1), # Probabilidad de tener un arma al inicio
		'sound_kill':None, # Sonido al morir
		'sound_wound':'wound1', # Sonido al ser herido
	},
	1:{
		'image':'zombie1',
		'hand':'hand3',
		'speed':240/FRAMES,
		'life':1200,
		'shield':700,
		'hurt':5,
		'enemy':ENEMY_ZOMBIES,
		ENERGY:100,
		'radius_search':1200,
		'radius_shot':370,
		'probability_armory':(0.4,0.2,0.1),
		'sound_kill':None,
		'sound_wound':'wound1',
	},
}

FIELDS = {
	0:{'image':'field0','dim':(WIDTH_FIELD,HEIGHT_FIELD)}
}

NATURE = {
	'stone0':{
		'image':'stone0',
		'dim':(150,150),
		'life':2000,
		'materials':{'wood':0,'stone':5},
		'sound_wound':'shot_stone0',
	},
	'stone1':{
		'image':'stone1',
		'dim':(80,80),
		'life':1000,
		'materials':{'wood':0,'stone':2},
		'sound_wound':'shot_stone0',
	},
	'tree1':{
		'image':'tree1',
		'dim':(250,250),
		'life':1500,
		'materials':{'wood':5,'stone':0},
		'sound_wound':'shot_wood0',
	},
	'tree2':{
		'image':'tree2',
		'dim':(150,150),
		'life':1000,
		'materials':{'wood':3,'stone':0},
		'sound_wound':'shot_wood0',
	},
}

BOXES = {
	0:{
		'image':'box0',
		'life':800,
		'reward_armory':0,
		'reward_bullets':2,
		'reward_materials':1,
		'sound_wound':'shot_wood0',
	},
	1:{
		'image':'box1',
		'life':900,
		'reward_armory':1,
		'reward_bullets':2,
		'reward_materials':1,
		'sound_wound':'shot_wood0',
	},
	2:{
		'image':'box2',
		'life':1000,
		'reward_armory':2,
		'reward_bullets':2,
		'reward_materials':2,
		'sound_wound':'shot_wood0',
	},
	3:{
		'image':'box3',
		'life':1200,
		'reward_armory':2,
		'reward_bullets':4,
		'reward_materials':2,
		'sound_wound':'shot_wood0',
	},
	4:{
		'image':'box4',
		'life':1400,
		'reward_armory':2,
		'reward_bullets':4,
		'reward_materials':4,
		'sound_wound':'shot_wood0',
	},
	5:{
		'image':'box5',
		'life':1800,
		'reward_armory':3,
		'reward_bullets':5,
		'reward_materials':4,
		'sound_wound':'shot_wood0',
	},
	6:{
		'image':'box6',
		'life':1400,
		'reward_armory':4,
		'reward_bullets':5,
		'reward_materials':7,
		'sound_wound':'shot_wood0',
	},
}

BUILDINGS = {
	'townhall':{
		'building':{
			'image':'townhall0',
			'dim':(300,300),
			'function':'townhall',
			'life':6000,
			'sound_wound':None,
		},
		'townhall':{},
	},
	'trunk':{
		'building':{
			'image':'trunk',
			'dim':(100,100),
			'function':'trunk',
			'life':2000,
			'sound_wound':'shot_wood0',
		},
		'trunk':{},
	},
}

ARMORY = {
	'hands':{
		'item': {
			'item':False,
			'lot':0,
			'max_lot':None,
			'icon_item':'icon_hands',
			'proportion_item':(80,80),
			'direction_item':0,
			'color_item':'black',
		},
		'armory':{
			'function':'fists',
			'capacity':None,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-40,20),
			'sound_action':'hands_action3',
			'sound_select_on':None,
			'sound_select_off':None,
		},
		'fists':{
			'left_hand_animation_action':((50,19,-20),(30,40,-20),(30,40,-20)),
			'right_hand_animation_action':((30,-40,20),(30,-40,20),(50,-10,20)),
			'animation_action':(7,7,7),
		},
	},
	'hands1':{
		'item': {
			'item':False,
			'lot':0,
			'max_lot':None,
			'icon_item':'icon_hands',
			'proportion_item':(80,80),
			'direction_item':0,
			'color_item':'black',
		},
		'armory':{
			'function':'fists',
			'capacity':None,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-40,20),
			'sound_action':'hands_action2',
			'sound_select_on':None,
			'sound_select_off':None,
		},
		'fists':{
			'left_hand_animation_action':((30,40,-20),(45,20,-20),(40,40,-20)),
			'right_hand_animation_action':((30,-40,20),(45,-20,20),(40,-40,20)),
			'animation_action':(7,7,7),
		},
	},
	# Drug
	'potion_bottle':{
		'item': {
			'item':True,
			'lot':4,
			'max_lot':10,
			'icon_item':'potion_bottle',
			'proportion_item':(35,60),
			'direction_item':0,
			'color_item':'purple',
		},
		'armory':{
			'function':'drug',
			'capacity':10,
			'left_hand_status':(30,22,-20),
			'right_hand_status':(30,-22,80),
			'sound_action':'drink0',
			'sound_select_on':'change_potion0',
			'sound_select_off':None,
		},
		'drug':{
			'image':'potion_bottle',
			'dim':(23,40),
			'img_status':(45,0,-70),
			'type':'potion',
			'life_added':400,
			'cure':3*FRAMES,
			'left_hand_animation_action':((30,22,-20),(30,22,-20)),
			'right_hand_animation_action':((30,-22,80),(30,-22,80)),
			'img_animation_action':((30,0,-70),(45,0,-70)),
			'animation_action':(20,20),
			'bubble':'bubble1',
			'sound_cure':'change_potion0',
		},
	},
	'potion_jug':{
		'item': {
			'item':True,
			'lot':2,
			'max_lot':4,
			'icon_item':'potion_jug',
			'proportion_item':(60,60),
			'direction_item':0,
			'color_item':'purple',
		},
		'armory':{
			'function':'drug',
			'capacity':4,
			'left_hand_status':(30,22,-20),
			'right_hand_status':(30,-22,80),
			'sound_action':'drink0',
			'sound_select_on':'change_potion0',
			'sound_select_off':None,
		},
		'drug':{
			'image':'potion_jug',
			'dim':(50,50),
			'img_status':(50,0,-50),
			'type':'potion',
			'life_added':1000,
			'cure':8*FRAMES,
			'left_hand_animation_action':((30,22,-20),(30,22,-20)),
			'right_hand_animation_action':((30,-22,80),(30,-22,80)),
			'img_animation_action':((30,0,-50),(50,0,-50)),
			'animation_action':((20,20)),
			'bubble':'bubble1',
			'sound_cure':'change_potion0',
		},
	},
	'bandages':{
		'item': {
			'item':True,
			'lot':4,
			'max_lot':10,
			'icon_item':'bandages',
			'proportion_item':(75,75),
			'direction_item':45,
			'color_item':'purple',
		},
		'armory':{
			'function':'drug',
			'capacity':10,
			'left_hand_status':(30,22,-20),
			'right_hand_status':(30,-22,80),
			'sound_action':'bandage0',
			'sound_select_on':None,
			'sound_select_off':None,
		},
		'drug':{
			'image':'bandages',
			'dim':(45,24),
			'img_status':(40,0,-50),
			'type':'drug',

			'life_added':400,
			'cure':3*FRAMES,
			'left_hand_animation_action':((30,22,-20),(30,22,-20)),
			'right_hand_animation_action':((30,-22,80),(30,-22,80)),
			'img_animation_action':((30,0,-50),(40,0,-50)),
			'animation_action':((20,20)),
			'bubble':'bubble0',
			'sound_cure':None,
		},
	},
	# BOMB
	'grenade0': {
		'item': {
			'item':True,
			'lot':5,
			'max_lot':5,
			'icon_item':'grenade0',
			'proportion_item':(70,70),
			'direction_item':-30,
			'color_item':'orange',
		},
		'armory':{
			'function':'bomb',
			'capacity':5,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-30,20),
			'sound_action':'hands_action0',
			'sound_select_on':'change_grenade0',
			'sound_select_off':None,
		},
		'bomb':{
			'image':'grenade0',
			'dim':(33,33),
			'img_status':(40,-20,-60),
			'type':'grenade',
			'cadence':1*FRAMES,
			'counter_explosion':2*FRAMES,
			'radius':100,
			'hurt':20,
		},
	},
	'grenade1': {
		'item': {
			'item':True,
			'lot':5,
			'max_lot':5,
			'icon_item':'grenade1',
			'proportion_item':(70,70),
			'direction_item':-30,
			'color_item':'orange',
		},
		'armory':{
			'function':'bomb',
			'capacity':5,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-30,20),
			'sound_action':'hands_action0',
			'sound_select_on':'change_grenade0',
			'sound_select_off':None,
		},
		'bomb':{
			'image':'grenade1',
			'dim':(33,33),
			'img_status':(40,-20,-60),
			'type':'grenade',
			'cadence':1*FRAMES,
			'counter_explosion':1.8*FRAMES,
			'radius':150,
			'hurt':25,
		},
	},
	'grenade2': {
		'item': {
			'item':True,
			'lot':5,
			'max_lot':5,
			'icon_item':'grenade2',
			'proportion_item':(70,70),
			'direction_item':-30,
			'color_item':'orange',
		},
		'armory':{
			'function':'bomb',
			'capacity':5,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-30,20),
			'sound_action':'hands_action0',
			'sound_select_on':'change_grenade0',
			'sound_select_off':None,
		},
		'bomb':{
			'image':'grenade2',
			'dim':(33,33),
			'img_status':(40,-20,-60),
			'type':'grenade',
			'cadence':1*FRAMES,
			'counter_explosion':1.6*FRAMES,
			'radius':160,
			'hurt':30,
		},
	},
	'grenade3': {
		'item': {
			'item':True,
			'lot':5,
			'max_lot':5,
			'icon_item':'grenade3',
			'proportion_item':(70,70),
			'direction_item':-30,
			'color_item':'orange',
		},
		'armory':{
			'function':'bomb',
			'capacity':5,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-30,20),
			'sound_action':'hands_action0',
			'sound_select_on':'change_grenade0',
			'sound_select_off':None,
		},
		'bomb':{
			'image':'grenade3',
			'dim':(33,33),
			'img_status':(40,-20,-60),
			'type':'grenade',
			'cadence':1*FRAMES,
			'counter_explosion':1.3*FRAMES,
			'radius':170,
			'hurt':40,
		}
	},
	'sticky0': {
		'item': {
			'item':True,
			'lot':5,
			'max_lot':5,
			'icon_item':'sticky0',
			'proportion_item':(70,70),
			'direction_item':45,
			'color_item':'orange',
		},
		'armory':{
			'function':'bomb',
			'capacity':5,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-30,20),
			'sound_action':'hands_action0',
			'sound_select_on':'change_grenade0',
			'sound_select_off':None,
		},
		'bomb':{
			'image':'sticky0',
			'dim':(45,20),
			'img_status':(40,-20,-30),
			'type':'sticky',
			'cadence':1*FRAMES,
			'counter_explosion':10*FRAMES,
			'radius':100,
			'hurt':27,
		},
	},
	'electricGrenade0': {
		'item': {
			'item':True,
			'lot':5,
			'max_lot':5,
			'icon_item':'electricGrenade0',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'orange',
		},
		'armory':{
			'function':'bomb',
			'capacity':5,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-30,20),
			'sound_action':'hands_action0',
			'sound_select_on':'change_grenade0',
			'sound_select_off':None,
		},
		'bomb':{
			'image':'electricGrenade0',
			'dim':(30,30),
			'img_status':(40,-20,-30),
			'type':'electricGrenade',
			'cadence':1*FRAMES,
			'counter_explosion':1.3*FRAMES,
			'radius':170,
			'hurt':60,
			'hurt_ray':10,
			'ray_time':0.1*FRAMES,
			'n_ray':15,
		},
	},
	# MATERIALS
	'wood': {
		'item':{
			'item':True,
			'lot':10,
			'max_lot':64,
			'icon_item':'icon_wood1',
			'proportion_item':(70,35),
			'direction_item':0,
			'color_item':'pinck',
		},
		'armory':{
			'function':'material',
			'capacity':64,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-40,20),
			'sound_action' : None,
			'sound_select_on': None,
			'sound_select_off': None,
		},
		'material':{},
	},
	'stone':{
		'item':{
			'item':True,
			'lot':10,
			'max_lot':64,
			'icon_item':'icon_stone',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'pinck',
		},
		'armory':{
			'function':'material',
			'capacity':64,
			'left_hand_status':(30,40,-20),
			'right_hand_status':(30,-40,20),
			'sound_action' : None,
			'sound_select_on': None,
			'sound_select_off': None,
		},
		'material':{},
	},
	# BUILDINGS
	'trunk':{
		'item':{
			'item':True,
			'lot':2,
			'max_lot':4,
			'icon_item':'trunk',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'blue',
		},
		'armory':{
			'function':'building',
			'capacity':4,
			'left_hand_status':(28,25,-20),
			'right_hand_status':(28,-25,20),
			'sound_action':'hammerBuild',
			'sound_select_on':None,
			'sound_select_off':None,
		},
		'building':{
			'image':'trunk',
			'dim':(40,40),
			'img_status':(35,0,-20),
			'building':'trunk',
		},
	},
	# WEAPON
	'EscopetaAAA': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'EscopetaAAA',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'blue',
		},
		'armory':{
			'function':'weapon',
			'capacity':2,
			'left_hand_status':(60,5,-20),
			'right_hand_status':(30,-10,80),
			'sound_action':'shot_escopeta0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'EscopetaAAA',
			'dim':(100,25),
			'img_status':(70,0,0),
			'type':'escopeta',
			'bullet':'escopeta',
			'cadence':1.1*FRAMES,
			'reload':3*FRAMES,
			'speed_bullet':15,
			'lon_bullet':600,
			'hurt_bullet':35,
			'n_bullets':20,
			'range_bullets':(-20,20),
			'shot_status':(90,0,0),
			'fire':None,
			'fire_dim':None,
			'fire_animation':None,
			'fire_status':None,
			'sound_reload':'reload_escopeta0',
		},
	},
	'EscopetaJTJ': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'EscopetaJTJ',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'blue',
		},
		'armory':{
			'function':'weapon',
			'capacity':4,
			'left_hand_status':(70,5,-20),
			'right_hand_status':(40,-10,80),
			'sound_action' : 'shot_escopeta0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'EscopetaJTJ',
			'dim':(95,18),
			'img_status':(70,0,0),
			'type':'escopeta',
			'bullet':'escopeta',
			'cadence':1.7*FRAMES,
			'reload':4*FRAMES,
			'speed_bullet':15,
			'lon_bullet':650,
			'hurt_bullet':45,
			'n_bullets':20,
			'range_bullets':(-20,20),
			'shot_status':(90,0,0),
			'fire':None,
			'fire_dim':None,
			'fire_animation':None,
			'fire_status':None,
			'sound_reload':'reload_escopeta0',
		},
	},
	'SubfusilRRX': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'SubfusilRRX',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'green',
		},
		'armory':{
			'function':'weapon',
			'capacity':15,
			'left_hand_status':(65,5,-20),
			'right_hand_status':(40,-10,80),
			'sound_action' : 'shot_subfusil0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'SubfusilRRX',
			'dim':(75,20),
			'img_status':(65,0,0),
			'type':'subfusil',
			'bullet':'subfusil',
			'cadence':0.3*FRAMES,
			'reload':1.7*FRAMES,
			'speed_bullet':30,
			'lon_bullet':800,
			'hurt_bullet':80,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(85,0,0),
			'fire':'fire0',
			'fire_dim':(20,20),
			'fire_animation':7,
			'fire_status':(110,0,0),
			'sound_reload':'reload_subfusil0',
		},
	},
	'SubfusilUTP': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'SubfusilUTP',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'green',
		},
		'armory':{
			'function':'weapon',
			'capacity':10,
			'left_hand_status':(75,3,-20),
			'right_hand_status':(50,-8,80),
			'sound_action' : 'shot_subfusil0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'SubfusilUTP',
			'dim':(85,23),
			'img_status':(65,0,0),
			'type':'subfusil',
			'bullet':'subfusil',
			'cadence':0.2*FRAMES,
			'reload':2.3*FRAMES,
			'speed_bullet':25,
			'lon_bullet':550,
			'hurt_bullet':100,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(90,0,0),
			'fire':'fire0',
			'fire_dim':(20,20),
			'fire_animation':7,
			'fire_status':(115,0,0),
			'sound_reload':'reload_subfusil0',
		},
	},
	'SubfusilSCN': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'SubfusilSCN',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'green',
		},
		'armory':{
			'function':'weapon',
			'capacity':15,
			'left_hand_status':(75,3,-20),
			'right_hand_status':(50,-8,80),
			'sound_action' : 'shot_subfusil0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'SubfusilSCN',
			'dim':(90,20),
			'img_status':(55,0,0),
			'type':'subfusil',
			'bullet':'subfusil',
			'cadence':0.4*FRAMES,
			'reload':1.5*FRAMES,
			'speed_bullet':25,
			'lon_bullet':550,
			'hurt_bullet':110,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(90,0,0),
			'fire':'fire0',
			'fire_dim':(20,20),
			'fire_animation':7,
			'fire_status':(110,0,0),
			'sound_reload':'reload_subfusil0',
		},
	},
	'PistolaTWW': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'PistolaTWW',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'yellow',
		},
		'armory':{
			'function':'weapon',
			'capacity':10,
			'left_hand_status':(30,10,40),
			'right_hand_status':(30,-10,0),
			'sound_action' : 'shot_pistola0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'PistolaTWW',
			'dim':(45,25),
			'img_status':(50,0,0),
			'type':'pistola',
			'bullet':'pistola',
			'cadence':0.8*FRAMES,
			'reload':2*FRAMES,
			'speed_bullet':20,
			'lon_bullet':700,
			'hurt_bullet':350,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(70,0,0),
			'fire':'fire1',
			'fire_dim':(30,30),
			'fire_animation':7,
			'fire_status':(85,0,0),
			'sound_reload':'reload_pistola0',
		},
	},
	'PistolaYTR': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'PistolaYTR',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'yellow',
		},
		'armory':{
			'function':'weapon',
			'capacity':10,
			'left_hand_status':(30,10,40),
			'right_hand_status':(30,-10,0),
			'sound_action' : 'shot_pistola0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'PistolaYTR',
			'dim':(70,20),
			'img_status':(60,0,0),
			'type':'pistola',
			'bullet':'pistola',
			'cadence':0.8*FRAMES,
			'reload':2*FRAMES,
			'speed_bullet':20,
			'lon_bullet':700,
			'hurt_bullet':400,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(85,0,0),
			'fire':'fire1',
			'fire_dim':(30,30),
			'fire_animation':7,
			'fire_status':(107,0,0),
			'sound_reload':'reload_pistola0',
		},
	},
	'PistolaGPB': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'PistolaGPB',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'yellow',
		},
		'armory':{
			'function':'weapon',
			'capacity':8,
			'left_hand_status':(30,10,40),
			'right_hand_status':(30,-10,0),
			'sound_action' : 'shot_pistola0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'PistolaGPB',
			'dim':(60,20),
			'img_status':(50,0,0),
			'type':'pistola',
			'bullet':'pistola',
			'cadence':0.7*FRAMES,
			'reload':2.2*FRAMES,
			'speed_bullet':20,
			'lon_bullet':700,
			'hurt_bullet':350,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(75,0,0),
			'fire':None,
			'fire_dim':(25,25),
			'fire_animation':7,
			'fire_status':(95,0,0),
			'sound_reload':'reload_pistola0',
		},
	},
	'RifleETW': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'RifleETW',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'red',
		},
		'armory':{
			'function':'weapon',
			'capacity':1,
			'left_hand_status':(63,3,-20),
			'right_hand_status':(33,-7,80),
			'sound_action' : 'shot_rifle0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'RifleETW',
			'dim':(110,30),
			'img_status':(70,0,0),
			'type':'rifle',
			'bullet':'rifle',
			'cadence':0.5*FRAMES,
			'reload':2.5*FRAMES,
			'speed_bullet':40,
			'lon_bullet':1200,
			'hurt_bullet':600,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(110,0,0),
			'fire':None,
			'fire_dim':None,
			'fire_animation':None,
			'fire_status':None,
			'sound_reload':'reload_rifle0',
		},
	},
	'MisilesUUT': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'MisilesUUT',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'purple',
		},
		'armory':{
			'function':'weapon',
			'capacity':1,
			'left_hand_status':(33,10,-20),
			'right_hand_status':(33,-10,80),
			'sound_action' : 'shot_misil0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'MisilesUUT',
			'dim':(80,30),
			'img_status':(50,0,0),
			'type':'misiles',
			'bullet':'misil',
			'radius_explosion':120,
			'hurt_explosion':15,
			'cadence':0.7*FRAMES,
			'reload':2.5*FRAMES,
			'speed_bullet':15,
			'lon_bullet':500,
			'hurt_bullet':300,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(80,0,0),
			'fire':None,
			'fire_dim':None,
			'fire_animation':None,
			'fire_status':None,
			'sound_reload':'reload_misil0',
		},
	},
	'MisilesHJH': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'MisilesHJH',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'purple',
		},
		'armory':{
			'function':'weapon',
			'capacity':2,
			'left_hand_status':(33,10,-20),
			'right_hand_status':(33,-10,80),
			'sound_action' : 'shot_misil0',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'MisilesHJH',
			'dim':(80,30),
			'img_status':(50,0,0),
			'type':'misiles',
			'bullet':'misil',
			'radius_explosion':130,
			'hurt_explosion':20,
			'cadence':0.6*FRAMES,
			'reload':2.5*FRAMES,
			'speed_bullet':15,
			'lon_bullet':500,
			'hurt_bullet':300,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(80,0,0),
			'fire':None,
			'fire_dim':None,
			'fire_animation':None,
			'fire_status':None,
			'sound_reload':'reload_misil0',
		},
	},
	'TaserNBV': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'TaserNBV',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'orange',
		},
		'armory':{
			'function':'weapon',
			'capacity':4,
			'left_hand_status':(33,10,-20),
			'right_hand_status':(33,-10,80),
			'sound_action' : 'buzz1',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'TaserNBV',
			'dim':(65,27),
			'img_status':(50,0,0),
			'type':'taser',
			'bullet':'buzz',
			'hurt_ray':5,
			'ray_time':0.1*FRAMES,
			'n_ray':8,
			'cadence':0.7*FRAMES,
			'reload':1.7*FRAMES,
			'speed_bullet':20,
			'lon_bullet':300,
			'hurt_bullet':100,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(60,0,0),
			'fire':'fire2',
			'fire_dim':(25,25),
			'fire_animation':10,
			'fire_status':(92,0,0),
			'sound_reload':'reload_taser0',
		}
	},
	'TaserDSA': {
		'item': {
			'item':True,
			'lot':0,
			'max_lot':None,
			'icon_item':'TaserDSA',
			'proportion_item':(80,80),
			'direction_item':45,
			'color_item':'orange',
		},
		'armory':{
			'function':'weapon',
			'capacity':3,
			'left_hand_status':(33,10,-20),
			'right_hand_status':(33,-10,80),
			'sound_action' : 'buzz1',
			'sound_select_on':'change_weapon0',
			'sound_select_off':None,
		},
		'weapon':{
			'image':'TaserDSA',
			'dim':(60,28),
			'img_status':(50,0,0),
			'type':'taser',
			'bullet':'buzz',
			'hurt_ray':6,
			'ray_time':0.15*FRAMES,
			'n_ray':6,
			'cadence':0.7*FRAMES,
			'reload':1.7*FRAMES,
			'speed_bullet':20,
			'lon_bullet':300,
			'hurt_bullet':100,
			'n_bullets':1,
			'range_bullets':(0,0),
			'shot_status':(60,0,0),
			'fire':'fire2',
			'fire_dim':(25,25),
			'fire_animation':10,
			'fire_status':(92,0,0),
			'sound_reload':'reload_taser0',
		},
	},
}

MUNITION = {
	'escopeta': {
		'item': {
			'item':True,
			'lot':30,
			'max_lot':None,
			'icon_item':'icon_bullet0',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'blue',
		},
	},
	'subfusil': {
		'item': {
			'item':True,
			'lot':100,
			'max_lot':None,
			'icon_item':'icon_bullet1',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'green',
		},
	},
	'pistola': {
		'item': {
			'item':True,
			'lot':40,
			'max_lot':None,
			'icon_item':'icon_bullet2',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'yellow',
		},
	},
	'rifle': {
		'item': {
			'item':True,
			'lot':15,
			'max_lot':None,
			'icon_item':'icon_bullet3',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'red',
		},
	},
	'misiles': {
		'item': {
			'item':True,
			'lot':6,
			'max_lot':None,
			'icon_item':'icon_misiles',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'purple',
		},
	},
	ENERGY: {
		'item': {
			'item':True,
			'lot':15,
			'max_lot':None,
			'icon_item':'energy',
			'proportion_item':(50,50),
			'direction_item':0,
			'color_item':'orange',
		},
	}
}

BULLETS = {
	'escopeta': {
		'image':'bullet0',
		'dim':(8,8),
		'munition':'escopeta',
		'price':1,
		'type':'bullet',
		'tail':'tail0',
		'dim_tail':(80,10),
		'lon_tail':120,
	},
	'subfusil': {
		'image':'bullet1',
		'dim':(16,8),
		'munition':'subfusil',
		'price':1,
		'type':'bullet',
		'tail':'tail0',
		'dim_tail':(160,10),
		'lon_tail':120,
	},
	'pistola': {
		'image':'bullet2',
		'dim':(10,10),
		'munition':'pistola',
		'price':1,
		'type':'bullet',
		'tail':'tail0',
		'dim_tail':(200,10),
		'lon_tail':120,
	},
	'rifle': {
		'image':'bullet3',
		'dim':(15,8),
		'munition':'rifle',
		'price':1,
		'type':'bullet',
		'tail':'tail0',
		'dim_tail':(150,10),
		'lon_tail':120,
	},
	'misil': {
		'image':'misil',
		'dim':(40,18),
		'munition':'misiles',
		'price':1,
		'type':'explosion',
		'tail':None,
		'dim_tail':(0,0),
		'lon_tail':0,
	},
	'buzz': {
		'image':'buzz',
		'dim':(15,15),
		'munition':ENERGY,
		'price':6,
		'type':'ray',
		'tail':None,
		'dim_tail':(0,0),
		'lon_tail':0,
	}
}