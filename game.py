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
            self.phase = "main" 
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
            "Placement Step:",
            self.placement_step
        )
        print(
            "Initial Placement:", 
            self.initial_placement_index,
            "/" ,
            len(self.initial_placement_order)
        )
        
        print() 
        
        for player in self.players: 
            print(player)
            
            
        