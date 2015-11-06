"""test_request.py"""
# pylint: disable=missing-docstring,line-too-long

from unittest import TestCase, main
import itertools
import json

from jsonrpcclient.request import Notification, Request, _sort_request
from jsonrpcclient.id_iterators import hex_iterator


class TestSortRequest(TestCase):

    def test(self):
        self.assertEqual(
            '{"jsonrpc": "2.0", "method": "add", "params": [2, 3], "id": 2}',
            json.dumps(_sort_request({'id': 2, 'params': [2, 3], 'method': 'add', 'jsonrpc': '2.0'})),
        )


class TestNotification(TestCase):

    def test(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'get'},
            Notification('get')
        )

    def test_str(self):
        self.assertEqual(
            '{"jsonrpc": "2.0", "method": "get"}',
            str(Notification('get'))
        )

    def test_method_name_directly(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'cat'},
            Notification.cat()
        )

    def test_positional(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'sqrt', 'params': [1]},
            Notification('sqrt', 1)
        )

    def test_keyword(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': {'name': 'Foo'}},
            Notification('find', name='Foo')
        )

    def test_both_positional_and_keyword(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': ['Foo', {'age': 42}]},
            Notification('find', 'Foo', age=42)
        )


class TestRequest(TestCase):

    def setUp(self):
        # Start each test with id 1
        Request.id_iterator = itertools.count(1)

    def tearDown(self):
        # Restore default iterator
        Request.id_iterator = itertools.count(1)

    def test(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'get', 'id': 1},
            Request('get'))

    def test_str(self):
        self.assertEqual(
            '{"jsonrpc": "2.0", "method": "get", "id": 1}',
            str(Request('get')))

    def test_method_name_directly(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'cat', 'id': 1},
            Request.cat())

    def test_positional(self):
        self.assertEqual(
                {'jsonrpc': '2.0', 'method': 'sqrt', 'params': [1], 'id': 1},
            Request('sqrt', 1))

    def test_keyword(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'find', 'params': {'name': 'Foo'}, 'id': 1},
            Request('find', name='Foo'))

    def test_specified_id(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'get', 'id': 'Request #1'},
            Request('get', request_id='Request #1'))

    def test_auto_iterating_id(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'id': 1},
            Request('go'))
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'id': 2},
            Request('go'))

    def test_specified_id(self):
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'cat', 'id': 'Request 1'},
            Request.cat(request_id='Request 1'))

    def test_custom_iterator(self):
        Request.id_iterator = hex_iterator(10)
        self.assertEqual(
            {'jsonrpc': '2.0', 'method': 'go', 'id': 'a'},
            Request('go'))


if __name__ == '__main__':
    main()
