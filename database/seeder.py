import database as db
from models.crumb import Crumb

session = db.Session()

for num in range(0, 100):
    session.add(Crumb())

session.commit()
