from unittest import mock, skip
import pytest
from dependencycheck.contract import Contract, Layer


class TestContractCheck:
    def test_kept_contract(self):
        contract = Contract(
            name='Foo contract',
            modules=(
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
            modules=(
                'foo',
            ),
            layers=(
                Layer('one'),
                Layer('two'),
                Layer('three'),
            ),
        )
        dep_graph = mock.Mock()
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
            modules=(
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
