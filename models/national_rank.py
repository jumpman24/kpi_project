from .base import BaseModel


class NationalRank(BaseModel):
    table_name = 'national_rank'
    columns = (
        'id',
        'name',
        'abbreviate',
    )

    def __str__(self):
        return f"{self.abbreviate}"
