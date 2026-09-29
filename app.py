from board import Board
from player import Player


board = Board()
board.initialize_board()

player1 = Player("red")
player2 = Player("blue")

print("Initial placement")

v1 = 0

print(
    "P1 settlement:",
    board.place_settlement(player1, v1, initial=True)
)

print(
    "P1 settlement list:",
    player1.settlements
)

print(
    "Vertex owner:",
    board.vertices[v1].owner
)

print(
    "Vertex building:",
    board.vertices[v1].building
)

neighbors = list(board.vertex_to_vertices[v1])

v2 = neighbors[0]

print(
    "P2 settlement next to P1:",
    board.place_settlement(player2, v2, initial=True)
)
edge_id = list(board.vertex_to_edges[v1])[0]

print(
    "P1 road:",
    board.place_road(player1, edge_id)
)

print(
    "P1 roads:",
    player1.roads
)

print(
    "Edge owner:",
    board.edges[edge_id].owner
)

edge = board.edges[edge_id]

if edge.v1 == v1:
    next_vertex = edge.v2
else:
    next_vertex = edge.v1

print(
    "P1 normal settlement:",
    board.place_settlement(player1, next_vertex)
)

from game import Game  


game = Game(n_players=4) 

game.start() 

print("Initial placement order:")
print(
    [
        game.players[i].color 
        for i in game.initial_placement_order
    ]
)

print()

print("current player: ",game.current_player.color) 
print("Valid settlements",game.get_valid_initial_settlements()) 

vertex_id = game.get_valid_initial_settlements()[0]

print(
    "Settlement:",
    game.place_initial_settlement(vertex_id)
)

print(
    "Current player:",
    game.current_player.color
)

print(
    "Step:",
    game.placement_step
)


road_id = game.get_valid_initial_roads()[0]

print(
    "Road:",
    game.place_initial_road(road_id)
)