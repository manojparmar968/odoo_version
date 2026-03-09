import functools
import json
import ast
from odoo.http import request
from odoo import http
from odoo.http import Response
from odoo.tools import date_utils

def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }

def return_Response(res):
    return http.Response(
        json.dumps(res),
        status=200,
        mimetype='application/json'
    )

def return_Response_error(res):
    return http.Response(
        json.dumps(res),
        status=400,
        mimetype='application/json'
    )
