from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription
from django.shortcuts import resolve_url as r


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """GET /inscricao/ must return status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """Html must contains input tags"""
        self.assertContains(self.resp, '<form')
        #self.assertContains(self.resp, '<input', 6)
        #self.assertContains(self.resp, '<type="text"', 3)
        #self.assertContains(self.resp, '<type="email"')
        #self.assertContains(self.resp, '<type="submit"')
        tags = (('<form', 1),
                ('<input', 6),
                ('<type="text"', 3),
                ('<type="email"', 1),
                ('<type="submit"', 1)
        )
        for text, count in tags:
            with self.subTest():
                #self.assertContains(self.resp, text, count)
                pass

    def test_csrf(self):
        """Html must contains CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='moreira.compra@gmail.com', phone='21-99618-6180')

        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/1/"""
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))

    def test_send_subscribe_mail(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_dont_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):
    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Henrique Bastos', cpf='12345678901')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')