from game import Game 

class CatanEnv: 
    def __init__(self,n_players = 4): 
        self.n_players = n_players 
        self.game = None 
        
    def reset(self): 
        self.game = Game(n_players=self.n_players) 
        self.game.start() 
        
        return self.get_state() 
    
    def get_state(self): 
        state  = {
            "phase": self.game.phase, 
            "current_player": self.game.current_player_index, 
            "round": self.game.round_number, 
            "last_roll": self.game.last_roll, 
            "players": [] 
        }
        
        for player in self.game.players: 
            state["players"].append({
                "color": player.color,
                "resources": player.resources.copy(), 
                "roads": player.roads.copy(), 
                "settlements": player.settlements.copy(), 
                "industries": player.industries.copy(), 
                "victory_points": player.victory_points
            })
        return state
    
    def step(self,action): 
        action_type = action["type"] 
        
        if action_type == "place_initial_settlement": 
            success = self.game.place_initial_settlement(
                action["vertex_id"]
            ) 
        elif action_type == "place_initial_road": 
            success = self.game.place_initial_road(
                action["edge_id"]
            )
        
        elif action_type == "roll": 
            result = self.game.roll_dice() 
            success = result is not None 
            
        elif action_type == "build_road": 
            success = self.game.build_road(
                action["edge_id"]
            )
            
        elif action_type == "build_settlement": 
            success = self.game.build_settlement(
                action["vertex_id"]
            )
        
        elif action_type == "build_industry": 
            success = self.game.build_industry(
                action["vertex_id"]
            )
        elif action_type == "end_turn": 
            success = self.game.end_turn() 
        else: 
            success = False 
            
        state = self.get_state() 
        done= self.game.phase == "game_over" 
        reward = 0 
        
        if done: 
            if self.game.winner  == self.game.current_player: 
                reward = 1 
            else: 
                reward = -1 
        
        info ={
            "success": success
        }
        
        return state,reward,done,info 