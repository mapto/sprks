__author__ = 'Horace'


class update_helper:
    @staticmethod
    def stringify(table, where, values):
        """
        Turns parameters into SQL UPDATE query (table_name/string, WHERE/dict, VALUES/dict
        """
        return "UPDATE `" + table + "` SET " + string_helper.dict_to_sql_query(values) + " WHERE " + ' AND '.join(
            string_helper.pairs_to_strings(where)) + ';'


class string_helper:
    @staticmethod
    def pairs_to_strings(dict):
        """
        Converts dictionary key/value pairs to list{"key='value'", "key2='value'", ...}
        """
        list = []
        for key, value in sorted(dict.iteritems()):
            list.append(key + "='" + str(value) + "'")

        return list

    @staticmethod
    def dict_to_sql_query(dict):
        """
        Converts dictionary to sql-compliant string: key1='value1',key2='value2',...
        """
        return ', '.join(string_helper.pairs_to_strings(dict));