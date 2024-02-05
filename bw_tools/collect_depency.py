from time import time
from typing import Optional, Tuple

from bw2data.backends import Activity, ExchangeDataset

from bw_tools.find_ecoinvent import set_current_get_db, ECOINVENT_391_CUTOFF


def get_dependency(activitity: Activity,
                   max_level: Optional[int] = -1) -> Tuple[dict[str, int], dict[str, set[str]], list[int]]:
    """
    Get all nodes that are connected to the given node. (as inputs)
    :param max_level: max level to go down. -1 for infinite
    :return:
    """
    # all visited nodes (codes)
    visited: set[str] = set[str]()
    # keep a dict of code -> level
    level: dict[str, int] = dict()
    # keep a dict. code -> all input codes
    inputs: dict[str, set[str]] = dict()
    # nodes to visit next
    to_visit = {activitity["code"]}
    # nodes to visit in the next iteration
    # all exchanges (eventually filtered by type). just ids for memory efficiency
    all_exchanges: list[int] = []
    current_level: int = 0

    while len(to_visit) and max_level != 0:
        print("---")
        # get all exchanges that we could currently reach
        visited.update(to_visit)
        for v in to_visit:
            level[v] = current_level
            inputs[v] = set()
        exchanges = list(
            ExchangeDataset.select(ExchangeDataset).where(
                (ExchangeDataset.output_code.in_(to_visit)) &
                (ExchangeDataset.input_code.not_in(visited)) &
                (ExchangeDataset.input_code != ExchangeDataset.output_code)))
        to_visit.clear()
        # add nodes that we did not visit yet for the next iteration
        for exc in exchanges:
            all_exchanges.append(exc.id)

            to_visit.add(exc.input_code)
            inputs[exc.output_code].add(exc.input_code)

        print(f"visited: {len(visited)}, "
              f"total exchanges: {len(all_exchanges)}, "
              f"next nodes: {len(to_visit)}, ")
        max_level -= 1
        current_level += 1
    # sort by the second element of the tuple (level)
    return level, inputs, all_exchanges


if __name__ == "__main__":
    db = set_current_get_db(ECOINVENT_391_CUTOFF)
    activity = db.get("75b45f49f7ad440bdea35a8b57bdccbd")
    # print(activity["code"])
    total_t = time()
    res = get_dependency(activity)
    print(round(time() - total_t,2))
