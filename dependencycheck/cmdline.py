from .dependencies import get_dependencies
from .contract import get_contracts, ContractBroken
from .reporter import Reporter


def main():
    dependencies = get_dependencies()
    reporter = Reporter()
    for contract in get_contracts():
        try:
            contract.check_dependencies(dependencies)
        except ContractBroken as e:
            reporter.store_broken_contract(contract, e)
        else:
            reporter.store_successful_contract(contract)

    reporter.output_report()

    if reporter.has_broken_contracts:
        return 1  # Fail
    else:
        return 0  # Pass
