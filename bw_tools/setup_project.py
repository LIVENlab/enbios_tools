"""
This package has just one function for setting up a brightway project with a evoincent database
"""
from pathlib import Path

import bw2data
import bw2io
from bw2io import SingleOutputEcospold2Importer


def safe_setup_ecoinvent(project_name: str,
                         ecoinvent_db_path: str,
                         db_name: str,
                         delete_project: bool = False,
                         delete_if_unlinked: bool = True):
    """
    Initiate a project with a ecoinvent database
    :param project_name: new project name
    :param ecoinvent_db_path: dataset path of the ecoinvent database
    :param db_name: name of the new database containing the ecoinvent database
    :param delete_project: Delete existing project
    :param delete_if_unlinked: Delete project if linking didn't work
    :return:
    """
    if project_name in bw2data.projects:
        if delete_project:
            bw2data.projects.delete_project(project_name, True)
        raise KeyError(f"Project '{project_name}' already exists")
    db_path = Path(ecoinvent_db_path)
    spold_files_glob = db_path.glob("*.spold")
    if not db_path.exists:
        raise FileNotFoundError(f"{ecoinvent_db_path} does not exist")
    if not next(spold_files_glob):
        raise KeyError(f"There are no spold files in {ecoinvent_db_path}")
    bw2data.projects.create_project(project_name)
    bw2data.projects.set_current(project_name)
    bw2io.bw2setup()

    imported = SingleOutputEcospold2Importer(ecoinvent_db_path, db_name)
    imported.apply_strategies()
    # print(type(imported))
    if imported.all_linked:
        imported.write_database()
    else:
        if delete_if_unlinked:
            bw2data.projects.delete_project(project_name, True)
        else:
            imported.write_unlinked(f"{db_name}_unlinked")


if __name__ == "__main__":
    # safe_setup_ecoinvent("ecoinvent_391_consequential",
    #                     "data/ecoinvent/ecoinvent 3.9.1_consequential_ecoSpold02/datasets",
    #                      "ecoinvent_391_consequential")
    pass
