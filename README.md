# pyUnittestExtras
extra functionalities for unittests 

##Classes and Objects

###DataSet
DataSet is a collection of data (strings, lists, dictionaries) that are provided
as sets to a test method for data driven testing

###DataSource
DataSource provides the same data sets to a test method like a DataSet, but it takes
the content from a local/remote file

###DataProvider

DataProvider is a unittest test method decorator for data driven tests

DataProvider provides data sets to the test parameters via a DataSet or DataSource

Will result in multiple test versions of the decorated test method

###DataProviderSingleton

Similar to DataProvider, but will not result in multiple test versions of the test method. Instead all data sets will report as a single test

##Tutorial I: Providing Primitives
In its simplistic form, a `DataSet` can provide individual (primitive or not) parameters to test methods:

```python
strings = DataSet(
    'string one',
    'string two',
    'yet another string'
)
```

These `strings` `Dataset` can then be provided to a test method using a `DataProvider`:

```python
from unittest import TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):
    strings = DataSet(
        'string one',
        'string two',
        'yet another string'
    )

    @DataProvider(strings)
    def test_string_has_3_words(self, text):
        self.assertEqual(
          len(text.split()), 3,
          'string "%s" does not have 3 words' % text
        )
```
This will result in multiple test runs (3 in this example)  

**Output (*removed Traceback info for simplicity*):**

```bash
pyUnittestExtras# python -m unittest discover -s test -p my_test_class.py
FF.
======================================================================
FAIL: test_string_has_3_words('string one') (test_temp.my_test_class)
----------------------------------------------------------------------
Traceback (most recent call last):
...
AssertionError: string "string one" does not have 3 words

======================================================================
FAIL: test_string_has_3_words('string two') (test_temp.my_test_class)
----------------------------------------------------------------------
Traceback (most recent call last):
...
AssertionError: string "string two" does not have 3 words

----------------------------------------------------------------------
Ran 3 tests in 0.000s

FAILED (failures=2)
```

***

##Tutorial II: Providing Lists
`DataSet` can also provide lists and tuples to test methods that are expecting more than one parameter:

```python
from unittest import TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):
    strings_and_expected_lengths = DataSet(
        ["abcdefg", 7],
        ["x"*7, 7],
        ["abc"*4, 12]
    )

    @DataProvider(strings_and_expected_lengths)
    def test_my_string(self, text, expected_length):
        self.assertEqual(len(text), expected_length)
```

***

##Tutorial III: Providing Dictionaries
Similar to providing lists, `DataSet` can also provide keyed dictionaries, 
this makes the data a bit more readable and easy to follow. 

***Caveat*: the keys in the data dictionaries must match the named parameters of the test method**.

```python
from unittest import TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):
    strings_and_expected_lengths = DataSet(
        dict(text="abcdefg", expected_length=7),
        dict(text="x"*7, expected_length=7),
        dict(text="abc"*4, expected_length=12)
    )

    @DataProvider(strings_and_expected_lengths)
    def test_my_string(self, text, expected_length):
        self.assertEqual(len(text), expected_length)
```

##Tutorial IV: DataProviderSingleton

While `DataProvider` creates an individual result per data set provided, `DataProviderSingleton` combines
all data sets provided into a single test result (though test setup and teardown will occur between variations). 

```python

from unittest import TestCase
from unittestextras import DataProviderSingleton as DataProvider, DataSet

class my_test_class(TestCase):
    strings_and_expected_lengths = DataSet(
        dict(text="abcdefg", expected_length=4), #will fail
        dict(text="x"*7, expected_length=7),
        dict(text="abc"*4, expected_length=11) #will fail
    )

    @DataProvider(strings_and_expected_lengths)
    def test_my_string(self, text, expected_length):
        self.assertEqual(len(text), expected_length)
```

will result in the following output:

```bash
pyUnittestExtras# python -m unittest discover -s . -p test_sample.py -v
test_my_string (test_sample.my_test_class) ... FAIL

======================================================================
FAIL: test_my_string (test_sample.my_test_class)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...
    raise assertion
AssertionError: The following Assertions occurred: ['Data set [0]: 7 != 4', 'Data set [2]: 12 != 11']

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
```

Notice that only 1 test is tracked by unittest module here!
 
Much like `DataProvider`, `id_index` and `id_key` can be used here as well to make the failing 
results easier to track to the individual data set.

***

##Appendix: Identifying Results
By default tests will be named in reference to their entire passed data set, but it's also possible to customize the signature of the individual test results.

### Naming results by indexed data parameter:
`DataProvider	` allows using one of the passed parameters in each set as a 'label' for the test id in the results by setting a `id_index`:

```python
from unittest import TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):
    strings_and_expected_lengths = DataSet(
        ["Simple String", "abcdefg", 7],
        ["Multiplied Character", "x"*7, 7],
        ["Multipled String", "abc"*4, 11]
    )

    @DataProvider(strings_and_expected_lengths, id_index=0)
    def test_my_string(self, data_label, text, expected_length):
        self.assertEqual(len(text), expected_length)
```

results in:

```bash
FAIL: test_my_string(Multipled String) (test_temp.my_test_class)
```

Which is a bit more readable than (without `id_index`:

```bash
FAIL: test_my_string('Multipled String','abcabcabcabc',11) (test_temp.my_test_class)
```

***

### Naming results by keyed data parameter:
`DataProvider	` also allows customizing the test signature in the results using a keyed parameter when passing keyed dictionaries in the `DataSet` by setting the `id_key`:

```python
from unittest import TestCase
from unittestextras import DataProvider, DataSet

class my_test_class(TestCase):
    strings_and_expected_lengths = DataSet(
        dict(data_label="Simple String", text="abcdefg", expected_length=7),
        dict(data_label="Multiplied Character", text="x"*7, expected_length=6),
        dict(data_label="Multiplied String", text="abc"*4, expected_length=12)
    )

    @DataProvider(strings_and_expected_lengths, id_key='data_label')
    def test_my_string(self, data_label, text, expected_length):
        self.assertEqual(len(text), expected_length)
```

Results in:

```bash
FAIL: test_my_string(Multiplied Character) (test_temp.my_test_class)
```

Which is a bit more readable than (without `id_key`):

```bash
FAIL: test_my_string(expected_length=6,text=xxxxxxx,data_label=Multiplied Character) (test_temp.my_test_class)
```