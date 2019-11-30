from flask import jsonify, redirect


class HTTPBaseResponese(tuple):
    def __new__(cls, resp, status_code=200, cookies={}):
        for c in cookies:
            if cookies[c] == None:
                resp.delete_cookie(c)
            else:
                resp.set_cookie(c, cookies[c])
        return super().__new__(tuple, (resp, status_code))


class HTTPResponse(HTTPBaseResponese):
    def __new__(cls,
                message='',
                status_code=200,
                status='ok',
                data=None,
                cookies={}):
        resp = jsonify({
            'status': status,
            'message': message,
            'data': data,
        })
        return super().__new__(HTTPBaseResponese, resp, status_code, cookies)


class HTTPRedirect(HTTPBaseResponese):
    def __new__(cls, location, status_code=302, cookies={}):
        resp = redirect(location)
        return super().__new__(HTTPBaseResponese, resp, status_code, cookies)


class HTTPError(HTTPResponse):
    def __new__(cls, message, status_code, data=None):
        return super().__new__(HTTPResponse, message, status_code, 'err', data)
