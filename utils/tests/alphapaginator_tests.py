"""
"""
import string
from utils.testing import FakeModelTestCase
from utils.alphapaginator import AlphaPaginator
from utils.tests.models import TestModel

class AlpaPaginatorTest(FakeModelTestCase):
    """
    """
    
    def test_backwards_compatibility(self):
        """
        Assert that basic numeric pagination still works
        """
        for i in range(40):
            TestModel.objects.create(name="test %s" % i)
        paginator = AlphaPaginator(TestModel.objects.all(), 10)
        self.assertEqual(paginator.num_pages, 4)
        page = paginator.page(1)
        self.assertEqual(10, page.object_list.count())
        
    
    def test_alphabet(self):
        """
        Assert that the test paginator returns the correct alphabet
        """
        test_alphabet = list("QWERTYUIOP")
        test_alphabet.sort()
        for letter in test_alphabet:
            TestModel.objects.create(name=letter+"asdf", test="test")
            
        for alphabet, field in [(test_alphabet, "name"),
                                (["T"], "test"),
                                ([], None)]:
            paginator = AlphaPaginator(TestModel.objects.all(), 10, field=field)
            self.assertEqual(alphabet, paginator.alphabet())
    
    def test_alphabetic_pagination(self):
        """
        Assert that pagination by letter works
        """
        alphabet = list(string.uppercase)
        for letter in alphabet: #two for each letter
            TestModel.objects.create(name=letter+"asdf", test="test")
            TestModel.objects.create(name=letter+"qwerty", test="blah")
        
        paginator = AlphaPaginator(TestModel.objects.all(), 10, field="name")
        # 26 letters * 2 of each / 10 per page (+ 1 page with only 2 entries) = 6 pages
        self.assertEqual(6, paginator.num_pages)
        
        pageM = paginator.page("m")
        self.assertEqual(2, len([o for o in pageM.object_list if o.name.lower().startswith('m')]))
        self.assertEqual(0, len([o for o in pageM.object_list if o.name.lower().startswith('a')]))
        self.assertEqual(0, len([o for o in pageM.object_list if o.name.lower().startswith('z')]))
        curr_page = 3 # m is the 12th letter * 2 of each / 10 per page (+ 1 for page with m on it)
        self.assertEqual(curr_page+1, pageM.next_page_number())
        self.assertEqual(curr_page-1, pageM.previous_page_number())
        
        