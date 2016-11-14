# pyUnittestExtras
extra functionalities for unittests 

###Classes and Objects

####DataSet
DataSet is a collection of data (strings, lists, dictionaries) that are provided
as sets to a test method for data driven testing

####DataSource
DataSource provides the same data sets to a test method like a DataSet, but it takes
the content from a local/remote file

####DataProvider

DataProvider is a unittest test method decorator for data driven tests

DataProvider provides data sets to the test parameters via a DataSet or DataSource

###Tutorial

####A simple data driven test that checks a provided string
in its simplistic form, a DataSet can provide individual arguments to test methods:
```python
from unittest imort TestCase
from unittestextras import DataProvider, DataSet
from ficticious_lib import KeyboardTyper, ScreenValidator

class my_test_class(TestCase):

    strings = DataSet(
        "abcdefg",
        "1234567",
        "abcd 1234 abc"
    )
    
  @DataProvider(strings)
  def test_my_string(self, text):
    kt = KeyboardTyper()
    sv = ScreenValidator()
    
    kt.type(text)
    sv.validate_on_screen(text)
    
```
 
####Providing lists to tests
```python
from unittest imort TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):

    strings = DataSet(
        ["abcdefg", 7],
        ["1234567", 7],
        ["abcd 1234 abc", 13]
    )
    
  @DataProvider(strings)
  def test_my_string(self, text, expected_length):
    self.assertEqual(len(text), expected_length)    
```

####Providing keyed properties to tests
```python
from unittest imort TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):

    strings = DataSet(
        {text: "abcdefg", expected_length: 7},
        {text: "1234567", expected_length: 7},
        {text: "abcd 1234 abc", expected_length: 13}
    )
    
  @DataProvider(strings)
  def test_my_string(self, text, expected_length):
    self.assertEqual(len(text), expected_length)    
```

###Identifying results
 Since each test method will be run multiple times (once for each data set provided),
 a mechanism to identify the failing data set is implemented as follow:
 
 ####Default: Indexing data sets by their location:
 By default, failing data sets will be identified by their index in the provided data list:
```python
from unittest imort TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):

    strings = DataSet(
        {text: "abcdefg", expected_length: 7},  # WILL BE IDENTIFIED AS [0]
        {text: "1234567", expected_length: 7},  # WILL BE IDENTIFIED AS [1]
        {text: "abcd 1234 abc", expected_length: 13} # WILL BE IDENTIFIED AS [2]
    )
    
  @DataProvider(strings)
  def test_my_string(self, text, expected_length):
    self.assertEqual(len(text), expected_length)    
```

If you'd like to use one of the passed arguments as the ID for the failing report you can do so by
passing either a id_key or id_index to the DataProvider:

```python
from unittest imort TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):

    strings = DataSet(
        {text: "abcdefg", expected_length: 7},  # WILL BE IDENTIFIED AS [abcdeg]
        {text: "1234567", expected_length: 7},  # WILL BE IDENTIFIED AS [1234567]
        {text: "abcd 1234 abc", expected_length: 13} # WILL BE IDENTIFIED AS [abcd 1234 abc]
    )
    
  @DataProvider(strings, id_key='text')
  def test_my_string(self, text, expected_length):
    self.assertEqual(len(text), expected_length)    
```

```python
from unittest imort TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):

    strings = DataSet(
        ["abcdefg", 7], # WILL BE IDENTIFIED AS [abcdeg]
        ["1234567", 7], # WILL BE IDENTIFIED AS [1234567]
        ["abcd 1234 abc", 13] # WILL BE IDENTIFIED AS [abcd 1234 abc]
    )
    
  @DataProvider(strings, id_index=0)
  def test_my_string(self, text, expected_length):
    self.assertEqual(len(text), expected_length)    
```
