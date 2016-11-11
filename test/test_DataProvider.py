__date__ = "4/9/16"
__author__ = "Sharon Lev"
__email__ = "sharon_lev@yahoo.com"

from unittest import TestCase
from src.unittestextras import DataProvider

class TestDataProvider(TestCase):
  """
  test data driven tests functionality
  """
  class decorated_class(object):

    _cause_error_at_setup = False
    _cause_error_in_test = False
    _raise_assertion_in_test = False
    _setup_count = 0
    _method_count = 0
    _tear_down_count = 0

    def setUp(self):
      print 'setup',
      self._setup_count += 1
      if self._cause_error_at_setup: raise IOError("generic setup error")

    def tearDown(self):
      print 'teardown'
      self._tear_down_count += 1

    data_dict = lambda:(
      dict(key1=1, key2=2),
      dict(key1=3, key2=4)
    )

    data_list = lambda:(
      [1,2,3],
      [4,5,6]
    )

    data_strings = lambda:(
      "string_1",
      "string_2"
    )

    @DataProvider(data_dict)
    def dict_driven_method(self, key1, key2):
      print key1, key2,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1

    @DataProvider(data_list)
    def list_driven_method(self, a, b, c):
      print a, b, c,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1

    @DataProvider(data_strings)
    def string_driven_method(self, a_string):
      print a_string,
      if self._cause_error_in_test: raise IOError("generic test error")
      assert not self._raise_assertion_in_test , "generic assertion error"
      self._method_count += 1


  def setUp(self):
    self.test_class = self.decorated_class()


  def test__dict_driven_testing(self):
    self.test_class.setUp()
    self.test_class.dict_driven_method()
    self.test_class.tearDown()
    for counter in [self.test_class._method_count, self.test_class._setup_count, self.test_class._tear_down_count]:
      self.assertEqual(counter, 2)


  def test__list_driven_testing(self):
    self.test_class.setUp()
    self.test_class.list_driven_method()
    self.test_class.tearDown()
    for counter in [self.test_class._method_count, self.test_class._setup_count, self.test_class._tear_down_count]:
      self.assertEqual(counter, 2)


  def test__string_driven_testing(self):
    self.test_class.setUp()
    self.test_class.string_driven_method()
    self.test_class.tearDown()
    for counter in [self.test_class._method_count, self.test_class._setup_count, self.test_class._tear_down_count]:
      self.assertEqual(counter, 2)


  def test__raise_error_in_setup(self):
    self.test_class.setUp()
    self.test_class._cause_error_at_setup = True
    assertion = None
    try:
      self.test_class.string_driven_method()
    except Exception, e:
      assertion = e

    self.assertIsInstance(e, Exception)


  def test__raise_error_in_test(self):
    self.test_class.setUp()
    self.test_class._cause_error_in_test = True
    assertion = False
    try:
      self.test_class.string_driven_method()
    except Exception, e:
      print type(e.message), e.message
      assertion = e

    self.assertIsInstance(assertion, Exception)
    self.assertEqual(len(assertion.errors), 2)

  def test__raise_assertion_in_test(self):
    self.test_class.setUp()
    self.test_class._raise_assertion_in_test = True
    assertion = False
    try:
      self.test_class.string_driven_method()
    except AssertionError, e:
      print type(e.message), e.message
      assertion = e

    self.assertIsInstance(assertion, AssertionError)
    self.assertEqual(len(assertion.failures), 2)