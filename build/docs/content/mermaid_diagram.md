<a id="mermaid_diagram"></a>

# mermaid\_diagram

Create a mermaid diagram (https://mermaid.js.org/) from activity relations.
Output is the insert
Diagram can be rendered here: https://mermaid.live in many mardown editors, pycharm markdown (with mermaid plugin installed)

<a id="mermaid_diagram.create_diagram"></a>

#### create\_diagram

```python
def create_diagram(activities: list[Activity],
                   for_markdown: bool = True) -> str
```

Create a mermaid diagram, with all activities and their exchanges between each other.

Activities are only included when they have a link to at least one other activity

**Arguments**:

- `activities`: brightway activity list
- `for_markdown`: if the output should be for markdown or pure mermaid

**Returns**:

a string, which can be written to a file

