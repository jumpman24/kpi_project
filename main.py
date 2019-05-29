from models import *

cities = City.select(id=634, name='Харків')
print(cities[0].get_country())
