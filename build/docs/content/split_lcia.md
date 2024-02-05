<a id="split_lcia"></a>

# split\_lcia

<a id="split_lcia.split_characterized_inventory"></a>

#### split\_characterized\_inventory

```python
def split_characterized_inventory(
        lca: LCA,
        technosphere_activity_groups: list[list[int]],
        make_calculations: bool = True) -> list[csr_matrix]
```

Split the results of a lcia calculation into groups. Each group is a list of activities, specified by their ids.

Calculations of lci and lcia are performed when they are missing and `make_calculations` is set to `True`

**Arguments**:

- `lca`: bw LCA object
- `technosphere_activity_groups`: list of (technosphere) activity-groups, activities are specified by their 'id'
- `make_calculations`: make lci and lcia calculations if the corresponding matrices are missing

**Returns**:

a list of sparse matrices, which are characterized inventories split by the activity groups.
score can be calculated by calling `sum()` for any matrix.

