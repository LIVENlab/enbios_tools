from typing import Literal, Optional

from bw2calc import LCA
from bw2calc.dictionary_manager import DictionaryManager
from bw2data.backends import ActivityDataset
from pandas import DataFrame

from bw_tools.split_lcia import _check_lca


def inventory2labeled_df(lca: LCA,
                         matrix: Literal["inventory", "characterized_inventory"] = "characterized_inventory",
                         biosphere_subset: Optional[list[str]] = None,
                         technosphere_subset: Optional[list[str]] = None,
                         alternative_dict_manager: Optional[DictionaryManager] = None) -> DataFrame:
    """
    Turn LCA inventory or characterized inventory matrix into a DataFrame with labels corresponding to the activity names.
    Lists of biosphere and technosphere activities can be passed in order to have a slice of the dataframe
    :param lca:
    :param matrix:
    :param biosphere_subset:
    :param technosphere_subset:
    :return:
    """
    _check_lca(lca)

    df = DataFrame(getattr(lca, matrix).toarray())
    if alternative_dict_manager:
        dict_manager: DictionaryManager = alternative_dict_manager
    else:
        dict_manager = lca.dicts
    # map id -> name
    bio_map = {a.id: a.name for a in
               ActivityDataset.select().where(ActivityDataset.id.in_(list(dict_manager.biosphere.keys())))}
    techno_map = {a.id: a.name for a in
                  ActivityDataset.select().where(ActivityDataset.id.in_(list(dict_manager.activity.keys())))}

    # map idx -> name
    idx_bio_map = {k: bio_map[v] for k, v in dict(dict_manager.biosphere.reversed).items()}
    idx_techno_map = {k: techno_map[v] for k, v in dict(dict_manager.activity.reversed).items()}

    df.rename(index=idx_bio_map, inplace=True)
    df.rename(columns=idx_techno_map, inplace=True)

    # slice as : , if None is passed
    biosphere_subset = biosphere_subset if biosphere_subset is not None else slice(None)
    technosphere_subset = technosphere_subset if technosphere_subset is not None else slice(None)

    df = df.loc[biosphere_subset, technosphere_subset]
    return df
