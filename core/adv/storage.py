from random import choice


class Storage:
    factory = None
    advs = list()

    def __init__(self, factory):
        self.factory = factory

    def create(self, advs_data):
        for adv_data in advs_data:
            self.save(self.factory.create(adv_data))

    def save(self, adv):
        self.advs.append(adv)

    def get(self):
        return choice(self.advs)
