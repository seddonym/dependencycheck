from unittest import mock
import pytest
from dependencycheck.contract import Contract, Layer, ContractBroken

class TestGetContracts:
    pass


class TestContractCheck:
    def test_simple_adherence_does_not_raise_exception(self):
        contract = Contract(
            name='Foo contract',
            modules=(
                'flowpackage',
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

        # Check that each of the possible transgressive imports are checked
        dep_graph.find_path.assert_has_calls((
            mock.call(downstream='one', upstream='two'),
            mock.call(downstream='one', upstream='three'),
            mock.call(downstream='two', upstream='three'),
        ))

    def test_simple_break_raises_contract_broken(self):
        contract = Contract(
            name='Foo contract',
            modules=(
                'flowpackage',
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
            ['one'],
            ['one'],
            ['two']
        ]

        with pytest.raises(ContractBroken):
            contract.check_dependencies(dep_graph)

        # Check that each of the possible transgressive imports are checked
        dep_graph.find_path.assert_has_calls((
            mock.call(downstream='one', upstream='two'),
            mock.call(downstream='one', upstream='three'),
            mock.call(downstream='two', upstream='three'),
        ))
