import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Polygon


class Vertex:
    def __init__(self, vertex_id, x, y):
        self.id = vertex_id
        self.x = x
        self.y = y
        self.owner = None
        self.building = None 


class Edge:
    def __init__(self, edge_id, v1, v2):
        self.id = edge_id
        self.v1 = v1
        self.v2 = v2
        self.owner = None


class Tile:
    def __init__(self, tile_id, q, r, x, y, resource, number):
        self.id = tile_id
        self.q = q
        self.r = r
        self.x = x
        self.y = y
        self.resource = resource
        self.number = number
        self.vertex_ids = []
        self.edge_ids = []


class Board:
    HEX_VERTEX_OFFSETS = [
        (-np.sqrt(3) / 2, 0.5),
        (0, 1),
        (np.sqrt(3) / 2, 0.5),
        (np.sqrt(3) / 2, -0.5),
        (0, -1),
        (-np.sqrt(3) / 2, -0.5)
    ]

    def __init__(self):
        self.tiles = {}
        self.vertices = {}
        self.edges = {}

        self.vertex_lookup = {}
        self.edge_lookup = {}

        self.vertex_to_vertices = {}
        self.vertex_to_edges = {}
        self.vertex_to_tiles = {}

        self.edge_to_tiles = {}
        self.tile_to_tiles = {}

        self.next_tile_id = 0
        self.next_vertex_id = 0
        self.next_edge_id = 0

    def get_or_create_vertex(self, x, y):
        key = (round(x, 5), round(y, 5))

        if key in self.vertex_lookup:
            return self.vertex_lookup[key]

        vertex_id = self.next_vertex_id
        self.next_vertex_id += 1

        vertex = Vertex(vertex_id, x, y)

        self.vertices[vertex_id] = vertex
        self.vertex_lookup[key] = vertex_id

        self.vertex_to_vertices[vertex_id] = set()
        self.vertex_to_edges[vertex_id] = set()
        self.vertex_to_tiles[vertex_id] = set()

        return vertex_id

    def get_or_create_edge(self, v1, v2):
        key = tuple(sorted((v1, v2)))

        if key in self.edge_lookup:
            edge_id = self.edge_lookup[key]

            return edge_id

        edge_id = self.next_edge_id
        self.next_edge_id += 1

        edge = Edge(edge_id, v1, v2)

        self.edges[edge_id] = edge
        self.edge_lookup[key] = edge_id

        self.edge_to_tiles[edge_id] = set()

        self.vertex_to_vertices[v1].add(v2)
        self.vertex_to_vertices[v2].add(v1)

        self.vertex_to_edges[v1].add(edge_id)
        self.vertex_to_edges[v2].add(edge_id)

        return edge_id

    def add_tile(self, q, r, resource, number):
        x = np.sqrt(3) * (q + r / 2)
        y = 1.5 * r

        tile_id = self.next_tile_id
        self.next_tile_id += 1

        tile = Tile(
            tile_id,
            q,
            r,
            x,
            y,
            resource,
            number
        )

        vertex_ids = []

        for dx, dy in self.HEX_VERTEX_OFFSETS:
            vertex_id = self.get_or_create_vertex(
                x + dx,
                y + dy
            )

            vertex_ids.append(vertex_id)

        tile.vertex_ids = vertex_ids

        edge_ids = []

        for i in range(6):
            v1 = vertex_ids[i]
            v2 = vertex_ids[(i + 1) % 6]

            edge_id = self.get_or_create_edge(v1, v2)

            edge_ids.append(edge_id)

        tile.edge_ids = edge_ids

        self.tiles[tile_id] = tile
        self.tile_to_tiles[tile_id] = set()

        for vertex_id in vertex_ids:
            self.vertex_to_tiles[vertex_id].add(tile_id)

        for edge_id in edge_ids:
            self.edge_to_tiles[edge_id].add(tile_id)

        return tile_id

    def build_tile_neighbors(self):
        for edge_id, tile_ids in self.edge_to_tiles.items():

            tile_ids = list(tile_ids)

            if len(tile_ids) == 2:
                tile_1 = tile_ids[0]
                tile_2 = tile_ids[1]

                self.tile_to_tiles[tile_1].add(tile_2)
                self.tile_to_tiles[tile_2].add(tile_1)

    def initialize_board(self):
        resources = [
            "wood", "wood", "wood", "wood",
            "brick", "brick", "brick",
            "sheep", "sheep", "sheep", "sheep",
            "wheat", "wheat", "wheat", "wheat",
            "ore", "ore", "ore",
            "desert"
        ]

        numbers = [
            2,
            3, 3,
            4, 4,
            5, 5,
            6, 6,
            8, 8,
            9, 9,
            10, 10,
            11, 11,
            12
        ]

        np.random.shuffle(resources)

        number_index = 0

        for q in range(-2, 3):
            for r in range(-2, 3):
                if max(abs(q), abs(r), abs(q + r)) > 2:
                    continue

                resource = resources.pop()

                if resource == "desert":
                    number = None
                else:
                    number = numbers[number_index]
                    number_index += 1

                self.add_tile(
                    q,
                    r,
                    resource,
                    number
                )

        self.build_tile_neighbors()

    def print_board(self):
        for tile_id, tile in self.tiles.items():
            tile = self.tiles[tile_id]

            print(
                "Tile:",
                tile.id,
                "Axial:",
                (tile.q, tile.r),
                "Resource:",
                tile.resource,
                "Number:",
                tile.number
            )

            print(
                "Vertices:",
                tile.vertex_ids
            )

            print(
                "Edges:",
                tile.edge_ids
            )

            print()

    def print_topology(self):
        print("Number of tiles:", len(self.tiles))
        print("Number of vertices:", len(self.vertices))
        print("Number of edges:", len(self.edges))

        print()

        print("Vertex -> Vertices")

        for vertex_id, neighbors in self.vertex_to_vertices.items():
            print(
                vertex_id,
                "->",
                sorted(neighbors)
            )

        print()

        print("Vertex -> Edges")

        for vertex_id, edges in self.vertex_to_edges.items():
            print(
                vertex_id,
                "->",
                sorted(edges)
            )

        print()

        print("Vertex -> Tiles")

        for vertex_id, tiles in self.vertex_to_tiles.items():
            print(
                vertex_id,
                "->",
                sorted(tiles)
            )

        print()

        print("Edge -> Tiles")

        for edge_id, tiles in self.edge_to_tiles.items():
            print(
                edge_id,
                "->",
                sorted(tiles)
            )

        print()

        print("Tile -> Tiles")

        for tile_id, tiles in self.tile_to_tiles.items():
            print(
                tile_id,
                "->",
                sorted(tiles)
            )

    def draw(self):
        fig, ax = plt.subplots(figsize=(10, 9))

        for tile in self.tiles.values():
            points = []

            for vertex_id in tile.vertex_ids:
                vertex = self.vertices[vertex_id]

                points.append(
                    (vertex.x, vertex.y)
                )

            polygon = Polygon(
                points,
                closed=True,
                facecolor="white",
                edgecolor="black",
                linewidth=2
            )

            ax.add_patch(polygon)

            if tile.number is None:
                text = f"{tile.resource}\nDesert"
            else:
                text = f"{tile.resource}\n{tile.number}"

            ax.text(
                tile.x,
                tile.y,
                text,
                ha="center",
                va="center",
                fontsize=10
            )

        for vertex in self.vertices.values():
            ax.scatter(
                vertex.x,
                vertex.y,
                s=25,
                color="black",
                zorder=5
            )

        ax.set_aspect("equal")
        ax.set_xlim(-5, 5)
        ax.set_ylim(-4.5, 4.5)
        ax.axis("off")
        ax.set_title("Catan Board")

        plt.show()
    
    def can_place_settlement(self, player, vertex_id, initial=False):
        if vertex_id not in self.vertices:
            return False

        vertex = self.vertices[vertex_id]

        if vertex.owner is not None:
            return False

        for neighbor_id in self.vertex_to_vertices[vertex_id]:
            neighbor = self.vertices[neighbor_id]

            if neighbor.owner is not None:
                return False

        if initial:
            return True

        for edge_id in self.vertex_to_edges[vertex_id]:
            edge = self.edges[edge_id]

            if edge.owner == player.color:
                return True

        return False


    def place_settlement(self, player, vertex_id, initial=False):
        if not self.can_place_settlement(player, vertex_id, initial):
            return False

        vertex = self.vertices[vertex_id]

        vertex.owner = player.color
        vertex.building = "settlement"

        player.settlements.append(vertex_id)
        player.victory_points += 1

        return True
    
    
    
    def can_place_road(self, player, edge_id):
        if edge_id not in self.edges:
            return False

        edge = self.edges[edge_id]

        if edge.owner is not None:
            return False

        endpoints = [edge.v1, edge.v2]

        for vertex_id in endpoints:
            vertex = self.vertices[vertex_id]

            if vertex.owner == player.color:
                return True

            if vertex.owner is not None:
                continue

            for connected_edge_id in self.vertex_to_edges[vertex_id]:
                if connected_edge_id == edge_id:
                    continue

                connected_edge = self.edges[connected_edge_id]

                if connected_edge.owner == player.color:
                    return True

        return False


    def place_road(self, player, edge_id):
        if not self.can_place_road(player, edge_id):
            return False

        edge = self.edges[edge_id]

        edge.owner = player.color

        player.roads.append(edge_id)

        return True
    
    
    
    def can_place_industry(self, player, vertex_id):
        if vertex_id not in self.vertices:
            return False

        vertex = self.vertices[vertex_id]

        if vertex.owner != player.color:
            return False

        if vertex.building != "settlement":
            return False

        return True


    def place_industry(self, player, vertex_id):
        if not self.can_place_industry(player, vertex_id):
            return False

        vertex = self.vertices[vertex_id]

        vertex.building = "industry"

        player.settlements.remove(vertex_id)
        player.industries.append(vertex_id)

        player.victory_points += 1

        return True
