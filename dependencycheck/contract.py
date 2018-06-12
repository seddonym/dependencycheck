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
        path = dependencies.find_path(upstream=self.layers[1].name,
                                      downstream=self.layers[0].name)
        if path:
            raise ContractBroken


def get_contracts():
    return [Contract()]