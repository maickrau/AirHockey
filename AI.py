#AI_bot
import config
import euclid

def norm(A):
	if not A==0:
		return A/abs(A)
	else:
		return 0


def AI_commands(state):

	if (config.difficulty==0):
	#	ball1_1, ball1_2, ball2_1, ball2_2, puck, walls_left, walls_right, stopPower, wall_player1_goal, wall_player2_goal, goal_player1, goal_player2 = state
		ball2_1 = state.getByIdent('letters2')
		ball2_2 = state.getByIdent('arrows2')
		puck = state.getByIdent('puck')
		#
		#
		# Somehow get following variables
		#
		#
		#
		pos_ball1x=ball2_1.pos.x
		pos_ball1y=ball2_1.pos.y
		pos_ball2x=ball2_2.pos.x
		pos_ball2y=ball2_2.pos.y
		pos_bigballx=puck.pos.x
		pos_bigbally=puck.pos.y
		num="2"
		
		
		
		pos_goalx=config.field_width/2
		pos_goaly=0
		# In theory powerup locations also.
		# And opponent's balls also
		
		#AI brain starts:
		
		#Point where balls want is pos_bigball + norm(pos_bigball)

		#2 possibility: by keys or straightly by updating state. Last one might cause problems, so:
		
		#ball1
		ball1x=pos_bigballx-pos_ball1x + (pos_bigballx-pos_ball1x)/abs(pos_bigballx-pos_ball1x)
		ball1y=pos_bigbally-pos_ball1y + (pos_bigbally-pos_ball1y)/abs(pos_bigbally-pos_ball1y)
		ball2x=pos_bigballx-pos_ball2x + (pos_bigballx-pos_ball2x)/abs(pos_bigballx-pos_ball2x)
		ball2y=pos_bigbally-pos_ball2y + (pos_bigbally-pos_ball2y)/abs(pos_bigbally-pos_ball2y)
		serial= { 'letters' + num: {'x': int(ball1x), 'y': int(ball1y)}, 'arrows' + num: {'x': ball2x, 'y': ball2y}, 'seq':'0', 'type':'input'}
	#	print serial
	elif(config.difficulty==1):
	#	ball1_1, ball1_2, ball2_1, ball2_2, puck, walls_left, walls_right, stopPower, wall_player1_goal, wall_player2_goal, goal_player1, goal_player2 = state
		ball2_1 = state.getByIdent('letters2')
		ball2_2 = state.getByIdent('arrows2')
		puck = state.getByIdent('puck')
		#
		#
		# Somehow get following variables
		#
		#
		#
		pos_ball1x=ball2_1.pos.x
		pos_ball1y=ball2_1.pos.y
		pos_ball2x=ball2_2.pos.x
		pos_ball2y=ball2_2.pos.y
		pos_bigballx=puck.pos.x
		pos_bigbally=puck.pos.y
		num="2"
		
		
		
		pos_goalx=config.field_width/2
		pos_goaly=0
		# In theory powerup locations also.
		# And opponent's balls also
		
		#AI brain starts:
		
		#Point where balls want is pos_bigball + norm(pos_bigball)

		#2 possibility: by keys or straightly by updating state. Last one might cause problems, so:
		
		#ball1
		
		
		ball1x=pos_bigballx-pos_ball1x + (pos_bigballx-pos_ball1x)/abs(pos_bigballx-pos_ball1x)		
		ball1y=pos_bigbally-pos_ball1y + (pos_bigbally-pos_ball1y)/abs(pos_bigbally-pos_ball1y)
		if (pos_bigbally-pos_ball1y+10)>0:
			ball1y=ball1y+150
		if (pos_bigbally-pos_ball2y+10)>0:
			ball2y=ball2y+150            
#		if (pos_bigballx-pos_ball1x)
#		ball2x=pos_ball2x;
#		ball2y=pos_ball2y;
		ball2x=pos_bigballx-pos_ball2x + (pos_bigballx-pos_ball2x)/abs(pos_bigballx-pos_ball2x)
		ball2y=pos_bigbally-pos_ball2y + (pos_bigbally-pos_ball2y)/abs(pos_bigbally-pos_ball2y)
		serial= { 'letters' + num: {'x': int(ball1x), 'y': int(ball1y)}, 'arrows' + num: {'x': ball2x, 'y': ball2y}, 'seq':'0', 'type':'input'}
		
	return serial