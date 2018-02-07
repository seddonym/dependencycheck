from unittest import TestCase
from tests import mypackage, flowpackage
from tests.mypackage import foo, bar, mysubpackage
from tests.mypackage.mysubpackage import baz, foo as mysubpackage_foo
from tests.flowpackage import upstream, downstream_absolute, downstream_relative
import importlib
import networkx
import pkgutil

class DependencyPath:
    def __init__(self, steps):
        self.steps = steps


class ModuleGraph:
    def __init__(self, modules):
        self.modules = modules
        # Directed graph
        self._graph = networkx.DiGraph()

    def get_dependency_path(self, upstream, downstream):
        # Add to the graph all the dependencies of downstream
        self._add_dependencies_for_module(downstream)
        # Find the shortest path to upstream
        return self._get_shortest_path(upstream, downstream)

    def _add_dependencies_for_module(self, a_module):
        pass

    def _get_shortest_path(self, upstream, downstream):
        shortest_path = networkx.shortest_path(self._graph,
                                               source=upstream, target=downstream)
        path = DependencyPath(steps=shortest_path)
        return path


    @classmethod
    def get_modules_from_patterns(cls, patterns):
        modules = []
        for pattern in patterns:
            modules.append(importlib.import_module(pattern))
        return modules

    @classmethod
    def get_submodules_from_path(cls, a_module):
        return cls._import_submodules(a_module)

    @classmethod
    def _import_submodules(cls, package):
        """ Import all submodules of a module, recursively, including subpackages

        :param package: package (name or actual module)
        :type package: str | module
        :rtype: list[types.ModuleType]
        """
        if isinstance(package, str):
            package = importlib.import_module(package)
        results = []
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results.append(importlib.import_module(full_name))
            if is_pkg:
                results.extend(cls._import_submodules(full_name))
        return results





class TestGetModulesFromPatterns(TestCase):
    def test_success_no_wildcards(self):
        modules = ModuleGraph.get_modules_from_patterns(('tests.mypackage',))
        self.assertEqual(modules, [mypackage])

    # TODO wildcards, failures


class TestGetSubmodules(TestCase):
    def test_success(self):
        submodules = ModuleGraph.get_submodules_from_path(mypackage)
        self.assertEqual(submodules,
            [bar,
             foo,
             mysubpackage,
             baz,
             mysubpackage_foo])


class TestDependencyFlow(TestCase):
    def test_direct_import_absolute(self):
        graph = ModuleGraph(modules=[flowpackage])

        path = graph.get_dependency_path(upstream=upstream, downstream=downstream_absolute)
        self.assertEqual(path.steps, [upstream, downstream_absolute])
