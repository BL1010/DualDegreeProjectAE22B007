import numpy as np 
from board import Board 
from player import Player 

class Game: 
    def __init__(self,n_players = 4, players_colors = None): 
        if players_colors is None: 
            players_colors = ["red","blue","green","yellow"]
            
        if n_players < 2 or n_players > len(players_colors): 
            raise ValueError("Invalid number of Players")
        
        self.board = Board() 
        
        self.players = [ Player(players_colors[i]) for i in range(n_players)] 
        
        self.current_player_index = 0 
        self.round_number = 1 
        self.phase = "initial_placement" 
        self.placement_step = "settlement"
        
        self.initial_placement_order = (
            list(range(n_players)) 
            + list(range(n_players-1,-1,-1))
        )
        
        self.initial_placement_index = 0 
        
        self.last_roll = None 
        self.winner= None 
        
        self.BUILD_COSTS = {
            "road": {
                "wood": 1, 
                "brick": 1
            }, 
            "settlement": {
                "wood": 1, 
                "brick": 1, 
                "sheep": 1, 
                "wheat": 1
            },
            "industry": {
              "ore": 3, 
              "wheat": 2  
            }
        }
        
    @property 
    def current_player(self): 
        return self.players[self.current_player_index] 
    
    def start(self): 
        self.board.initialize_board() 
        
    def place_initial_settlement(self,vertex_id): 
        if self.phase!="initial_placement": 
            return False 
        if self.placement_step != "settlement": 
            return False 
        
        player = self.current_player 
        
        success = self.board.place_settlement(
            player,
            vertex_id, 
            initial=True
        )
        if not success: 
            return False 
        
        self.placement_step = "road" 
        return True 
    
    
    def place_initial_road(self,edge_id): 
        if self.phase!="initial_placement": 
            return False 
        
        if self.placement_step != "road": 
            return False 
        
        player = self.current_player 
        
        success= self.board.place_road(
            player,
            edge_id
        )
        
        if not success: 
            return False 
        
        self.advance_initial_placement() 
        
        return True 
    
    def advance_initial_placement(self): 
        self.initial_placement_index+=1 
        
        if self.initial_placement_index >= len(
            self.initial_placement_order
        ): 
            self.phase = "roll" 
            self.placement_step = None 
            self.current_player_index = 0 
            self.round_number = 1 
            return 
        
        self.current_player_index= (
            self.initial_placement_order[
                self.initial_placement_index
            ]
        )
        
        self.placement_step = "settlement" 
        
    def get_valid_initial_settlements(self): 
        
        if self.phase != "initial_placement": 
            return [] 
        if self.placement_step != "settlement": 
            return [] 
        
        player = self.current_player 
        
        valid_vertices = [] 
        
        
        for vertex_id in self.board.vertices: 
            if self.board.can_place_settlement(
                player,
                vertex_id,
                initial=True
            ): 
                valid_vertices.append(vertex_id) 
        return valid_vertices 
    
    
    def get_valid_initial_roads(self): 
        if self.phase != "initial_placement": 
            return [] 
        if self.placement_step != "road": 
            return [] 
        
        player = self.current_player 
        
        valid_edges = [] 
        
        for edge_id in self.board.edges:  
            if self.board.can_place_road(
                player,
                edge_id
            ): 
                valid_edges.append(edge_id)
        return valid_edges 
    
    
    
    def print_state(self): 
        
        print("Phase:", self.phase) 
        print("Round:",self.round_number) 
        
        print(
            "Current Player:",
            self.current_player.color
        )
        print(
            "Last Roll: " ,
            self.last_roll
        )
        print(
            "Placement Step:",
            self.placement_step
        )
        print(
            "Initial Placement:", 
            self.initial_placement_index,
            "/" ,
            len(self.initial_placement_order)
        )
        
        if self.winner is not None: 
            print(
                "Winner:",
                self.winner.color
            )
        
        print() 
        
        for player in self.players: 
            print(player)
            
    def roll_dice(self): 
        if self.phase!="roll": 
            return None 
        
        die_1 = np.random.randint(1,7) 
        die_2 = np.random.randint(1,7) 
        
        self.last_roll = die_1 + die_2 
        self.distribute_resources(self.last_roll) 
        self.phase= "main_action" 
        return self.last_roll 
    
    
    def distribute_resources(self,dice_value): 
        for tile in self.board.tiles.values(): 
            
            if tile.number != dice_value: 
                continue 
            
            for vertex_id in tile.vertex_ids: 
                vertex = self.board.vertices[vertex_id] 
                
                if vertex.owner is None: 
                    continue 
                
                if vertex.building == "settlement": 
                    amount = 1 
                elif vertex.building == "industry": 
                    amount = 2 
                else: 
                    continue 
                
                for player in self.players: 
                    if player.color == vertex.owner: 
                        player.add_resource(
                            tile.resource,
                            amount
                        )
                        break 
                    
    def can_afford(self,player,building_type): 
        cost = self.BUILD_COSTS[building_type] 
        for resource, amount in cost.items(): 
            if player.resources[resource]<amount: 
                return False 
        return True 
    
    
    def pay_cost(self,player,building_type): 
        cost = self.BUILD_COSTS[building_type] 
        for resource, amount in cost.items(): 
            player.resources[resource]-=amount 
            
            
    def build_road(self,edge_id): 
        if self.phase!="main_action": 
            return False 
        
        player= self.current_player 
        if not self.can_afford(player,"road"): 
            return False 
        
        if not self.board.can_place_road(player,edge_id): 
            return False 
        
        self.pay_cost(player,"road") 
        
        success =  self.board.place_road(
            player,
            edge_id
        )
        if success: 
            self.check_winner() 
        
        return success 
        
    def build_settlement(self, vertex_id):
        if self.phase != "main_action":
            return False

        player = self.current_player

        if not self.can_afford(player, "settlement"):
            return False

        if not self.board.can_place_settlement(
            player,
            vertex_id,
            initial=False
        ):
            return False

        self.pay_cost(player, "settlement")

        success =  self.board.place_settlement(
            player,
            vertex_id,
            initial=False
        )  
        if success: 
            self.check_winner() 
            
        return success 
       
    def build_industry(self, vertex_id):
        if self.phase != "main_action":
            return False

        player = self.current_player

        if not self.can_afford(player, "industry"):
            return False

        if not self.board.can_place_industry(
            player,
            vertex_id
        ):
            return False

        self.pay_cost(player, "industry")

        success = self.board.place_industry(
            player,
            vertex_id
        ) 
        if success: 
            self.check_winner() 
        
        return success
        
    def advance_turn(self):
        self.current_player_index += 1

        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
            self.round_number += 1

        self.phase = "roll"
        self.last_roll = None 
        
    def end_turn(self):
        if self.phase != "main_action":
            return False

        if self.winner is not None:
            return False

        self.advance_turn()

        return True
                    
                    
    def check_winner(self):
        for player in self.players:
            if player.victory_points >= 10:
                self.winner = player
                self.phase = "game_over"
                return player

        return None
