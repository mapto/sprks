__author__ = 'Horace'

from libraries.db_helper import *


class TestUpdateHelper:

    def setup_method(self, method):
        self.list1 = {'list1_key1': 'list1_value1', 'list1_key2': 'list1_value2', 'list1_key3': 'list1_value3'}
        self.list2 = {'list2_key1': 'list2_value1', 'list2_key2': 'list2_value2', 'list2_key3': 'list2_value3'}

    def test_stringify(self):
        assert update_helper.stringify("Table1", self.list1, self.list2) == \
               "UPDATE `Table1` SET list2_key1='list2_value1', list2_key2='list2_value2', list2_key3='list2_value3' " \
               "WHERE list1_key1='list1_value1' AND list1_key2='list1_value2' AND list1_key3='list1_value3';"


class TestStringHelper:

    def setup_method(self, method):
        self.dict = {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}

    def test_pairs_to_strings(self):
        """
        Test coversion from dict to list of "key0='value0'" strings
        """
        assert string_helper.pairs_to_strings(self.dict) == ["key1='value1'", "key2='value2'", "key3='value3'"]

    def test_dict_to_sql_query(self):
        """
        Test conversion from dictionary of pairs to sql-compliant key1='value1',key2='value2'...
        """
        assert string_helper.dict_to_sql_query(self.dict) == "key1='value1', key2='value2', key3='value3'"