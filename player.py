class Player:
    def __init__(self, color):
        self.color = color

        self.resources = {
            "wood": 0,
            "brick": 0,
            "sheep": 0,
            "wheat": 0,
            "ore": 0
        }

        self.roads = []
        self.settlements = []
        self.industries = []

        self.victory_points = 0

    def add_resource(self, resource, amount=1):
        self.resources[resource] += amount

    def remove_resource(self, resource, amount=1):
        if self.resources[resource] < amount:
            return False

        self.resources[resource] -= amount
        return True

    def add_road(self, edge_id):
        self.roads.append(edge_id)

    def add_settlement(self, vertex_id):
        self.settlements.append(vertex_id)
        self.victory_points += 1

    def add_industry(self, vertex_id):
        self.industries.append(vertex_id)
        self.victory_points += 2

    def __str__(self):
        return (
            f"Player {self.color}: "
            f"VP={self.victory_points}, "
            f"Resources={self.resources}, "
            f"Roads={self.roads}, "
            f"Settlements={self.settlements}, "
            f"Industries={self.industries}"
        )