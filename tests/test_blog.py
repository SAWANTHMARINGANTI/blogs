import unittest
from app.models import Blog

class BlogTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the Blog class
    '''

    def setUp(self):
        '''
        Set up method that will run before every Test
        '''
        self.new_blog = Blog(id=6,title = 'life',blog='My post',user_id= 2)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog,Blog))
