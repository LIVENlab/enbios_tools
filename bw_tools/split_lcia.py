from typing import Optional, Literal

import bw2data
from bw2calc import LCA
from bw2calc.dictionary_manager import DictionaryManager
from scipy.sparse import csr_matrix

from bw_tools.find_ecoinvent import ECOINVENT_391_CUTOFF, set_current_get_db


def _check_lca(lca: LCA, make_calculations: bool = True,
               inventory_name: Literal["inventory", "characterized_inventory"] = "inventory"):
    if not hasattr(lca, "inventory"):
        if make_calculations:
            print("calculating inventory")
            lca.lci()
        else:
            raise ValueError("Must do lci first")
    if inventory_name == "inventory":
        return

    if not hasattr(lca, "characterization_matrix"):
        print("loading lcia data")
        lca.load_lcia_data()

    if not hasattr(lca, "characterized_inventory"):
        if make_calculations:
            print("calculating lcia")
            lca.lcia()
        else:
            raise ValueError("Must do lcia first")


def split_inventory(lca: LCA,
                    technosphere_activities: list[int],
                    inventory_name: Literal["inventory", "characterized_inventory"] = "inventory",
                    make_calculations: bool = True) -> csr_matrix:
    """
    Split the results of a lcia calculation into groups. Each group is a list of activities, specified by their ids.
    Calculations of lci and lcia are performed when they are missing and `make_calculations` is set to `True`
    :param lca: bw LCA object
    :param technosphere_activities: list of (technosphere) activity-groups, activities are specified by their 'id'
    :param make_calculations: make lci and lcia calculations if the corresponding matrices are missing
    :return: a list of sparse matrices, which are characterized inventories split by the activity groups.
    score can be calculated by calling `sum()` for any matrix.
    """
    _check_lca(lca, make_calculations, inventory_name)
    inventory = getattr(lca, inventory_name)
    # do matrix multiplication for each final location
    return inventory[:, [lca.dicts.activity[c] for c in technosphere_activities]]


def split_characterized_inventory(lca: LCA,
                                  technosphere_activity_groups: list[list[int]],
                                  make_calculations: bool = True) -> list[
    csr_matrix]:
    """
    Split the results of a lcia calculation into groups. Each group is a list of activities, specified by their ids.
    Calculations of lci and lcia are performed when they are missing and `make_calculations` is set to `True`
    :param lca: bw LCA object
    :param technosphere_activity_groups: list of (technosphere) activity-groups, activities are specified by their 'id'
    :param make_calculations: make lci and lcia calculations if the corresponding matrices are missing
    :return: a list of sparse matrices, which are characterized inventories split by the activity groups.
    score can be calculated by calling `sum()` for any matrix.
    """
    _check_lca(lca, make_calculations)

    results: list[csr_matrix] = []
    # do matrix multiplication for each final location
    for activities in technosphere_activity_groups:
        results.append(
            lca.characterized_inventory[:, [lca.dicts.activity[c] for c in activities]]
        )

    return results


def subset_lcia(lca: LCA,
                technosphere_activities: Optional[list[int]] = None,
                biosphere_activities: Optional[list[int]] = None,
                make_calculations: bool = True) -> csr_matrix:
    _check_lca(lca, make_calculations)
    return lca.characterized_inventory[
        [lca.dicts.biosphere[c] for c in biosphere_activities] if biosphere_activities else slice(None),
        [lca.dicts.activity[c] for c in technosphere_activities] if technosphere_activities else slice(None)]


def _subset_matrix(matrix: csr_matrix,
                   dicts:DictionaryManager,
                   col_ids: Optional[list[int]] = None,
                   row_ids: Optional[list[int]] = None) -> csr_matrix:
    return matrix[
        [dicts.biosphere[c] for c in row_ids] if row_ids else slice(None),
        [dicts.activity[c] for c in col_ids] if col_ids else slice(None)]

def remove_zero_rows(matrix: csr_matrix, dicts: DictionaryManager) -> tuple[csr_matrix, DictionaryManager]:
    activity_ids = []
    reverse_bio_dict = dicts.biosphere.reversed
    for row_idx, row_value in enumerate(matrix.sum(0)):
        if row_value[0, 0] != 0.0:
            activity_ids.append(reverse_bio_dict[row_idx])
    subset_csr = _subset_matrix(matrix, row_ids=activity_ids)
    subset_dicts_ = subset_dicts(lca, biosphere_activities=activity_ids)
    return subset_csr, subset_dicts_


def remove_zero_cols(matrix: csr_matrix, dicts: DictionaryManager) -> tuple[csr_matrix, DictionaryManager]:
    activity_ids = []
    reverse_bio_dict = dicts.biosphere.reversed
    for col_idx, col_value in enumerate(matrix.sum(0)):
        if col_value[0, 0] != 0.0:
            activity_ids.append(reverse_bio_dict[col_idx])
    subset_csr = _subset_matrix(matrix, dicts, col_ids=activity_ids)
    subset_dicts_ = _subset_dicts(dicts, col_ids=activity_ids)
    return subset_csr, subset_dicts_


def _subset_dicts(dicts: DictionaryManager,
                  col_ids: Optional[list[int]] = None,
                  row_ids: Optional[list[int]] = None) -> DictionaryManager:
    new_dicts = DictionaryManager()
    for k in dicts:
        setattr(new_dicts, k, getattr(dicts, k).original)

    for map_name, activities in [("biosphere", row_ids),
                                 ("activity", col_ids)]:
        if activities:
            map_ = getattr(new_dicts, map_name)
            slice = list(filter(lambda i: i[1] in activities, sorted(map_.reversed.items())))
            setattr(new_dicts, map_name, {act_id[1]: idx for idx, act_id in enumerate(slice)})
    return new_dicts

def subset_dicts(lca,
                 technosphere_activities: Optional[list[int]] = None,
                 biosphere_activities: Optional[list[int]] = None,
                 make_calculations: bool = True) -> DictionaryManager:
    new_dicts = DictionaryManager()
    for k in lca.dicts:
        setattr(new_dicts, k, getattr(lca.dicts, k).original)

    for map_name, activities in [("biosphere", biosphere_activities),
                                 ("activity", technosphere_activities)]:
        if activities:
            map_ = getattr(new_dicts, map_name)
            slice = list(filter(lambda i: i[1] in activities, sorted(map_.reversed.items())))
            setattr(new_dicts, map_name, {act_id[1]: idx for idx, act_id in enumerate(slice)})
    return new_dicts

if __name__ == "__main__":
    db = set_current_get_db(ECOINVENT_391_CUTOFF)
    method = bw2data.methods.random()
    print(method)
    activity = db.random()
    print(activity)
    _lca = LCA({activity: 1}, method=method)
    x = split_characterized_inventory(_lca, [[18000, 18001, 18002, 18003]])
    print(x[0].toarray(), x[0].sum())

    _lca = LCA({activity: 1}, method=method)
    _lca.lci()
    _lca.lcia()
    mm = _lca.characterized_inventory[:, [_lca.dicts.activity[c] for c in [18000, 18001, 18002, 18003]]]
    print(mm.toarray(), mm.sum())
