import logging


class Game(object):
    """Basic game object"""
    finish = 120
    places = []
    players = []
    leaders = []
    turn = 0

    def start(self):
        logging.info("Starting game")
        self.generate()
        self.leaders = []
        for player in self.players:
            logging.info("Setting up player %s", player.id)
            player.start()
        self.turn = 0

    def newPlayer(self, id):
        from player import Player
        logging.info("Creating new player")
        logging.debug(id)
        self.players.append(Player(id, self))

    def nextTurn(self):
        self.turn += 1
        logging.info("Going to turn #%s", self.turn)

        turners = [player for player in self.players if not player.isFinished()]
        for player in turners:
            self.doTurn(player)

    def isFinished(self):
        finished = len(self.leaders) >= len(self.players)
        logging.debug("Finished %s.", finished)
        return finished

    def dice(self):
        import random
        roll = random.randint(1, 6)
        logging.debug("Rolled %s", roll)
        return roll

    def generate(self):
        logging.info("Generating field")
        self.places = []
        from place import Place
        self.places = [Place(i) for i in range(0, self.finish+1)]

    def doTurn(self, player):
        logging.info("Doing %s's turn:" % (player.id))
        player.roll()
        if player.pos == 7:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 14:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 21:
            logging.debug("Restart game")
            player.pos == 0
        elif player.pos == 24:
            print("Go to 52")
            player.pos == 52
        elif player.pos == 27:
            print("Go to 17")
            player.pos == 17
        elif player.pos == 31:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 47:
            print("Go to 61")
            player.pos = 61
        elif player.pos == 48:
            print("Go to 41")
            player.pos = 41
        elif player.pos == 51:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 58:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 68:
            print("Go to 55")
            player.pos = 55
        elif player.pos == 70:
            print("Go to 80")
            player.pos = 80
        elif player.pos == 71:
            print("Go to 62")
            player.pos = 62
        elif player.pos == 77:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 91:
            print("Go to 99")
            player.pos = 99
        elif player.pos == 95:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 100:
            print("Go to 46")
            player.pos = 46
        elif player.pos == 107:
            print("Go to 37")
            player.pos = 37
        elif player.pos == 109:
            logging.debug("Double")
            self.doTurn(player)
        elif player.pos == 113:
            logging.debug("Double")
            self.doTurn(player)

        if player.isFinished():
            if not(player in self.leaders):
                self.leaders.append(player)
