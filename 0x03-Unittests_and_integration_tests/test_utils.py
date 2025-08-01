#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from utils import access_nested_map,get_json,memoize
from unittest.mock import patch,Mock

class TestAccessNestedMap(unittest.TestCase):
    
    
    @parameterized.expand([
         ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map,path,expected):
        result = access_nested_map(nested_map,path)
        self.assertEqual(result,expected)
        
    @parameterized.expand([
        ({},("a",),"a"),
        ({"a": 1},("a","b"),"b"),
    ])    
    def test_access_nested_map_exception(self,nested_map,path,expected_key):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map,path)
        self.assertEqual(str(context.exception), f"'{expected_key}'")
        
class TestGetJson(unittest.TestCase):
    @parameterized.expand([
          ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url,test_payload,mock_get):
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        
        result = get_json(test_url)
        
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result,test_payload)
        
class TestMemoize(unittest.TestCase):
    """Test a memoize function"""
    def test_memoize(self):
        """Test a memoize function"""
        class TestClass:
            """Test a class"""
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            test_class = TestClass()
            result1 = test_class.a_property
            result2 = test_class.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()

        
        
if __name__ == '__main__':
    unittest.main()