class Place:
    def __init__(self, id):
        self.id = id

    def use(self, player):
        print("%s is at %s" % (player.id, self.id))
        pass
