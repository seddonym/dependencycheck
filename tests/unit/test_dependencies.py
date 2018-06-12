from dependencycheck.dependencies import DependencyGraph


class TestDependencyGraph:
    def test_find_path_direct(self):
        graph = DependencyGraph()

        path = graph.find_path(upstream='one', downstream='two')

        assert path == ('one',)

    def test_find_path_indirect(self):
        graph = DependencyGraph()

        path = graph.find_path(upstream='one', downstream='four')

        assert path == ('three', 'two', 'one',)

    def test_find_path_nonexistent(self):
        graph = DependencyGraph()

        path = graph.find_path(upstream='one', downstream='four')

        assert path is None
