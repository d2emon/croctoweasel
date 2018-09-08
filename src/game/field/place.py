import logging


class Place:
    def __init__(self, id, name, **params):
        self.id = id
        self.name = name
        self.description = ""

    def __str__(self):
        return "{:<4}{} {}".format(self.id, self.name, self.description)

    def __repr__(self):
        return str(self)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def action(self, game, player):
        print(player)


class DoubleTurn(Place):
    def __init__(self, id, name, **params):
        # super().__init__(id, name, **params)
        Place.__init__(self, id, name, **params)
        self.description = "Double turn"

    def action(self, game, player):
        # super().action(player)
        Place.action(self, game, player)

        print("Double turn")
        logging.debug("Double")
        game.move_player_by(player)


class Moving(Place):
    move_to = 1

    def __init__(self, id, name, **params):
        # super().__init__(id, name, **params)
        Place.__init__(self, id, name, **params)
        self.move_to = params['move_to']
        self.description = "Moving to {}".format(self.move_to)

    def action(self, game, player):
        # super().action(player)
        Place.action(self, game, player)

        print("Going to {}" .format(self.move_to))
        logging.debug("Redirect to %s", self.move_to)
        player.pos = self.move_to


class Restart(Place):
    def __init__(self, id, name, **params):
        # super().__init__(id, name, **params)
        Place.__init__(self, id, name, **params)
        self.description = "Restart game"

    def action(self, game, player):
        # super().action(game, player)
        Place.action(self, game, player)

        print("Restarting race")
        logging.debug("Restart")
        player.start()


place_types = (Place, DoubleTurn, Moving, Restart)


def place_from_data(place_id, **kwargs):
    kwargs['id'] = place_id
    place_class = place_types[kwargs.get('type', 0)]
    return place_class(**kwargs)
