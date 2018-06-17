from .dependencies import get_dependencies
from .contract import get_contracts, ContractBroken
from .report import Report


def main():
    dependencies = get_dependencies()
    report = Report()
    for contract in get_contracts():
        contract.check_dependencies(dependencies)
        report.add_contract(contract)

    report.output()

    if report.has_broken_contracts:
        return 1  # Fail
    else:
        return 0  # Pass
