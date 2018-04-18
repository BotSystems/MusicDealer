import unittest

from core.area.models import Area
from core.chanel.models import Chanel
from dotenv import load_dotenv
from core.storage.models import Storage
# import core.database



class TestStorage(unittest.TestCase):
    #
    # def setUpClass(cls):
    #     pass

    # def test_upper(self):
    #     storage = Storage('@md_music')
    #     self.assertEqual(storage.name, '@md_music')

    def testIfLinkNotExistShouldUseFinderStrategy(self):
        for facility in Storage.select():
            print(facility.name)

    def testIfLinkNotExistShouldUseFrowardStrategy(self):
        pass


if __name__ == '__main__':
    unittest.main()
