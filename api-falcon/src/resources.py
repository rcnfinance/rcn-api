from graceful.resources.generic import RetrieveUpdateAPI
from graceful.resources.generic import ListCreateAPI
import falcon
from serializers import LoanSerializer
from models import Loan


class LoanList(ListCreateAPI):
    serializer = LoanSerializer()

    def list(self, params, meta, **kwargs):
        return Loan.objects.all()

    def create(self, params, meta, validated, **kwargs):
        loan = Loan(**validated)
        loan.save()
        return loan


class LoanItem(RetrieveUpdateAPI):
    serializer = LoanSerializer()

    def retrieve(self, params, meta, loan_index, **kwargs):
        try:
            return Loan.objects.get(index=loan_index)
        except Loan.DoesNotExist:
            raise falcon.HTTPNotFound(title='Loan does not exists', description='Loan with index={} does not exists'.format(loan_index))

    def update(self, params, meta, loan_index, validated, **kwargs):
        try:
            loan = Loan.objects.get(index=loan_index)
            updated = loan.modify(**validated)
            if updated:
                return loan
        except Loan.DoesNotExist:
            raise falcon.HTTPNotFound(title='Loan does not exists', description='Loan with index={} does not exists'.format(loan_index))