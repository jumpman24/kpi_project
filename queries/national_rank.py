from database import execute_query
from models import NationalRank
from typing import List


def select_national_rank(rid: int = None) -> List[NationalRank]:
    query = "SELECT id, name, abbreviate FROM national_rank"

    if rid:
        query += f" WHERE id = {rid}"

    result = execute_query(query)

    national_ranks = []
    for national_rank_id, name, abbreviate in result:
        national_rank = NationalRank(national_rank_id, name, abbreviate)
        national_ranks.append(national_rank)

    return national_ranks
