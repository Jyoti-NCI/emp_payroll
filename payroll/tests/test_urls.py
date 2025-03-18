from django.urls import reverse, resolve
class TestUrls:
    def test_allemployees_url(self):
        path = reverse('payroll:allemployees', kwargs={})
        assert resolve(path).view_name == 'payroll:allemployees'
        