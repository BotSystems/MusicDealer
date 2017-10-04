from models import Chanel, Download, Area, db

# Connect to our database.
db.connect()

# Create the tables.
db.create_tables([Chanel, Download, Area])
