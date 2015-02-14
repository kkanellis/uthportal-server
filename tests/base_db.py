
import unittest

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.entry = { 'hello' : 'world' }
        self.new_entry = { 'hello' : 'universe' }

    def routine(self):
        self.assertTrue(self.manager.connect())
        self.assertTrue(self.manager.insert_document('test', self.entry))

        self.assertIsNone(self.manager.find_document('test', { 'hello' : 'World' }))
        self.assertIsNone(self.manager.find_document('test.test', { 'hello' : 'world'}))

        self.assertDictContainsSubset(self.entry, self.manager.find_document('test', { }))
        self.assertDictContainsSubset(self.entry, self.manager.find_document('test', { 'hello': 'world'}))

        self.assertTrue(self.manager.update_document('test', self.entry, self.new_entry ))
        self.assertIsNone(self.manager.find_document('test', { 'hello' : 'world' }))

        self.assertTrue(self.manager.remove_document('test', { 'HELLO' : 'world' }))
        self.assertTrue(self.manager.remove_document('test', self.entry))
        self.assertDictContainsSubset(self.new_entry , self.manager.find_document('test', { 'hello' : 'universe' }))

        self.assertTrue(self.manager.remove_document('test', { 'hello': 'universe' }))
        self.assertIsNone(self.manager.find_document('test', self.entry))
        self.assertTrue(self.manager.disconnect())

