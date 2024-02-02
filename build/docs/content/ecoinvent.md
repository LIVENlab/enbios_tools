<a id="find_ecoinvent"></a>

# find\_ecoinvent

This package helps to quickly set the bw project to a certain ecoinvent dataset.
The base function **find_bw_ecoinvent_project** searches through all bw projects and their databases and looks
for specific activities that are only contained in the relevant ecoinvent dataset.
The 2 other function set the bw project (**set_current_project**) and directly return the corresponding ecoinvent (**set_current_get_db**).

Other ecoinvent versions/datasets can be added by adding
- a simple name Literal
- adding the code of a random activity of that dataset
- adding the Literal to the ECOINVENT_391 list

<a id="find_ecoinvent.ECOINVENT_391_CUTOFF"></a>

#### ECOINVENT\_391\_CUTOFF

ecoinvent version 3.9.1 cutoff

<a id="find_ecoinvent.ECOINVENT_391_CONSEQUENTIAL"></a>

#### ECOINVENT\_391\_CONSEQUENTIAL

ecoinvent version 3.9.1 consequential

<a id="find_ecoinvent.ECOINVENT_391_APOS"></a>

#### ECOINVENT\_391\_APOS

ecoinvent version 3.9.1 apos

<a id="find_ecoinvent.ECOINVENT_391"></a>

#### ECOINVENT\_391

Ecoinvent versions that can be used (one of the above Literals)

<a id="find_ecoinvent.find_bw_ecoinvent_project"></a>

#### find\_bw\_ecoinvent\_project

```python
def find_bw_ecoinvent_project(
        ecoinvent_database_type: ECOINVENT_391) -> Optional[tuple[str, str]]
```

Find the brightway project that matches the given ecoinvent

**Arguments**:

- `ecoinvent_database_type`: one of ECOINVENT_391

**Returns**:

tuple: [project name, database name]

<a id="find_ecoinvent.set_current_project"></a>

#### set\_current\_project

```python
def set_current_project(ecoinvent_database_type: ECOINVENT_391)
```

Set the current project to the brightway project with the given ecoinvent version, if it exists

**Arguments**:

- `ecoinvent_database_type`: one of ECOINVENT_391

<a id="find_ecoinvent.set_current_get_db"></a>

#### set\_current\_get\_db

```python
def set_current_get_db(
        ecoinvent_database_type: ECOINVENT_391
) -> bw2data.backends.SQLiteBackend
```

Set the current project to the brightway project with the given ecoinvent version and return the database

**Arguments**:

- `ecoinvent_database_type`: one of ECOINVENT_391

**Returns**:

The bw database object for the given ecoinvent version

