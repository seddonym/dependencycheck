class Reporter:
    def __init__(self):
        self.has_broken_contracts = False

    def store_broken_contract(self, contract, exception):
        self.has_broken_contracts = True

    def store_successful_contract(self, contract):
        pass

    def output_report(self):
        if self.has_broken_contracts:
            print('Dependency contract broken.')
        else:
            print('Dependencies OK.')
