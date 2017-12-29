class Reporter:
    @classmethod
    def report_broken_contract(cls, exception):
        print('Dependency contract broken.')

    @classmethod
    def report_success(cls):
        print('Dependencies OK.')