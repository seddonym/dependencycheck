from pydeps.py2depgraph import py2dep


def get_dependencies():
    deps = py2dep('sample',
                 verbose=0,
                 show_cycles=False,
                 show_raw_deps=False,
                 noise_level=200,
                 max_bacon=200,
                 show_deps=False)
    return []


class DependencyGraph:
    
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
        return None