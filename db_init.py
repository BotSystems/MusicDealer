from models import Area, Chanel, Download, db

# Connect to our database.
db.connect()

# Create the tables.
db.create_tables([Area, Chanel, Download])
