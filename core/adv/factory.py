from core.adv.models import Adv


class Factory:
    @staticmethod
    def create(adv_data):
        return Adv(**adv_data)
