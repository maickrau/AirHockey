#AI_bot

def AI_commands(state):
	
	#
	#
	# Somehow get following variables
	#
	#
	#
	pos_ball1x=100
	pos_ball1y=100
	pos_ball2x=100 
	pos_ball2y=100
	pos_bigballx=100
	pos_bigbally=100
	
	pos_goalx=config.width/2
	pos_goaly=0
	# In theory powerup locations also.
	# And opponent's balls also
	
	#AI brain starts:
	
	#Point where balls want is pos_bigball + norm(pos_bigball)

	#2 possibility: by keys or straightly by updating state. Last one might cause problems, so:
	
	#ball1
	if(pos_ball1x>pos_bigballx+norm(pos_bigballx-pos_goalx)):
		ball1x=1
	elif(pos_ball1x==pos_bigballx+norm(pos_bigballx-pos_goalx)):
		ball1x=0
	else:
		ball1x=-1
	
	if(pos_ball1y>pos_bigbally+norm(pos_bigbally-pos_goaly)):
		ball1y=1
	elif(pos_ball1y==pos_bigbally+norm(pos_bigbally-pos_goaly)):
		ball1y=0
	else:
		ball1y=-1
	
	
	#ball2
	if(pos_ball2x>pos_bigballx+norm(pos_bigballx-pos_goalx)):
		ball2x=1
	elif(pos_ball2x==pos_bigballx+norm(pos_bigballx-pos_goalx)):
		ball2x=0
	else:
		ball2x=-1
	
	if(pos_ball2y>pos_bigbally+norm(pos_bigbally-pos_goaly)):
		ball2y=1
	elif(pos_ball2y==pos_bigbally+norm(pos_bigbally-pos_goaly)):
		ball2y=0
	else:
		ball2y=-1
		
	