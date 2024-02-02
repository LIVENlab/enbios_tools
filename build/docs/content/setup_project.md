<a id="setup_project"></a>

# setup\_project

This package has just one function for setting up a brightway project with a evoincent database

<a id="setup_project.safe_setup_ecoinvent"></a>

#### safe\_setup\_ecoinvent

```python
def safe_setup_ecoinvent(project_name: str,
                         ecoinvent_db_path: str,
                         db_name: str,
                         delete_project: bool = False,
                         delete_if_unlinked: bool = True)
```

Initiate a project with a ecoinvent database

**Arguments**:

- `project_name`: new project name
- `ecoinvent_db_path`: dataset path of the ecoinvent database
- `db_name`: name of the new database containing the ecoinvent database
- `delete_project`: Delete existing project
- `delete_if_unlinked`: Delete project if linking didn't work

