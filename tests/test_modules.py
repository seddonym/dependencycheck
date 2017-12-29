from unittest import TestCase
from tests import mypackage
from tests.mypackage import foo, bar, mysubpackage
from tests.mypackage.mysubpackage import baz, foo as mysubpackage_foo

import importlib
import pkgutil


class ModuleGraph:
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
        :rtype: dict[str, types.ModuleType]
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
