# guac.py
#
# plays Tic Tac Toe
# clicked boxes alternate red and blue
# boxes fall if no winner
# boxes launch upon win
# avocado "Vanna White" reacts accordingly

import json
import time
import arena
import re

HOST = "oz.andrew.cmu.edu"
TOPIC = "realm/s/wine/"
REALM = "realm"
SCENE = "wine"

# Globals (yes, Sharon)

icons = {} # dict of cube objects to be indexed by tuple (x,y)
#grid of the state of each object
grid = [[0,0,0,0,0,0], 
		[0,0,0,0,0,0], 
		[0,0,0,0,0,0], 
		[0,0,0,0,0,0], 
		[0,0,0,0,0,0], 
		[0,0,0,0,0,0], 
		[0,0,0,0,0,0], 
		[0,0,0,0,0,0],
		[0,0,0,0,0,0], 
		[0,0,0,0,0,0]]

wineNames = [["Riesling","Cabernet Sauvignon","Chardonnay","Merlot","Pinot Noir",""],
			["","Pinot Grigio","Zinfandel","Malbec","Merlot2",""],
			["I'm","Running","Out","Of","Wine","Names"],
			["","The Red Stuff","","","wine (probably)",""],
			["","","","","",""],
			["","Dead Dove (DO NOT EAT)","","grapes?","",""],
			["","Wine coolers","","","",""],
			["","","","","",""],
			["","","","","",""],
			["","","","","",""],]
Xcoords = [-0.42235, -0.25725, -0.09215, 0.09215, 0.25725, 0.42235]
Ycoords = [1.12075, 1.03185, 0.94295, 0.85405, 0.76515, 0.62545, 0.53655, 0.44765, 0.35875, 0.26985]
color = [(164,168,50),(236,242,48),(145,145,145),(94,235,23)] #dark yellow, bright yellow, grey, green
messages = []
cardcat = None

def initIcons():
	global Xcoords, Ycoords
	global icons
	for x in range (0,6):
		for y in range (0,10):
			#print("x: " + str(x) + " y: " + str(y))
			name = "icon_"+str(x)+"_"+str(y)
			icons[(x,y)]=arena.Object(objType=arena.Shape.sphere,
									  persist=True,
									  objName=name,
									  physics=arena.Physics.static,
									  data='{"collision-listner":"", "material": {"transparent":true,"opacity": 0.8},"impulse":{"on":"mouseup","force":"0 40 0","position": "10 1 1"}}',
									  location=(Xcoords[x],Ycoords[y],0.2),
									  color=color[2],
									  scale=(0.02,0.02,0.02),
									  clickable=True);

def deleteCardcat():
    global cardcat
    cardcat.delete()


def drawCardcat():
    global cardcat
    cardcat = arena.Object(persist=True,
                           objName="cardcatalog",
                           objType=arena.Shape.gltf_model,
                           url="models/cardcat.glb",
                           location=(0,0,0),
                           scale=(0.485,0.425,0.49))


def draw_board():
    global grid
    global wineNames
    global icons
    initIcons();
    for y in range (0,10):
    	for x in range (0,6):
    		if(wineNames[y][x]!=""):
    			icons[(x,y)].update(color=color[0])
    			grid[y][x]=1
    drawCardcat();
    

def icon_select(x,y):
	global icons
	global grid
	global wineNames
	if(grid[y][x]==0):
		#idk yet. enter text?
		wineDisp = arena.Object(objType=arena.Shape.text,
					objName="wine_name",
					persist=True,
					data='{"text":"empty"}',
					location=(0,1.8,-0.4),
					color=color[1],
					scale=(1,1,1));
	else:
		icons[(x,y)].update(color=color[1]);
		wineDisp = arena.Object(objType=arena.Shape.text,
					objName="wine_name",
					persist=True,
					data='{"text":"'+wineNames[y][x]+'"}',
					location=(0,1.8,-0.4),
					color=color[1],
					scale=(1,1,1));
	

def icon_unselect(x,y):
	global icons
	global grid
	if(grid[y][x]==1):
		icons[(x,y)].update(color=color[0])
	else:
		icons[(x,y)].update(color=color[2])

def icon_click(x,y):

	global icons
	global grid
	if(grid[y][x]==1):
		icons[(x,y)].update(color=color[1])
	else:
		icons[(x,y)].update(color=color[2])

	

def scene_callback(msg):
	global icons
	global grid

	jsonMsg = json.loads(msg)
	if jsonMsg["action"] != "clientEvent":
	  return
	# Check for mouseenter events
	# the obj vars are arena objects
	# the state vars are just ints that hold if the light is on/off
	if jsonMsg["type"] == "mouseenter":
		name = jsonMsg["object_id"]
		numname = name.split("_") #1 is x, 2 is y
		x = int(numname[1])
		y = int(numname[2])
		icon_select(x,y)

     # Check for mouseleve events
	if jsonMsg["type"] == "mouseleave":
		name = jsonMsg["object_id"]
		numname = name.split("_") #1 is x, 2 is y
		x = int(numname[1])
		y = int(numname[2])
		icon_unselect(x,y)

	if jsonMsg["type"] == "mousedown":
		name = jsonMsg["object_id"]
		numname = name.split("_") #1 is x, 2 is y
		x = int(numname[1])
		y = int(numname[2])
		icon_click(x,y)



arena.init(HOST, REALM, SCENE, scene_callback)
print("starting main loop")
draw_board()
arena.handle_events()
