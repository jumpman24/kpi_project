from database import execute_query
from models import Rank
from typing import List


def select_rank(rid: int = None) -> List[Rank]:
    query = "SELECT id, name, abbreviate FROM rank"

    if rid:
        query += f" WHERE id = {rid}"

    result = execute_query(query)

    ranks = []
    for rank_id, name, abbreviate in result:
        rank = Rank(rank_id, name, abbreviate)
        ranks.append(rank)

    return ranks
