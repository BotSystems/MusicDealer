from models import Chanel, Download, db

# Connect to our database.
db.connect()

# Create the tables.
db.create_tables([Chanel, Download])
