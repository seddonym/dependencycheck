from unittest.mock import patch, Mock

from dependencycheck.dependencies import DependencyGraph


class TestDependencyGraph:
    SOURCES = {
        'one': Mock(
            imports=[],
        ),
        'two': Mock(
            imports=['one'],
        ),
        'three': Mock(
            imports=['two'],
        ),
        'four': Mock(
            imports=['three'],
        ),
    }

    def test_find_path_direct(self):
        with patch.object(DependencyGraph, '_generate_pydep_sources',
                          return_value=self.SOURCES):
            graph = DependencyGraph('foo')

        path = graph.find_path(upstream='one', downstream='two')

        assert path == ('one',)

    def test_find_path_indirect(self):
        with patch.object(DependencyGraph, '_generate_pydep_sources',
                          return_value=self.SOURCES):
            graph = DependencyGraph('foo')

        path = graph.find_path(upstream='one', downstream='four')

        assert path == ('three', 'two', 'one',)

    def test_find_path_nonexistent(self):
        with patch.object(DependencyGraph, '_generate_pydep_sources',
                          return_value=self.SOURCES):
            graph = DependencyGraph('foo')

        path = graph.find_path(upstream='four', downstream='one')

        assert path is None
