import yaml
import os
import logging


logger = logging.getLogger(__name__)


class Layer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self)


class Contract:
    def __init__(self, name, modules, layers, recursive=False):
        self.name = name
        self.modules = modules
        self.layers = layers
        self.recursive = recursive

    def check_dependencies(self, dependencies):
        self.illegal_dependencies = []

        logger.debug('Checking dependencies for contract {}...'.format(self))

        for module in self.modules:
            logger.debug("Module '{}':".format(module))
            for upstream_layer in self.layers:

                upstream_module = "{}.{}".format(module, upstream_layer.name)

                downstream_layers = self._get_layers_downstream_of(upstream_layer)
                for downstream_layer in downstream_layers:
                    downstream_module = "{}.{}".format(module, downstream_layer.name)
                    path = dependencies.find_path(
                        upstream=downstream_module,
                        downstream=upstream_module)
                    if path:
                        logger.debug('Illegal dependency found: '.format(path))
                        self.illegal_dependencies.append(path)

    @property
    def is_kept(self):
        try:
            return len(self.illegal_dependencies) == 0
        except AttributeError:
            raise RuntimeError(
                'Cannot check whether contract is kept '
                'until check_dependencies is called.'
            )

    def _get_layers_downstream_of(self, layer):
        return self.layers[self.layers.index(layer) + 1:]

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self)


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