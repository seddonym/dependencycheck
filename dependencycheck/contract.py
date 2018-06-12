class ContractBroken(Exception):
    pass


class Contract:
    def check_dependencies(self, dependencies):
        pass


def get_contracts():
    return [Contract()]