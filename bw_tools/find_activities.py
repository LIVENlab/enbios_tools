from typing import Iterable, Optional

from bw2data.backends import Activity, ActivityDataset
from bw2data.backends import ActivityDataset as ADS


def _convert_to_activities(activities_ds: Iterable[ADS]) -> list[Activity]:
    return list(Activity(a) for a in activities_ds)


def _guarantee_activities(activities_ds: Iterable[ADS], *,
                          ids: Optional[list[int]] = None,
                          codes: Optional[list[str]] = None) -> bool:
    """

    TODO needs testing
    :param activities_ds:
    :param ids:
    :param codes:
    :return:
    """
    assert (ids is not None) ^ (codes is not None)
    assert len(list(activities_ds)) == len(ids or codes)
    if ids:
        contained_ids = sorted(list(a.id for a in activities_ds))
        if not sorted(ids) == contained_ids:
            print(f"missing activity ids {set(ids) - set(contained_ids)}")
            return False
        return True
    else:
        contained_codes = sorted(list(a.code for a in activities_ds))
        if not sorted(ids) == contained_codes:
            print(f"missing activity codes {set(ids) - set(contained_codes)}")
            return False
        return True


def find_activities_by_ids(ids: list[int],
                               same_order: bool = True,
                               guarantee_all: bool = False) -> list[Activity]:
        """
        Efficiently find a list of activities by their ids. Does not guarantee that all activities are retrieved, if some ids are missing.
        :param ids: ids to search for
        :param same_order: Same order as passed as parameter
        :param guarantee_all: Guarantee all activities are present
        :return: list of bw activities
        """
        activities_ds = ADS.select().where(ADS.id.in_(ids))
        if guarantee_all:
            _guarantee_activities(activities_ds, ids=ids)
        if same_order:
            return _convert_to_activities(sorted(activities_ds, key=lambda a: ids.index(a.id)))
        else:
            return _convert_to_activities(activities_ds)


def find_activities_by_codes(codes: list[str], same_order: bool = True, guarantee_all: bool = False) -> list[
        Activity]:
        """
        Efficiently find a list of activities by their codes. Does not guarantee that all activities are retrieved,
        if some codes are missing.
        :param codes: codes to search for
        :param same_order: Same order as passed as parameter
        :param guarantee_all: Guarantee all activities are present
        :return: list of bw activities
        """
        activities_ds: Iterable[ADS] = ADS.select().where(ADS.code.in_(codes))
        if guarantee_all:
            _guarantee_activities(activities_ds, codes=codes)
        if same_order:
            return _convert_to_activities(sorted(activities_ds, key=lambda a: codes.index(a.code)))
        else:
            return _convert_to_activities(activities_ds)
