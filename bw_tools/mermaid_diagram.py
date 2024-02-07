"""
Create a mermaid diagram (https://mermaid.js.org/) from activity relations.
Output is the insert
Diagram can be rendered here: https://mermaid.live in many mardown editors, pycharm markdown (with mermaid plugin installed)
"""
from typing import Iterable

from bw2data.backends import Activity, ActivityDataset, ExchangeDataset
from bw2data.backends import ExchangeDataset as Ex
from tqdm import tqdm


def _base_diagram_pre(for_markdown: bool) -> str:
    if for_markdown:
        return """```mermaid
flowchart LR

"""
    else:
        return """flowchart LR
"""


def _base_diagram_post(emission_key_strings: list[str],resources_key_strings:list[str], for_markdown:bool) -> str:
    em_class_str_lines = "\n".join(f"class {ak} biosphere" for ak in emission_key_strings)
    re_class_str_lines = "\n".join(f"class {ak} resource" for ak in resources_key_strings)
    class_activity_lines = f"\n".join([em_class_str_lines, re_class_str_lines])
    if for_markdown:
        return "\n" + class_activity_lines + f"""
classDef biosphere fill: #80d080
```"""
    else:
        return "\n" + class_activity_lines + f"""
classDef biosphere fill: #80d080
"""

def slow_exchange_search( activity_keys: list[tuple[str,str]]) -> set[ExchangeDataset]:
    all_codes = [i[1] for i in activity_keys]
    sub_res: set[ExchangeDataset] = set()
    for item in tqdm(activity_keys):
        all_res:Iterable[Ex] = Ex.select().where((Ex.input_database == item[0]) & (Ex.input_code == item[1]) |
                     (Ex.output_database == item[0]) & (Ex.output_code == item[1]))
        for res in all_res:
            if res.input_code == item[1] and res.output_code != item[1] and res.output_code in all_codes:
                sub_res.add(res)
    return sub_res


def create_diagram(activities: list[Activity], for_markdown: bool = True) -> str:
    """
    Create a mermaid diagram, with all activities and their exchanges between each other.
    Activities are only included when they have a link to at least one other activity
    :param activities: brightway activity list
    :param for_markdown: if the output should be for markdown or pure mermaid
    :return: a string, which can be written to a file
    """
    activity_keys: list[tuple[str,str]] = [a.key for a in activities]
    ks = lambda act: "_".join(act.key)
    activity_key_string_map = {
        ks(a): a["name"].replace("(","-").replace(")","-")
        for a in activities
    }
    if len(activity_keys) == 0:
        return _base_diagram_pre(for_markdown) + _base_diagram_post([], [],for_markdown)

    compound_query = None
    for item in activity_keys:
        sub_query = ((Ex.input_database == item[0]) & (Ex.input_code == item[1]) |
                     (Ex.output_database == item[0]) & (Ex.output_code == item[1]))
        compound_query = sub_query if compound_query is None else (compound_query | sub_query)

    try:
        results = list(Ex.select().where(compound_query))
    except RecursionError as err:
        results = slow_exchange_search(activity_keys)
    # print(len(results))
    included_activities = []
    result_str = _base_diagram_pre(for_markdown)
    for ex in results:
        in_str = f"{ex.input_database}_{ex.input_code}"
        out_str = f"{ex.output_database}_{ex.output_code}"
        in_md_str = in_str
        if in_str not in included_activities:
            in_md_str += f"({activity_key_string_map[in_str]})"
            included_activities.append(in_str)
        out_md_str = out_str
        if out_str not in included_activities:
            out_md_str += f"({activity_key_string_map[out_str]})"
            included_activities.append(out_str)
        result_str += f"{in_md_str} -- {ex.data['amount']} --> {out_md_str}\n"
    emissions = []
    resources = []
    for act in activities:
        _t = act.get("type")
        if _t == "emission":
            emissions.append(ks(act))
        elif _t == "natural resource":
            resources.append(ks(act))
    result_str += _base_diagram_post(emissions, resources, for_markdown)
    return result_str


if __name__ == "__main__":
    import bw2data

    bw2data.projects.set_current("nonlinear-method-test")
    db = bw2data.Database("db")
    open("diagram.md", "w").write(create_diagram(list(db), False))

