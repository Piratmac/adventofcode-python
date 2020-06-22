from math import sqrt


class PlayerBlocked(Exception):
    pass


def collisions(players):
    positions = [x.position for x in players]
    if positions == set(positions):
        return None
    else:
        return [x for x in set(positions) if positions.count(x) > 1]


class RaceTrack:
    vertices = {}
    edges = {}
    """
    Represents which directions are allowed based on the track piece

    Structure:
    track_piece: allowed directions
    """
    allowed_directions = {
        "/": directions_all,
        "\\": directions_all,
        "+": directions_all,
        "|": directions_vertical,
        "-": directions_horizontal,
        "^": directions_vertical,
        "v": directions_vertical,
        ">": directions_horizontal,
        "<": directions_horizontal,
    }

    # Usual replacements
    player_replace = {
        ">": "-",
        "<": "-",
        "^": "|",
        "v": "|",
    }

    def __init__(self, vertices=[], edges={}):
        self.vertices = vertices
        self.edges = edges

    def text_to_track(self, text, allowed_directions={}):
        """
        Converts a text to a set of coordinates

        The text is expected to be separated by newline characters
        The vertices will have x-y*j as coordinates (so y axis points south)
        Edges will be calculated as well

        :param string text: The text to convert
        :param str elements: How to interpret the track
        :return: True if the text was converted
        """
        self.vertices = {}
        self.allowed_directions.update(allowed_directions)

        for y, line in enumerate(text.splitlines()):
            for x in range(len(line)):
                if line[x] in self.allowed_directions:
                    self.vertices[x - y * 1j] = line[x]

        for source, track in self.vertices.items():
            for direction in self.allowed_directions[track]:
                target = source + direction
                if not target in self.vertices:
                    continue

                target_dirs = self.allowed_directions[self.vertices[target]]
                if -direction not in target_dirs:
                    continue

                if source in self.edges:
                    self.edges[source].append(target)
                else:
                    self.edges[source] = [target]

        return True

    def track_to_text(self, mark_coords={}, wall=" "):
        """
        Converts a set of coordinates to a text

        The text will be separated by newline characters

        :param dict mark_coords: List of coordinates to mark, with letter to use
        :param string wall: Which character to use as walls
        :return: the converted text
        """

        min_y, max_y = int(max_imag(self.vertices)), int(min_imag(self.vertices))
        min_x, max_x = int(min_real(self.vertices)), int(max_real(self.vertices))

        text = ""

        for y in range(min_y, max_y - 1, -1):
            for x in range(min_x, max_x + 1):
                if x + y * 1j in mark_coords:
                    text += mark_coords[x + y * 1j]
                else:
                    text += self.vertices.get(x + y * 1j, wall)
            text += "\n"

        return text

    def replace_elements(self, replace_map=None):
        """
        Replaces elements in the track (useful to remove players)

        :param dict replace_map: Replacement map
        :return: True
        """

        if replace_map is None:
            replace_map = self.player_replace
        self.vertices = {x: replace_map.get(y, y) for x, y in self.vertices.items()}
        return True

    def find_elements(self, elements):
        """
        Finds elements in the track

        :param dict elements: elements to find
        :return: True
        """

        found = {x: y for x, y in self.vertices.items() if y in elements}
        return found


class Player:
    """
    Represents which directions are allowed based on the track piece

    Structure:
    track_piece: source direction: allowed target direction
    """

    allowed_directions = {
        "/": {north: [east], south: [west], east: [north], west: [south],},
        "\\": {north: [west], south: [east], east: [south], west: [north],},
        "+": {
            north: directions_all,
            south: directions_all,
            east: directions_all,
            west: directions_all,
        },
        "|": {
            north: directions_vertical,
            south: directions_vertical,
            east: None,
            west: None,
        },
        "-": {
            north: None,
            south: None,
            east: directions_horizontal,
            west: directions_horizontal,
        },
    }

    initial_directions = {
        ">": east,
        "<": west,
        "^": north,
        "v": south,
    }

    position = 0
    direction = 0

    def __init__(self, racetrack, position=0, direction=None):
        self.position = position
        if direction is None:
            self.direction = self.initial_directions[racetrack.vertices[position]]
        else:
            self.direction = direction

    def move(self, racetrack, steps=1):
        """
        Moves the player in the direction provided

        :param RaceTrack racetrack: The track to use
        :param int steps: The number of steps to take
        :return: nothing
        """
        for step in range(steps):
            # First, let's move the player
            self.before_move()

            self.position += self.direction

            if self.position not in racetrack.vertices:
                raise PlayerBlocked

            self.after_move()

            # Then, let's make him turn
            self.before_rotation()

            track = racetrack.vertices[self.position]
            possible_directions = self.allowed_directions[track][self.direction]

            if possible_directions is None:
                raise PlayerBlocked
            elif len(possible_directions) == 1:
                self.direction = possible_directions[0]
            else:
                self.choose_direction(possible_directions)

            self.after_rotation()

    def before_move(self):
        pass

    def after_move(self):
        pass

    def before_rotation(self):
        pass

    def after_rotation(self):
        pass

    def choose_direction(self, possible_directions):
        self.direction = possible_directions[0]

    def turn_left(self):
        self.direction *= 1j

    def turn_right(self):
        self.direction *= -1j
