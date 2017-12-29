TODO

- Read dependency graph
- Read contract yml
- Check adherence


python -m dependencycheck


Create a directional graph.
Work down the submodule order contract.
For each submodule:
 - For each submodule below it:
   - Store number of steps required to get from parent to child (should be none)
Report shortest steps (define this more clearly)