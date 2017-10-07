from core.area.models import Area
from core.chanel.models import Chanel
from core.database import db
from core.download.models import Download

db.connect()

# Create the tables.
db.create_tables([Area, Chanel, Download])
