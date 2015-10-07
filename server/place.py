import logging


class Place:
    description = ""

    def __init__(self, id, name, **params):
        self.id = id
        self.name = name
        self.description = ""

    def __repr__(self):
        return "%s.\t%s\n\t%s" % (self.id, self.name, self.description)

    def serialize(self):
        return {"id": self.id, "name": self.name, "description": self.description}

    def use(self, player):
        print(player)


class DoubleTurn(Place):
    description = "Double turn"

    def use(self, player):
        Place.use(self, player)

        print("Double turn")
        logging.debug("Double")
        player.turn()


class Moving(Place):
    move_to = 1

    def __init__(self, **params):
        Place.__init__(self, **params)
        self.move_to = params['move_to']
        self.description = "Moving to %d" % (self.move_to)

    def use(self, player):
        Place.use(self, player)

        print("Going to %s" % (self.move_to))
        logging.debug("Redirect to %s" % (self.move_to))
        player.pos = self.move_to


class Restart(Place):
    description = "Restart game"

    def use(self, player):
        Place.use(self, player)

        print("Restarting race")
        logging.debug("Restart")
        player.start()
