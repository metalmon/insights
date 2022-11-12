# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

import unittest

import frappe

from .sql_builder import SQLQueryBuilder


class TestSQLBuilder(unittest.TestCase):
    def test_connection_to_site_db(self):
        conn_args = {
            "data_source": "Test Site Connection",
            "database_name": frappe.conf.db_name,
            "username": frappe.conf.db_name,
            "password": frappe.conf.db_password,
            "host": "localhost",
            "port": 3306,
            "use_ssl": False,
        }

        from insights.insights.doctype.insights_data_source.sources.frappe_db import (
            FrappeDB,
        )

        frappe_db = FrappeDB(**conn_args)
        self.assertTrue(frappe_db.test_connection())
        self.site_db = frappe_db

    def test_query(self):
        self.test_connection_to_site_db()
        builder = SQLQueryBuilder()
        doc = frappe.get_doc(TEST_QUERY)
        sql = builder.build(doc, dialect=self.site_db.engine.dialect)
        self.assertTrue(sql)


TEST_QUERY = {
    "doctype": "Insights Query",
    "title": "Test Todo Count",
    "data_source": "Site DB",
    "tables": [
        {
            "label": "ToDo",
            "table": "tabToDo",
            "doctype": "Insights Query Table",
            "join": {
                "with": {"label": "User", "value": "tabUser"},
                "condition": {"label": "owner = name", "value": "owner = name"},
                "type": {"label": "Right", "value": "right"},
            },
        },
    ],
    "columns": [
        {
            "label": "Name",
            "column": "name",
            "doctype": "Insights Query Column",
            "table": "tabToDo",
            "table_label": "ToDo",
        },
        {
            "label": "Due Date",
            "column": "date",
            "type": "Date",
            "table": "tabToDo",
            "table_label": "ToDo",
            "aggregation": "Group By",
            "format_option": '{\n  "date_format": "Month"\n}',
            "doctype": "Insights Query Column",
        },
    ],
    "filters": {
        "type": "LogicalExpression",
        "operator": "&&",
        "level": 1,
        "position": 1,
        "conditions": [
            {
                "type": "BinaryExpression",
                "operator": "=",
                "left": {
                    "type": "Column",
                    "value": {"column": "status", "table": "tabToDo"},
                },
                "right": {"type": "String", "value": "Open"},
            }
        ],
    },
}
