import yaml
import os


class ContractBroken(Exception):
    pass


class Layer:
    def __init__(self, name):
        self.name = name


class Contract:
    def __init__(self, name, modules, layers, recursive=False):
        self.name = name
        self.modules = modules
        self.layers = layers
        self.recursive = recursive

    def check_dependencies(self, dependencies):
        illegal_dependencies = []

        for upstream_layer in self.layers:
            downstream_layers = self._get_layers_downstream_of(upstream_layer)
            for downstream_layer in downstream_layers:
                path = dependencies.find_path(
                    upstream=downstream_layer.name,
                    downstream=upstream_layer.name)
                if path:
                    illegal_dependencies.append(path)
        if illegal_dependencies:
            raise ContractBroken

    def _get_layers_downstream_of(self, layer):
        return self.layers[self.layers.index(layer) + 1:]


def contract_from_yaml(key, data):
    layers = []
    for layer_data in data['layers']:
        layers.append(Layer(layer_data))

    return Contract(
        name=key,
        modules=data['modules'],
        layers=layers,
    )


def get_contracts(path):
    """Given a path to a project, read in any contracts from a contract.yml file.
    Args:
        path (string): the path to the project root.
    Returns:
        A list of Contract instances.
    """
    contracts = []

    file_path = os.path.join(path, 'contracts.yml')

    with open(file_path, 'r') as file:
        data_from_yaml = yaml.load(file)
        for key, data in data_from_yaml.items():
            contracts.append(contract_from_yaml(key, data))

    return contracts