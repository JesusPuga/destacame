from django.test import SimpleTestCase
from constants import publicKey

class GetPublicKeyHandlerTests(SimpleTestCase):

    def test_handler_renders_public_key(self):
        response = self.client.get('/get_public_key/')
        self.assertContains(response, publicKey, status_code=200)