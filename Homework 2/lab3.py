from connectfour import *
from basicplayer import *
import basicplayer
import time

reset_nodes_expanded()
start = time.clock()
run_game(new_player,basic_player)
end = time.clock()
runtime = end - start
print "New Player vs Basic Player"
print "Execution Time:", runtime
print "Nodes Expanded:", basicplayer.nodes_expanded[1]

reset_nodes_expanded()
start = time.clock()
run_game(alphabeta_player,basic_player)
end = time.clock()
runtime = end - start
print "Alphabeta Player vs Basic Player"
print "Execution Time:", runtime
print "Nodes Expanded:", basicplayer.nodes_expanded[1]
