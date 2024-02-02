"""
This package helps to quickly set the bw project to a certain ecoinvent dataset.
The base function **find_bw_ecoinvent_project** searches through all bw projects and their databases and looks
for specific activities that are only contained in the relevant ecoinvent dataset.
The 2 other function set the bw project (**set_current_project**) and directly return the corresponding ecoinvent (**set_current_get_db**).

Other ecoinvent versions/datasets can be added by adding
- a simple name Literal
- adding the code of a random activity of that dataset
- adding the Literal to the ECOINVENT_391 list

"""
from typing import Literal, Optional

import bw2data
from bw2data.errors import UnknownObject

ECOINVENT_391_CUTOFF = Literal["ECOINVENT_391_cutoff"]  # ecoinvent version 3.9.1 cutoff
ECOINVENT_391_CONSEQUENTIAL = Literal["ECOINVENT_391_consequential"]  # ecoinvent version 3.9.1 consequential
ECOINVENT_391_APOS = Literal["ECOINVENT_391_apos"]  # ecoinvent version 3.9.1 apos

_random_db_activities = {
    ECOINVENT_391_CUTOFF: 'bf0e87b03dc559621b618208aca6f708',
    ECOINVENT_391_CONSEQUENTIAL: '2a8404c1200201231df3a5ce52f9e11e',
    ECOINVENT_391_APOS: '34a77aa7741b325e862d6bda603af353'
}

ECOINVENT_391 = [ECOINVENT_391_CUTOFF, ECOINVENT_391_APOS,
                 ECOINVENT_391_CONSEQUENTIAL]  # Ecoinvent versions that can be used (one of the above Literals)


def find_bw_ecoinvent_project(ecoinvent_database_type: ECOINVENT_391) -> Optional[tuple[str, str]]:
    """
    Find the brightway project that matches the given ecoinvent
    :param ecoinvent_database_type: one of ECOINVENT_391
    :return: tuple: [project name, database name]
    """
    all_projects = bw2data.projects
    for project in all_projects:
        bw2data.projects.set_current(project.name)
        # print(f"project: {project.name}")
        databases = bw2data.databases
        if not databases:  # for the debugger... :/
            continue
        for database in databases:
            # print(f" - {database}")
            db: bw2data.backends.SQLiteBackend = bw2data.Database(database)
            if not db.metadata.get("format") == 'Ecoinvent XML':
                continue
            try:
                db.get(_random_db_activities.get(ecoinvent_database_type))
                # print(project.name, databases)
                return project.name, database
            except UnknownObject:
                pass


def set_current_project(ecoinvent_database_type: ECOINVENT_391):
    """
    Set the current project to the brightway project with the given ecoinvent version, if it exists
    :param ecoinvent_database_type: one of ECOINVENT_391
    """
    project, db = find_bw_ecoinvent_project(ecoinvent_database_type)
    if not project:
        raise ValueError(f"BW project using {ecoinvent_database_type} not found")
    print(f"Setting current project to '{project}', which has the ecoinvent db: '{db}'")
    bw2data.projects.set_current(project)


def set_current_get_db(ecoinvent_database_type: ECOINVENT_391) -> bw2data.backends.SQLiteBackend:
    """
    Set the current project to the brightway project with the given ecoinvent version and return the database
    :param ecoinvent_database_type: one of ECOINVENT_391
    :return: The bw database object for the given ecoinvent version
    """
    project, db = find_bw_ecoinvent_project(ecoinvent_database_type)
    if not project:
        raise ValueError(f"BW project using {ecoinvent_database_type} not found")
    bw2data.projects.set_current(project)
    return bw2data.Database(db)
