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


def get_contracts():
    return [Contract()]