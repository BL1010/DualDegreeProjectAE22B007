from env import CatanEnv


env = CatanEnv(n_players=4)

state = env.reset()

while state["phase"] == "initial_placement":

    vertex_id = env.game.get_valid_initial_settlements()[0]

    state, reward, done, info = env.step({
        "type": "place_initial_settlement",
        "vertex_id": vertex_id
    })

    edge_id = env.game.get_valid_initial_roads()[0]

    state, reward, done, info = env.step({
        "type": "place_initial_road",
        "edge_id": edge_id
    })


print("Initial placement completed")
print()

print("Current player:", env.game.current_player.color)
print("Phase:", env.game.phase)
print()


print("ROLLING DICE")

state, reward, done, info = env.step({
    "type": "roll"
})

print("Dice:", env.game.last_roll)
print("Phase:", env.game.phase)
print("Roll successful:", info["success"])
print()


print("RESOURCE STATE AFTER ROLL")

for player in env.game.players:
    print(
        player.color,
        player.resources
    )

print()


print("TESTING BUILD")

player = env.game.current_player

player.resources["wood"] = 10
player.resources["brick"] = 10
player.resources["sheep"] = 10
player.resources["wheat"] = 10
player.resources["ore"] = 10

print("Resources before building:")
print(player.resources)
print()


valid_edges = []

for edge_id in env.game.board.edges:
    if env.game.board.can_place_road(player, edge_id):
        valid_edges.append(edge_id)

edge_id = valid_edges[0]

state, reward, done, info = env.step({
    "type": "build_road",
    "edge_id": edge_id
})

print("Built road at edge:", edge_id)
print("Build successful:", info["success"])
print("Resources after building:")
print(player.resources)
print("Player roads:", player.roads)
print()


print("ENDING TURN")

old_player = player.color

state, reward, done, info = env.step({
    "type": "end_turn"
})

print("Ended turn for:", old_player)
print("End turn successful:", info["success"])
print("New current player:", env.game.current_player.color)
print("New phase:", env.game.phase)
print("New round:", env.game.round_number)
