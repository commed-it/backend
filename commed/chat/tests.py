from django.test import TestCase
from .consumers import is_the_message_correct

# Create your tests here.
class MessageIsCorrect(TestCase):

    def test_is_message_correct(self):
        message_example = {
            'type': 'message',
            'message': '''Some large string that nobody wants to comment about.'''
        }
        self.assertTrue(is_the_message_correct(message_example))

    def test_is_formal_offer_correct(self):
        formal_offer_example = {
            'type': 'formalOffer',
            'formalOffer': 3, # formal offer ID
        }
        self.assertTrue(is_the_message_correct(formal_offer_example))

    def test_is_not_correct(self):
        a = {'type': 'a'}
        self.assertFalse(is_the_message_correct(a))
        b = {}
        self.assertFalse(is_the_message_correct(b))
