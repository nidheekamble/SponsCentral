from SponsCentral import db
from SponsCentral.models import Region
db.create_all()

reg = "regionsData.csv"
file = open(reg, "r")
data = file.readlines()

regList = []
for line in data:
	line = line.strip()
	regList.append(line.split(','))

#print(regList)

i = 1 #for the region id
for field in regList:
	region = Region(region_id=i, region_name=field[0], state="Maharashtra", city="Bombay", latitude=field[1], longitude=field[2])
	db.session.add(region)
	db.session.commit()
	i+=1

Region.query.all()
