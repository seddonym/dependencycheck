import os
from dependencycheck.contract import get_contracts, Layer


def test_get_contracts():
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, '..', 'assets', 'singlecontractfile')

    contracts = get_contracts(path)

    assert len(contracts) == 2
    expected_contracts = [
        {
            'name': 'Contract One',
            'modules': ['foo', 'bar'],
            'layers': ['one', 'two'],
        },
        {
            'name': 'Contract Two',
            'modules': ['baz/*'],
            'layers': ['one', 'two', 'three'],
        },
    ]
    for contract_index, contract in enumerate(contracts):
        expected_data = expected_contracts[contract_index]
        assert contract.name == expected_data['name']

        for module_index, module in enumerate(contract.modules):
            expected_module_data = expected_data['modules'][module_index]
            assert module == expected_module_data

        for layer_index, layer in enumerate(contract.layers):
            expected_layer_data = expected_data['layers'][layer_index]
            assert isinstance(layer, Layer)
            assert layer.name == expected_layer_data
