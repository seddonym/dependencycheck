from pydeps.py2depgraph import py2dep
import networkx
from networkx.algorithms import shortest_path


def get_dependencies(package_name):
    return DependencyGraph(package_name)


class DependencyGraph:
    def __init__(self, package_name):
        self.package_name = package_name
        sources = self._generate_pydep_sources()
        self._build_networkx_graph_from_sources(sources)

    def _generate_pydep_sources(self):
        pydep_graph = py2dep(
            self.package_name,
            verbose=0,
            show_cycles=False,
            show_raw_deps=False,
            noise_level=200,
            max_bacon=200,
            show_deps=False,
        )
        self._pydep_graph = pydep_graph
        return pydep_graph.sources

    def _build_networkx_graph_from_sources(self, sources):
        self._networkx_graph = networkx.DiGraph()
        for module_name, source in sources.items():
            # self._networkx_graph.add_node(module_name)
            for upstream_module in source.imports:
                self._networkx_graph.add_edge(module_name, upstream_module)

    def find_path(self, downstream, upstream):
        """
        Args:
            downstream (string) - absolute name of module.
            upstream (string)- absolute name of module.
        Returns:
            List of module names showing the dependency path between
            the downstream and the upstream module, or None if there
            is no dependency.

            For example, given an upstream module 'alpha' and a downstream
            module 'delta':

                - ['alpha'] will be returned if delta directly imports alpha.
                - ['gamma', 'beta', 'alpha'] will be returned if delta imports
                  gamma, which imports beta, which imports alpha.
        """
        try:
            path = shortest_path(self._networkx_graph, downstream, upstream)
        except networkx.NetworkXNoPath:
            return None
        else:
            return tuple(path[1:])
