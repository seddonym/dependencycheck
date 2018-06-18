from unittest import mock, skip
import pytest
from dependencycheck.contract import Contract, Layer
import logging
import sys

logger = logging.getLogger('dependencycheck')
logging.getLogger('pydeps').setLevel(logging.ERROR)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class TestContractCheck:
    def test_kept_contract(self):
        contract = Contract(
            name='Foo contract',
            packages=(
                'foo',
            ),
            layers=(
                Layer('one'),
                Layer('two'),
                Layer('three'),
            ),
        )
        dep_graph = mock.Mock()
        dep_graph.find_path.return_value = None
        dep_graph.get_children.return_value = []

        contract.check_dependencies(dep_graph)

        assert contract.is_kept is True

        # Check that each of the possible disallowed imports were checked
        dep_graph.find_path.assert_has_calls((
            mock.call(downstream='foo.one', upstream='foo.two'),
            mock.call(downstream='foo.one', upstream='foo.three'),
            mock.call(downstream='foo.two', upstream='foo.three'),
        ))

    def test_broken_contract(self):
        contract = Contract(
            name='Foo contract',
            packages=(
                'foo',
            ),
            layers=(
                Layer('one'),
                Layer('two'),
                Layer('three'),
            ),
        )
        dep_graph = mock.Mock()
        dep_graph.get_children.return_value = []
        # Mock that one imports two and three, and two imports three
        dep_graph.find_path.side_effect = [
            None,
            ['foo.one', 'foo.two'],
            ['foo.one', 'foo.three'],
            ['foo.two', 'foo.three']
        ]

        contract.check_dependencies(dep_graph)

        assert contract.is_kept is False

        # Check that each of the possible disallowed imports are checked
        dep_graph.find_path.assert_has_calls((
            mock.call(downstream='foo.one', upstream='foo.two'),
            mock.call(downstream='foo.one', upstream='foo.three'),
            mock.call(downstream='foo.two', upstream='foo.three'),
        ))

    def test_unchecked_contract_raises_exception(self):
        contract = Contract(
            name='Foo contract',
            packages=(
                'foo',
            ),
            layers=(
                Layer('one'),
                Layer('two'),
                Layer('three'),
            ),
        )

        with pytest.raises(RuntimeError) as excinfo:
            contract.is_kept
        assert 'Cannot check whether contract is ' \
            'kept until check_dependencies is called.' in str(excinfo.value)

    def test_broken_contract_children(self):
        contract = Contract(
            name='Foo contract',
            packages=(
                'foo',
            ),
            layers=(
                Layer('one'),
                Layer('two'),
            ),
        )
        dep_graph = mock.Mock()
        # Mock some deeper submodules
        dep_graph.get_children.side_effect = [
            ['foo.one.alpha', 'foo.one.alpha.red', 'foo.one.alpha.green', 'foo.one.beta'],
            # For foo.one
            ['foo.two.gamma'],  # For foo.two
            ['foo.two.gamma'],  # For foo.two (second call)
        ]

        # Mock that foo.one.alpha.red imports foo.two.gamma
        dep_graph.find_path.side_effect = [
            None, None, None, None, None,
            ['foo.one.alpha.red', 'foo.two.gamma'],
            None, None, None, None
        ]

        contract.check_dependencies(dep_graph)

        assert contract.is_kept is False

        # Check that each of the possible disallowed imports are checked
        dep_graph.find_path.assert_has_calls((
            mock.call(downstream='foo.one', upstream='foo.two'),
            mock.call(downstream='foo.one', upstream='foo.two.gamma'),
            mock.call(downstream='foo.one.alpha', upstream='foo.two'),
            mock.call(downstream='foo.one.alpha', upstream='foo.two.gamma'),
            mock.call(downstream='foo.one.alpha.red', upstream='foo.two'),
            mock.call(downstream='foo.one.alpha.red', upstream='foo.two.gamma'),
            mock.call(downstream='foo.one.alpha.green', upstream='foo.two'),
            mock.call(downstream='foo.one.alpha.green', upstream='foo.two.gamma'),
            mock.call(downstream='foo.one.beta', upstream='foo.two'),
            mock.call(downstream='foo.one.beta', upstream='foo.two.gamma'),
        ))