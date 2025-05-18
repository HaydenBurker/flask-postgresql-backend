import json

import psycopg2
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import Response

from db import connection

def internal_error():
    return Response(json.dumps({"message": "internal server error"}), 500)

class ExceptionHandlerMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except HTTPException as e:
            response = Response(str(e), e.code)
            return response(environ, start_response)
        except psycopg2.Error as e:
            print("psycopg2 error: " + str(e))
            response = internal_error()
            connection.rollback()
            return response(environ, start_response)
        except Exception as e:
            print("internal server error: " + str(e))
            response = internal_error()
            return response(environ, start_response)
