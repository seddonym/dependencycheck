from .dependencies import get_dependencies
from .contract import Contract, ContractBroken
from .reporter import Reporter


def main():
    dependencies = get_dependencies()
    contract = Contract()
    try:
        contract.check_dependencies(dependencies)
    except ContractBroken as e:
        Reporter.report_broken_contract(e)
        return 1  # Fail
    else:
        Reporter.report_success()
        return 0  # Pass
