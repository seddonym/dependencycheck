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
                Layer('upstream'),
                Layer('downstream'),
            ),
        )
        dep_graph = mock.Mock()
        dep_graph.find_path.return_value = None

        contract.check_dependencies(dep_graph)

        dep_graph.find_path.assert_called_once_with(downstream='upstream',
                                                    upstream='downstream')

    def test_simple_break_raises_contract_broken(self):
        contract = Contract(
            name='Foo contract',
            modules=(
                'flowpackage',
            ),
            layers=(
                Layer('upstream'),
                Layer('downstream'),
            ),
        )
        dep_graph = mock.Mock()
        dep_graph.find_path.return_value = [
            'downstream',
        ]

        with pytest.raises(ContractBroken):
            contract.check_dependencies(dep_graph)

        dep_graph.find_path.assert_called_once_with(downstream='upstream',
                                                    upstream='downstream')