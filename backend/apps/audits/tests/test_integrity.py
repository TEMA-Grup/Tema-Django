import pytest
from apps.companies.models import Company
from apps.clients.models import Client
from apps.audits.models import Audit
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_reference_increments_per_company():
    c = Company.objects.create(name="A")
    d = Company.objects.create(name="B")
    cl1 = Client.objects.create(company=c, name="C1")
    cl2 = Client.objects.create(company=d, name="D1")
    a1 = Audit.objects.create(company=c, client=cl1, name="X")
    a2 = Audit.objects.create(company=c, client=cl1, name="Y")
    b1 = Audit.objects.create(company=d, client=cl2, name="Z")
    assert a1.reference != a2.reference
    assert a1.reference != b1.reference

@pytest.mark.django_db
def test_client_company_must_match_audit_company():
    c1 = Company.objects.create(name="C1")
    c2 = Company.objects.create(name="C2")
    cl = Client.objects.create(company=c1, name="CL")
    a = Audit(company=c2, client=cl, name="Bad")
    with pytest.raises(ValidationError):
        a.full_clean()