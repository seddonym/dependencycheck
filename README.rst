TODO

- Read dependency graph
- Read contract yml
- Check adherence


python -m dependencycheck

Next:
 - Get get_dependency_path working. Investigate whether better to use modulegraph.ModuleGraph to work out dependencies (getReferences?) or wrap a networkx graph instead.


Create a directional graph.
Work down the submodule order contract.
For each submodule:
 - For each submodule below it:
   - Store number of steps required to get from parent to child (should be none)
Report shortest steps (define this more clearly)

TODO:
 - Make the rocky river style contract work. It should go through
 each module listed in the contract and look at the submodules as layers.
- Handle networkx.exception.NodeNotFound gracefully.
 - Then, only report the breakage once.
 - Make the layers style contract work. It should check that nothing within the
each layer imports from a layer above.
