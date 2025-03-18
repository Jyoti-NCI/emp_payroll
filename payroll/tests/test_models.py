from mixer.backend.django import mixer
import pytest
@pytest.mark.django_db
class TestModels:
    def test_payroll_is_post_production_completed(self):
        payroll = mixer.blend('payroll.Employee', salary=5000)
        assert payroll.is_post_production_completed == True
    def test_payroll_is_not_post_production_completed(self):
        payroll = mixer.blend('payroll.Employee', salary=0)
        assert payroll.is_post_production_completed == False
    