from .base import BaseModel
from .country import Country


class City(BaseModel):
    table_name = 'city'
    columns = (
        'id',
        'name',
        'country_id',
    )

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"City: {self.name}"

    def get_country(self):
        return Country.get_by_id(self.country_id)

    @classmethod
    def info(cls, city_id=None):
        query = (
            "SELECT c.id, CONCAT(c.name, ' (', c2.code, ')') "
            "FROM city c "
            "INNER JOIN country c2 "
            "ON c.country_id=c2.id"
        )

        if city_id:
            query += f' WHERE c.id = {city_id}'

        query += ' ORDER BY c2.id, c.id'

        return cls.execute_query(query)
