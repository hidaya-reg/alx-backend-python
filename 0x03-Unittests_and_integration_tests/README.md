# 0x03. Unittests and Integration Tests
Unit testing is the process of testing that a particular function returns expected results for different set of inputs. A unit test is supposed to test standard inputs and corner cases. A unit test should only test the logic defined inside the tested function. Most calls to additional functions should be mocked, especially if they make network or database calls.

The goal of a unit test is to answer the question: if everything defined outside this function works as expected, does this function work as expected?

Integration tests aim to test a code path end-to-end. In general, only low level functions that make external calls such as HTTP requests, file I/O, database I/O, etc. are mocked.

Integration tests will test interactions between every part of your code.

Execute your tests with: `$ python -m unittest path/to/test_file.py`
## Resources
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)
- [How to mock a readonly property with mock?](https://stackoverflow.com/questions/11836436/how-to-mock-a-readonly-property-with-mock)
- [parameterized](https://pypi.org/project/parameterized/)
- [Memoization](https://en.wikipedia.org/wiki/Memoization)

## Learning Objectives
<details>
<summary>unittest framework</summary>

### ``unittest`` framework
#### Test Discovery
Test discovery in Python's ``unittest`` module is a feature that automatically finds and runs test cases across multiple files in a project. This can be especially useful in larger projects where tests are spread across various modules and files. ``unittest`` will look for test files and test cases according to specific naming conventions.
##### How Test Discovery Works
1. Naming Convention:
    + Test files should be named with a ``test_`` prefix (e.g., ``test_example.py``) or ``_test`` suffix.
    + Test case methods should start with test_ (e.g., def test_addition(self):).
2. Directory Structure: Typically, ``tests`` are organized into a tests directory, but test discovery can work on any directory where test files are located.
3. Running Test Discovery:
    + To run test discovery from the command line, navigate to the root directory of your project and use: `python -m unittest discover`
    + By default, ``unittest`` will search for files that match the ``test*.py`` pattern in the current directory and any subdirectories.
    + You can specify a directory, pattern, or start directory as well, like this:
    ```bash
    python -m unittest discover -s tests -p "test_*.py"
    ```
        - ``-s`` or ``--start-directory`` specifies the starting directory for test discovery.
        - ``-p`` or ``--pattern`` specifies the file pattern to look for test files.
**Example Project Structure**
```markdown
my_project/
├── app/
│   ├── module1.py
│   └── module2.py
└── tests/
    ├── test_module1.py
    └── test_module2.py
```
Each ``test_*.py`` file in the ``tests/`` directory could contain test cases for the corresponding module in ``app/``. You can run all the tests in ``tests/`` with:
```bash
python -m unittest discover -s tests
```
#### Organizing test code
##### 1. Create a Dedicated ``tests/`` Directory
Place all test files in a ``tests/`` directory at the root of your project. This keeps test files separate from the application code, making them easier to find and manage.
```plaintext
my_project/
├── app/
│   ├── module1.py
│   ├── module2.py
├── tests/
│   ├── test_module1.py
│   ├── test_module2.py
└── README.md
```
##### 2. Follow Naming Conventions
- File Names: Name test files with a ``test_`` prefix (e.g., ``test_module1.py``), which helps with test discovery.
- Test Classes and Methods: Use descriptive names for test classes and methods. Test class names should start with ``Test``, and individual test method names should start with ``test_``.
##### 3. Group Tests by Module or Feature
Create a separate test file for each module or feature, and include all related tests in that file. This makes it easy to locate tests for a specific part of your application.
For example, tests for module1.py would go in test_module1.py

##### 4. Use ``setUp`` and ``tearDown`` for Reusable Code
- ``setUp`` runs before each test, allowing you to prepare the test environment (e.g., creating a database connection).
- ``tearDown`` runs after each test, letting you clean up (e.g., closing the database connection).
```python
class TestModule1(unittest.TestCase):
    def setUp(self):
        self.test_data = [1, 2, 3]

    def tearDown(self):
        self.test_data = None

    def test_data_length(self):
        self.assertEqual(len(self.test_data), 3)
```
##### 5. Use ``setUpClass`` and ``tearDownClass`` for Class-Level Setup
Use ``@classmethod`` with ``setUpClass`` and ``tearDownClass`` if there’s setup that only needs to run once for the entire class (e.g., setting up a temporary database).
```python
class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = setup_database()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
```
##### 6. Organize Tests into Subdirectories if Needed
For large projects, you can use subdirectories in ``tests/`` to organize tests by module, feature, or category (e.g., ``unit/``, ``integration/``, ``functional/``).
```plaintext
tests/
├── unit/
│   ├── test_module1.py
├── integration/
│   ├── test_database.py
└── functional/
    └── test_user_flow.py
```
##### 7. Use Test Fixtures to Share Setup Across Tests
- A fixture is a reusable piece of setup that can be used across different tests, often created with ``setUp`` or ``setUpClass``.
- You could also use the ``unittest.mock`` module to mock objects or dependencies to isolate the functionality you’re testing.

##### 8. Run Tests with Test Discovery
Use the unittest discovery command to run all tests at once:
```bash
python -m unittest discover -s tests
```

</details>
<details>
<summary>Test Suite</summary>

### Test Suite
A test suite is a collection of test cases, test classes, or even other test suites, grouped together to be run together in a single batch. Test suites are useful in scenarios where you want to organize tests into categories or run specific groups of tests independently. This can be particularly helpful in larger projects where you may want to run only a subset of tests (e.g., critical tests only) or structure tests in logical groups for different components.

#### Creating and Running a Test Suite
1. Basic Structure: A test suite can be created using ``unittest.TestSuite()``, where you add specific test cases using the ``addTest()`` or ``addTests()`` method.
2. Using ``unittest.TextTestRunner``: You can then pass the suite to ``unittest.TextTestRunner`` to execute the tests in the suite.

Example
```python
import unittest

# First test case
class TestMathOperations(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_subtraction(self):
        self.assertEqual(5 - 2, 3)

# Second test case
class TestStringOperations(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('hello'.upper(), 'HELLO')

    def test_isupper(self):
        self.assertTrue('HELLO'.isupper())
        self.assertFalse('hello'.isupper())
```
**Creating a Test Suite**
You can create a test suite that includes specific test cases or test classes:
```python
def suite():
    suite = unittest.TestSuite()

    # Adding individual test methods to the suite
    suite.addTest(TestMathOperations('test_addition'))
    suite.addTest(TestStringOperations('test_upper'))

    # Adding an entire test class to the suite
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathOperations))

    return suite
```
**Running the Test Suite**
```python
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
```
**Explanation of the Example:**
- Adding Specific Test Methods: ``suite.addTest(TestMathOperations('test_addition'))`` adds only the ``test_addition`` method to the suite. This is helpful if you only want to run specific tests from a class.
- Adding All Tests from a Test Case: ``suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestMathOperations))`` loads all test methods from the ``TestMathOperations`` class into the suite.

#### Using ``unittest.TestLoader`` to Create Suites Automatically
``unittest.TestLoader`` provides methods like ``loadTestsFromTestCase`` and ``discover`` to automatically load tests, making it easier to build suites without manually adding each test.

- Example: Creating a Suite with All Tests in a Module
If all tests are in a single module, you can load all tests at once:
```python
def suite():
    return unittest.TestLoader().loadTestsFromModule(my_test_module)
```
- Example: Discovering Tests in a Directory
For larger projects with many test files, you can use unittest.TestLoader().discover to find all tests in a directory:
```python
if __name__ == '__main__':
    suite = unittest.TestLoader().discover(start_dir='test_directory', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)
```
#### Benefits of Test Suites
- **Selective Execution:** Run only specific tests or categories (e.g., smoke tests, regression tests).
- **Logical Organization:** Organize tests by functionality or component.
- **Parallel Execution:** Some frameworks and CI/CD tools support running test suites in parallel, improving test performance.
</details>
<details>
<summary>Parameterized Tests</summary>

### Parameterized Tests 
Parameterized tests are tests that allow you to run the same test logic with different inputs and expected outputs. This is helpful when you want to test a function or method with various inputs without having to duplicate the test code for each case. Python’s unittest doesn’t directly support parameterized tests out-of-the-box, but there are a few ways to achieve it.
#### Ways to Implement Parameterized Tests in ``unittest``
1. **Using ``subTest``:**
    + ``subTest`` is part of ``unittest`` and is helpful when you want to pass different parameters to a test case.
    + It keeps each sub-test isolated, so if one fails, the others still run.

Example: Parameterized Tests with ``subTest``
```python
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add(self):
        test_cases = [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300)
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertEqual(add(a, b), expected)

if __name__ == '__main__':
    unittest.main()
```
In this example, subTest runs add(a, b) for each case, verifying that it matches the expected value. If a sub-test fails, it shows which input caused the failure, making it easier to debug.
**Benefits of Using subTest**
- Isolation of Tests:
    + Each call to ``self.subTest()`` creates a new context for that specific test case. If one of the assertions fails, it will not prevent the subsequent assertions from running. This means you can see the results of all test cases in a single run.
    + If you don't use ``subTest``, when an assertion fails, the entire test method stops executing. You won't know if other cases pass or fail unless you run the tests multiple times.
- Clearer Reporting:
    + When a sub-test fails, ``unittest`` will report it with a clear indication of which specific input caused the failure. This includes the values of ``a``, ``b``, and ``expected``.
    + If you simply assert without ``subTest``, the error message might not provide as much context regarding which set of inputs caused the failure.
- Debugging Ease:
    + If you have multiple test cases, and one fails, you can easily debug the failing case while still knowing the status of the others. This makes it easier to pinpoint issues in your code.
**Example Comparison**
**Without ``subTest``**
```python
class TestAddFunction(unittest.TestCase):
    def test_add(self):
        test_cases = [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300)
        ]

        for a, b, expected in test_cases:
            self.assertEqual(add(a, b), expected)  # If one fails, all subsequent tests are skipped
```
If one of the assertions fails (e.g., ``add(-1, 1)`` returns 1 instead of 0), the test will stop executing, and you'll only see the failure for that test case.

**With subTest**
```python
class TestAddFunction(unittest.TestCase):
    def test_add(self):
        test_cases = [
            (1, 2, 3),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300)
        ]

        for a, b, expected in test_cases:
            with self.subTest(a=a, b=b, expected=expected):
                self.assertEqual(add(a, b), expected)  # Each sub-test is independent
```
In this case, if ``add(-1, 1)`` fails, you will still get results for the other test cases, allowing you to identify that the tests for ``(1, 2)``, ``(0, 0)``, and ``(100, 200)`` passed, while only ``(-1, 1)`` failed.
#### Using ``parameterized`` Package:
- The ``parameterized`` library provides decorators to simplify parameterized tests in ``unittest``.
- This requires installing an additional package (``parameterized``), but it offers a more concise syntax.
```bash
pip install parameterized
```
**Example: Using the ``parameterized`` Library**
```python
import unittest
from parameterized import parameterized

def multiply(a, b):
    return a * b

class TestMultiplyFunction(unittest.TestCase):
    @parameterized.expand([
        (2, 3, 6),
        (0, 10, 0),
        (-1, 1, -1),
        (7, 6, 42)
    ])
    def test_multiply(self, a, b, expected):
        self.assertEqual(multiply(a, b), expected)

if __name__ == '__main__':
    unittest.main()
```
Here, the ``parameterized.expand`` decorator applies different sets of inputs (``a``, ``b``) and the ``expected`` value to the ``test_multiply`` method. Each tuple represents a set of arguments to pass to the function and compare to the expected output.
#### Using ``unittest.TestCase`` with Dynamic Test Methods:
- You can dynamically create test methods within the ``TestCase`` class to handle parameterized testing.
- This is more advanced and used when the test cases are complex or need to be dynamically generated.
#### Benefits of Parameterized Tests
- Reduced Code Duplication: You don’t need to write separate test methods for each input.
- Readable and Organized: Keeps related test cases together, making it easier to see how the function performs with different inputs.
- Easier Maintenance: New test cases can be added without duplicating the entire test function.
**Choosing an Approach**
- ``subTest``: Good for simple cases and when you don’t want to add external dependencies.
- ``parameterized`` Library: Useful when you have many test cases, and you want concise code.
- Dynamic Test Methods: For more advanced cases where tests are generated programmatically based on certain conditions or inputs.
</details>
<details>
<summary>Mocking</summary>

### Mocking
Mocking is a technique used in unit testing to simulate the behavior of complex, real objects in a controlled way. This is particularly useful when the real object is impractical to use in tests, such as when it involves external systems (like databases, APIs, or other services), has side effects, or is slow to instantiate.
#### Why Use Mocking?
- **Isolation:** It allows you to isolate the unit of work you are testing, ensuring that tests are only affected by the code you're testing.
- **Speed:** Tests that rely on external resources can be slow. Mocking can make tests run faster by avoiding the need for these resources.
- **Predictability:** Mocking gives you control over the behavior of dependencies, ensuring they return expected results without side effects.
#### Using ``unittest.mock``
The ``unittest.mock`` module, part of the Python standard library, provides tools for mocking and patching in unit tests.

**Basic Mock Example**
```python
from unittest import TestCase
from unittest.mock import Mock

class MyClass:
    def method(self):
        return "real method"

class TestMyClass(TestCase):
    def test_method(self):
        my_mock = Mock()
        my_mock.method.return_value = "mocked method"
        
        # Use the mock
        result = my_mock.method()
        self.assertEqual(result, "mocked method")
```

#### Common Methods and Assertions Provided by Mock

| **Method/Assertion**           | **Description**                                                                           | **Example**                                                                                                     |
|--------------------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| `Mock()`                       | Creates a new mock object.                                                               | `mock = Mock()`                                                                                               |
| `return_value`                | Sets the value returned when the mock is called.                                        | `mock.return_value = 'Hello'`                                                                                 |
| `side_effect`                 | Sets a function to be called when the mock is invoked, or an iterable for multiple returns.| `mock.side_effect = [1, 2, 3]`                                                                                |
| `assert_called_once()`        | Asserts that the mock was called exactly once.                                          | `mock.assert_called_once()`                                                                                    |
| `assert_called_with(*args, **kwargs)` | Asserts that the mock was called with the specified arguments.                      | `mock.assert_called_with(1, 2)`                                                                                |
| `assert_any_call(*args, **kwargs)` | Asserts that the mock was called with the specified arguments at least once.        | `mock.assert_any_call(1, 2)`                                                                                  |
| `assert_not_called()`         | Asserts that the mock was never called.                                                  | `mock.assert_not_called()`                                                                                     |
| `reset_mock()`                | Resets all call information on the mock.                                                | `mock.reset_mock()`                                                                                            |
| `call_count`                  | Returns the number of times the mock was called.                                        | `print(mock.call_count)`                                                                                       |
| `call_args`                   | Returns the last call made to the mock.                                                  | `print(mock.call_args)`                                                                                        |
| `call_args_list`              | Returns a list of all calls made to the mock.                                           | `print(mock.call_args_list)`                                                                                  |

#### Example
```python
from unittest.mock import Mock

# Create a mock object
mock = Mock()

# Setting return value
mock.return_value = 'Hello'
print(mock())  # Output: Hello

# Setting side effects
mock.side_effect = [1, 2, 3]
print(mock())  # Output: 1
print(mock())  # Output: 2

# Assert that the mock was called with specific arguments
mock(1, 2)
mock.assert_called_with(1, 2)

# Assert that the mock was called exactly once
mock.assert_called_once()

# Assert that the mock was never called
mock.assert_not_called()

# Resetting the mock
mock.reset_mock()
mock.assert_not_called()  # No error, as it has been reset
```
</details>
<details>
<summary>Patching</summary>

### Patching
Patching is a technique provided by the ``unittest.mock`` library that allows you to temporarily replace or modify objects in your code for the duration of a test. This is particularly useful for isolating the unit of code you're testing from its dependencies, such as external APIs, databases, or other components that might introduce variability or side effects.

#### How Does Patching Work?
1. Targeting an Object: When you use ``@patch``, you specify a **target**—a string representing the object you want to replace. The target string usually follows the format ``'module.ClassName.method'`` or ``'module.function_name'``.
2. Creating a Mock Object: The patching process automatically creates a mock object to replace the target. This mock can be configured to return specific values, track how many times it was called, or assert calls to it.
3. Injection into the Test Function: The mock object is then passed as an argument to the test function. The order of the arguments corresponds to the order of the ``@patch`` decorators.
4. Scope of Patching: The patching is temporary. Once the test function completes, the original target is restored. This ensures that your tests do not interfere with each other.

#### How Does Patching End Up in the Function Definition?
When you use @patch on a test function, it wraps that function and modifies it to include the mock object as an argument. Here's how it looks in practice:
```python
from unittest.mock import patch

@patch('my_module.external_api_call')
def test_my_function(mock_api):
    # Inside this function, mock_api is a mock object
    mock_api.return_value = {'data': 'mocked data'}
    # Test logic using mock_api
```
#### Use Cases
##### Example 1: Mimicking API Output
```python
# my_module.py

import requests

def fetch_data(api_url):
    response = requests.get(api_url)
    return response.json()
```
**Test with Patching**
```python
# test_my_module.py

import unittest
from unittest.mock import patch
from my_module import fetch_data

class TestFetchData(unittest.TestCase):

    @patch('my_module.requests.get')
    def test_fetch_data(self, mock_get):
        # Define the mock response data
        # `mock_get` is a mock object that represents the requests.get method in my_module
        mock_response = {'key': 'value'}
        mock_get.return_value.json.return_value = mock_response

        # Call the function with a test URL
        result = fetch_data('http://example.com/api/data')

        # Assertions
        mock_get.assert_called_once_with('http://example.com/api/data')
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()
```
**Explanation**
Mimicking API Output: we use ``@patch`` to mock the ``requests.get`` method. We configure it to return a mock response when ``json()`` is called, allowing us to test the ``fetch_data`` function without hitting the actual API.

**How @patch Works:**
- ``@patch('my_module.requests.get')`` replaces ``requests.get`` in ``my_module``'s namespace with a mock object during the ``test_fetch_data`` function.
- This mock object (``mock_get``) lets you control the return value and behavior of ``requests.get`` in your tests.
##### Example 2: Simulating a Database Connection
In this example, let’s say you have a function that retrieves a user from a database. We will mock the database connection to return a predefined user object.
```python
# user_module.py

import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
```
**Test with Patching**
```python
# test_user_module.py

import unittest
from unittest.mock import patch, MagicMock
from user_module import get_user

class TestGetUser(unittest.TestCase):

    @patch('user_module.sqlite3.connect')
    def test_get_user(self, mock_connect):
        # Create a mock connection and cursor
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Define what the cursor should return when executing the query
        mock_cursor.fetchone.return_value = (1, 'John Doe')

        # Call the function
        user = get_user(1)

        # Assertions
        mock_connect.assert_called_once_with('users.db')
        mock_cursor.execute.assert_called_once_with('SELECT * FROM users WHERE id = ?', (1,))
        self.assertEqual(user, (1, 'John Doe'))

if __name__ == '__main__':
    unittest.main()
```
**Explanation**
Simulating Database Connection: we patch the ``sqlite3.connect`` method to prevent a real database connection. We create a ``MagicMock`` for the cursor and define its behavior, so when we call ``get_user``, it returns a predefined user tuple.

##### Example 3: Using ``unittest.mock.patch`` to Simulate ``sys.stdout``
```python
import unittest
from unittest.mock import patch
import io

def my_function():
    print("Hello, world!")

class TestMyFunction(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_my_function_output(self, mock_stdout):
        # Call the function that prints to standard output
        my_function()
        
        # Get the value written to the mocked stdout
        output = mock_stdout.getvalue().strip()
        
        # Assert the output matches the expected value
        self.assertEqual(output, "Hello, world!")

if __name__ == '__main__':
    unittest.main()
```
**Explanation:**
- ``@patch('sys.stdout', new_callable=io.StringIO)``: This decorates the test method and temporarily replaces sys.stdout with a StringIO object, which acts as a buffer to capture printed output.
- ``mock_stdout.getvalue()``: Retrieves the content that was printed during the test.
- Assertions: You can use ``assertEqual`` or other assertions to check that the output matches your expectations.

</details>
<details>
<summary>How to mock a readonly property with mock</summary>

### Mocking the Read-Only Property:
#### Using ``PropertyMock`` with ``patch``:
The ``PropertyMock`` class is used in combination with ``patch`` to mock properties. The ``patch()`` function can be applied to the property where it is defined.

**Example Scenario:**
```python
# my_module.py
class MyClass:
    @property
    def read_only_property(self):
        return "original value"
```
Here's how to mock this read-only property in a unit test:
```python
# test_my_module.py
import unittest
from unittest.mock import patch, PropertyMock
from my_module import MyClass

class TestMyClass(unittest.TestCase):
    @patch('my_module.MyClass.read_only_property', new_callable=PropertyMock)
    def test_read_only_property(self, mock_read_only):
        # Set the return value for the property mock
        mock_read_only.return_value = "mocked value"

        # Create an instance of MyClass
        obj = MyClass()

        # Assert that the property now returns the mocked value
        self.assertEqual(obj.read_only_property, "mocked value")
        mock_read_only.assert_called_once()

if __name__ == '__main__':
    unittest.main()
```
**Explanation:**
- ``@patch('my_module.MyClass.read_only_property', new_callable=PropertyMock)``: The ``patch()`` decorator targets the ``read_only_property`` attribute of ``MyClass`` in ``my_module`` and replaces it with a ``PropertyMock``.
- ``new_callable=PropertyMock``: Specifies that ``PropertyMock`` should be used for the replacement.
- ``mock_read_only.return_value``: Sets the return value of the mocked property to ``"mocked value"``.
- When ``obj.read_only_property`` is accessed, it returns ``"mocked value"`` instead of the original ``"original value"``.

</details>
<details>
<summary>Re-using old test code</summary>

### Re-using old test code
Re-using old test code is a great way to avoid duplication, save time, and maintain consistency across tests.
#### 1. Using Base Test Classes
You can create a **base test class** that contains setup code, common utility methods, or even test cases that should be shared by multiple subclasses. Other test classes can then inherit from this base class, reusing its methods and attributes.
```python
import unittest

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        # Common setup for all derived test cases
        self.shared_data = [1, 2, 3]

    def assertIsPositive(self, value):
        # Custom assertion that can be used by all derived test cases
        self.assertGreater(value, 0)

class TestFeatureA(BaseTestCase):
    def test_feature_a_behavior(self):
        self.assertIsPositive(len(self.shared_data))

class TestFeatureB(BaseTestCase):
    def test_feature_b_behavior(self):
        self.assertEqual(sum(self.shared_data), 6)
```
In this example:
- ``BaseTestCase`` provides a ``setUp`` method and a custom assertion, ``assertIsPositive``.
- ``TestFeatureA`` and ``TestFeatureB`` inherit from ``BaseTestCase`` and can directly use the setup and custom assertion.
#### 2. Using Helper Functions or Utility Modules
Place reusable helper functions in a separate **utility module** and import them in your test files as needed. This is useful when multiple tests require the same helper logic but don’t need to inherit from a common class.
```python
# test_utils.py - A separate utility module for helper functions
def create_mock_user(id, name):
    return {"id": id, "name": name}

# test_feature_c.py
import unittest
from test_utils import create_mock_user

class TestFeatureC(unittest.TestCase):
    def test_user_creation(self):
        user = create_mock_user(1, "Alice")
        self.assertEqual(user["name"], "Alice")
```
#### 3. Using ``setUpClass`` and ``tearDownClass`` for Shared Setup Across Tests
``setUpClass`` and ``tearDownClass`` are class methods that run once per class, instead of once per test method. You can use these to set up expensive resources (like database connections) once, allowing all tests in the class to reuse them.
```python
import unittest

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup shared resource, e.g., open database connection
        cls.db_connection = open_database()

    @classmethod
    def tearDownClass(cls):
        # Clean up shared resource
        cls.db_connection.close()

    def test_database_query(self):
        result = self.db_connection.query("SELECT * FROM users")
        self.assertIsNotNone(result)

    def test_another_database_query(self):
        result = self.db_connection.query("SELECT * FROM orders")
        self.assertIsNotNone(result)
```
#### 4. Using Test Suites to Combine Tests
A test suite allows you to combine multiple test cases or test classes to run together. This is helpful for reusing tests in different contexts or organizing tests into specific groups.
```python
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestFeatureA('test_feature_a_behavior'))
    suite.addTest(TestFeatureB('test_feature_b_behavior'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
```
#### 5. Parameterized Tests with ``unittest``
When you need to test a function with multiple inputs, parameterized tests allow you to reuse the same test code with different parameters. You can use the ``subTest`` feature in ``unittest`` to achieve this.
```python
import unittest

class TestParameterized(unittest.TestCase):
    def test_addition(self):
        cases = [
            (1, 2, 3),
            (5, 7, 12),
            (0, 0, 0),
        ]
        for a, b, expected in cases:
            with self.subTest(a=a, b=b):
                self.assertEqual(a + b, expected)
```
#### 6. Using Mock Objects to Share Test Setup
Mocking can be helpful when multiple tests need a simulated environment. Using ``unittest.mock.patch``, you can reuse the same mock setup across different tests or even globally within a test class.
```python
from unittest import TestCase
from unittest.mock import patch

class TestAPI(TestCase):
    @patch('app.external_api.get_data', return_value={"status": "ok"})
    def test_api_response(self, mock_get_data):
        response = app.some_function()
        self.assertEqual(response, {"status": "ok"})

    @patch('app.external_api.get_data', return_value={"status": "ok"})
    def test_another_response(self, mock_get_data):
        response = app.some_function()
        self.assertIn("status", response)
```
#### 7. Reusing Fixtures with ``setUpModule`` and ``tearDownModule``
For module-level fixtures, you can define ``setUpModule`` and ``tearDownModule`` functions, which run once for the entire module. This is useful for expensive setup tasks that only need to happen once, like starting a server.
```python
def setUpModule():
    global server
    server = start_test_server()

def tearDownModule():
    server.stop()

class TestServiceA(unittest.TestCase):
    def test_something(self):
        self.assertTrue(server.is_running())
```
</details>
<details>
<summary>Integration Tests</summary>

### Integration Tests
Integration tests are a type of software testing where different units, modules, or components of an application are tested together to ensure they work as expected when combined. Unlike unit tests, which focus on individual functions or classes in isolation, integration tests check how the units interact with each other and test the overall behavior of a feature or subsystem.
#### Key Characteristics of Integration Tests:
- Scope: Integration tests cover multiple components and check their interactions.
- Purpose: They ensure that different parts of the application work together as intended.
- Complexity: More comprehensive than unit tests, but they don't cover the entire application end-to-end.
- Dependencies: They may involve actual database connections, API calls, or other integrated systems.
#### Example Use Cases for Integration Tests:
- Verifying that a web server correctly interacts with a database.
- Testing the interaction between a web application and an external API.
- Checking how different services in a microservices architecture communicate.
#### How to Implement Integration Tests:
##### 1. Set Up Your Test Environment:
- Make sure your environment mimics a real-world scenario as closely as possible. This might include setting up a test database or using mock services that replicate real dependencies.
- Use environment variables or configuration files to separate the test environment from production.

##### 2. Choose a Testing Framework:
- Python: Use ``unittest``, ``pytest``, or ``nose2``.
- JavaScript: Use ``Jest`` or ``Mocha``.
- Java: Use ``JUnit`` or ``TestNG``.
- Other languages have their own standard testing tools and frameworks.

##### 3. Write Test Cases:
- Each integration test should include steps to set up the test, perform actions, and verify that the results are as expected.
- Ensure tests clean up any resources they use, like temporary files or database entries.

#### Example in Python with ``unittest``:
Suppose you have a simple web application that fetches user data from a database.

Sample ``app.py`` Code:
```python
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return jsonify({'id': user[0], 'name': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404
```
**Integration Test Code (test_integration.py):**
```python
import unittest
import app

class TestUserAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask app and set up test data
        app.app.testing = True
        cls.client = app.app.test_client()
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO users (id, name) VALUES (1, 'John Doe')")
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("DROP TABLE users")
        conn.commit()
        conn.close()

    def test_get_user_success(self):
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', response.get_data(as_text=True))

    def test_get_user_not_found(self):
        response = self.client.get('/users/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
```
**Key Points in the Example:**
- ``setUpClass``: Prepares the test environment by creating the database and inserting sample data.
- ``tearDownClass``: Cleans up after all tests are done to prevent side effects.
- Client Testing: Uses ``Flask``'s ``test_client()`` to make HTTP requests to the app.
- Assertions: Check that the status code and response data match expected values.

**Best Practices for Integration Tests:**
- Isolate the Environment: Ensure tests do not affect the real data or state. Use separate test databases and mock services when possible.
- Automate Cleanup: Ensure any changes made during tests are reverted.
- Use Mocks for External Services: When testing interactions with APIs or external services, use unittest.mock or similar libraries to mock responses.
- Run Tests Frequently: Integrate tests into your CI/CD pipeline for regular verification.
</details>
<details>
<summary>Memoization </summary>

### Memoization 
Memoization is an optimization technique used primarily in computing to speed up function calls by caching previously computed results. When a function is called with a particular set of inputs, its output is stored in memory (often in a dictionary or similar data structure). If the function is called again with the same inputs, the stored result is returned immediately instead of recomputing it.
#### Key Features of Memoization:
1. **Caching Results:** The main purpose is to save time on expensive function calls by avoiding redundant calculations.
2. **Use Cases:** It’s particularly effective for functions that are called multiple times with the same arguments, such as recursive functions or those with expensive calculations (e.g., Fibonacci numbers, combinatorial problems).
3. **Implementation:** Memoization can be implemented manually or through built-in decorators (like ``functools.lru_cache`` in Python).

#### Example of Memoization in Python
```python
def memoize(f):
    cache = {}
    
    def memoized_f(n):
        if n not in cache:
            cache[n] = f(n)
        return cache[n]
    
    return memoized_f

@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Testing the memoized Fibonacci function
print(fibonacci(10))  # Output: 55
```
#### Benefits of Memoization:
- **Performance Improvement:** It significantly speeds up functions with overlapping subproblems, reducing the time complexity from exponential to linear for some algorithms.
- **Simplicity:** Easy to implement, especially in languages or frameworks that support higher-order functions or decorators.
#### Limitations:
- **Memory Usage:** It requires additional memory to store results, which may be problematic for large input sizes or when dealing with a high number of unique calls.
- **Statefulness:** It can introduce complexity if the function relies on external states or mutable objects, as these may change over time.
</details>

## Required Files
- **``utils.py``**
- **``client.py``**
- **``fixtures.py``**

## Tasks
### 0. Parameterize a unit test
Familiarize yourself with the ``utils.access_nested_map`` function and understand its purpose. Play with it in the Python console to make sure you understand.
In this task you will write the first unit test for ``utils.access_nested_map``.

Create a ``TestAccessNestedMap`` class that inherits from ``unittest.TestCase``.

Implement the ``TestAccessNestedMap.test_access_nested_map`` method to test that the method returns what it is supposed to.

Decorate the method with ``@parameterized.expand`` to test the function for following inputs:
```python
nested_map={"a": 1}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a",)
nested_map={"a": {"b": 2}}, path=("a", "b")
```
For each of these inputs, test with ``assertEqual`` that the function returns the expected result.

The body of the test method should not be longer than 2 lines.

### 1. Parameterize a unit test
Implement ``TestAccessNestedMap.test_access_nested_map_exception``. Use the ``assertRaises`` context manager to test that a ``KeyError`` is raised for the following inputs (use ``@parameterized.expand``):
```python
nested_map={}, path=("a",)
nested_map={"a": 1}, path=("a", "b")
```
Also make sure that the exception message is as expected.

### 2. Mock HTTP calls
Familiarize yourself with the ``utils.get_json`` function.
Define the ``TestGetJson(unittest.TestCase)`` class and implement the ``TestGetJson.test_get_json`` method to test that ``utils.get_json`` returns the expected result.

We don’t want to make any actual external HTTP calls. Use ``unittest.mock.patch`` to patch ``requests.get``. Make sure it returns a ``Mock`` object with a ``json`` method that returns ``test_payload`` which you parametrize alongside the ``test_url`` that you will pass to ``get_json`` with the following inputs:
```python
test_url="http://example.com", test_payload={"payload": True}
test_url="http://holberton.io", test_payload={"payload": False}
```
Test that the mocked ``get`` method was called exactly once (per input) with ``test_url`` as argument.

Test that the output of ``get_json`` is equal to ``test_payload``.

### 3. Parameterize and patch
Read about memoization and familiarize yourself with the ``utils.memoize`` decorator.
Implement the TestMemoize(unittest.TestCase) class with a ``test_memoize`` method.
Inside ``test_memoize``, define following class
```python
class TestClass:

    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()
```
Use ``unittest.mock.patch`` to mock ``a_method``. Test that when calling ``a_property`` twice, the correct result is returned but ``a_method`` is only called once using ``assert_called_once``.

### 4. Parameterize and patch as decorators
Familiarize yourself with the ``client.GithubOrgClient`` class.
In a new ``test_client.py`` file, declare the ``TestGithubOrgClient(unittest.TestCase)`` class and implement the ``test_org`` method.
This method should test that ``GithubOrgClient.org`` returns the correct value.
Use ``@patch`` as a decorator to make sure ``get_json`` is called once with the expected argument but make sure it is not executed.
Use ``@parameterized.expand`` as a decorator to parametrize the test with a couple of ``org`` examples to pass to ``GithubOrgClient``, in this order:
- ``google``
- ``abc``
Of course, no external HTTP calls should be made.

### 5. Mocking a property
``memoize`` turns methods into properties. Read up on how to mock a property (see resource).
Implement the ``test_public_repos_url`` method to unit-test ``GithubOrgClient._public_repos_url``.
Use ``patch`` as a context manager to patch ``GithubOrgClient.org`` and make it return a known payload.
Test that the result of ``_public_repos_url`` is the expected one based on the mocked payload.

### 6. More patching
Implement ``TestGithubOrgClient.test_public_repos`` to unit-test ``GithubOrgClient.public_repos``.
Use ``@patch`` as a decorator to mock ``get_json`` and make it return a payload of your choice.
Use ``patch`` as a context manager to mock ``GithubOrgClient._public_repos_url`` and return a value of your choice.
Test that the list of repos is what you expect from the chosen payload.
Test that the mocked property and the mocked ``get_json`` was called once.

### 7. Parameterize
Implement ``TestGithubOrgClient.test_has_license`` to unit-test ``GithubOrgClient.has_license``.
Parametrize the test with the following inputs
```python
repo={"license": {"key": "my_license"}}, license_key="my_license"
repo={"license": {"key": "other_license"}}, license_key="my_license"
```
You should also parameterize the expected returned value.

### 8. Integration test: fixtures
We want to test the ``GithubOrgClient.public_repos`` method in an integration test. That means that we will only mock code that sends external requests.
Create the ``TestIntegrationGithubOrgClient(unittest.TestCase)`` class and implement the ``setUpClass`` and ``tearDownClass`` which are part of the ``unittest.TestCase`` API.
Use ``@parameterized_class`` to decorate the class and parameterize it with fixtures found in ``fixtures.py``. The file contains the following fixtures:
```python
org_payload, repos_payload, expected_repos, apache2_repos
```
The ``setupClass`` should mock ``requests.get`` to return example payloads found in the fixtures.
Use ``patch`` to start a patcher named ``get_patcher``, and use ``side_effect`` to make sure the mock of ``requests.get(url).json()`` returns the correct fixtures for the various values of url that you anticipate to receive.
Implement the ``tearDownClass`` class method to stop the patcher.

### 9. Integration tests
Implement the ``test_public_repos`` method to test ``GithubOrgClient.public_repos``.
Make sure that the method returns the expected results based on the fixtures.
Implement ``test_public_repos_with_license`` to test the ``public_repos`` with the argument ``license="apache-2.0"`` and make sure the result matches the expected value from the fixtures.