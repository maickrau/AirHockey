#AI_bot
import config
import euclid

def norm(A):
	if not A==0:
		return A/abs(A)
	else:
		return 0
def AI_commands(state):
	ball1_1, ball1_2, ball2_1, ball2_2, puck, walls_left, walls_right, stopPower, wall_player1_goal, wall_player2_goal, goal_player1, goal_player2 = state
	
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
	
	
	
	pos_goalx=config.width/2
	pos_goaly=0
	# In theory powerup locations also.
	# And opponent's balls also
	
	#AI brain starts:
	
	#Point where balls want is pos_bigball + norm(pos_bigball)

	#2 possibility: by keys or straightly by updating state. Last one might cause problems, so:
	
	#ball1
	ball1x=pos_bigballx-pos_ball1x
	ball1y=pos_bigbally-pos_ball1y
	ball2x=pos_bigballx-pos_ball2x
	ball2y=pos_bigballx-pos_ball2y
	serial= { 'letters' + num: {'x': ball1x, 'y': ball1y}, 'arrows' + num: {'x': ball2x, 'y': ball2y}
	}
	return serial