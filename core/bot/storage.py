class Storage:
    factory = None
    bots = {}

    def __init__(self, factory):
        self.factory = factory

    def create(self, areas):
        for area in areas:
            self.save(self.factory.create(area))

    def save(self, bot):
        self.bots[bot.token] = bot

    def get(self, token):
        return self.bots[token]
