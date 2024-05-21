from tornado.web import url
from .extension import MakeAPaymentHandler

# url('/regex_pattern', HandlerClass, kwargs=None, name=None)
# http://www.tornadoweb.org/en/stable/web.html?#tornado.web.URLSpec

URL_PATTERNS = [
    url(r'/make_a_payment(?:/(?P<routing_key>[\w.-]+))?/?',
        MakeAPaymentHandler),
]
