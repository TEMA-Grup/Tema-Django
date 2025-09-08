import pytest_lazyfixture
from apps.companies.models import Company
from apps.clients.models import Client
from apps.audits.models import Audit

@pytest.mark.django_db
def test_reference_auto_increments():
    c = Company.objects.create(name="T1")
    cl = Client.objects.create(company=c, name="M1")
    a1 = Audit.objects.create(company=c, client=cl, name="Denetim 1")
    a2 = Audit.objects.create(company=c, client=cl, name="Denetim 1")
    assert a1.reference != a2.reference