<a id="find_activities"></a>

# find\_activities

<a id="find_activities.find_activities_by_ids"></a>

#### find\_activities\_by\_ids

```python
def find_activities_by_ids(ids: list[int],
                           same_order: bool = True,
                           guarantee_all: bool = False) -> list[Activity]
```

Efficiently find a list of activities by their ids. Does not guarantee that all activities are retrieved, if some ids are missing.

**Arguments**:

- `ids`: ids to search for
- `same_order`: Same order as passed as parameter
- `guarantee_all`: Guarantee all activities are present

**Returns**:

list of bw activities

<a id="find_activities.find_activities_by_codes"></a>

#### find\_activities\_by\_codes

```python
def find_activities_by_codes(codes: list[str],
                             same_order: bool = True,
                             guarantee_all: bool = False) -> list[Activity]
```

Efficiently find a list of activities by their codes. Does not guarantee that all activities are retrieved,

if some codes are missing.

**Arguments**:

- `codes`: codes to search for
- `same_order`: Same order as passed as parameter
- `guarantee_all`: Guarantee all activities are present

**Returns**:

list of bw activities

