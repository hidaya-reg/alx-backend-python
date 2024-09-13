#!/usr/bin/env python3
""" Unit tests for memoization in utils """

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Test cases for memoize decorator"""

    def test_memoize(self):
        """Test the memoize decorator."""

        class TestClass:
            """Test class with a method and a memoized property."""

            def a_method(self):
                """Regular method that returns 42."""
                return 42

            @memoize
            def a_property(self):
                """Memoized method that calls a_method."""
                return self.a_method()

        # Create an instance of TestClass
        test_obj = TestClass()

        # Patch a_method to track how many times it's called
        with patch.object(
            TestClass, 'a_method', return_value=42
        ) as mock_method:
            # Access a_property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Check that the result is correct both times
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was called only once
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
