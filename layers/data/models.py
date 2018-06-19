class Complaint:
    def get_bill(self):
        from ..domain import billing
        return billing.Bill()
