import os
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

class Cup(object):
    def __init__(self, with_static=True):
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        if with_static:
            self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
                '/static':  os.path.join(os.path.dirname(__file__), 'static')
            })
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                 autoescape=True)
        self.url_map = Map()
        self.views = {}

    def add_url_rule(self, url, endpt, func):
        self.url_map.add(Rule(url, endpoint=endpt))
        self.views[endpt] = func

    def getView(self, endpoint):
        return self.views[endpoint]

    def route(self, func):
        self.add_url_rule('/', func.__name__, func)
        def decorator(*args, **kwargs):
            func(*args, **kwargs)
            return decorator

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            data = self.getView(endpoint)(request, **values)
            return Response(data)
        except HTTPException, e:
            print "e"
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def run(self, host, port, use_debugger=True, use_reloader=True):
        from werkzeug.serving import run_simple
        run_simple(host, port, self, use_debugger, use_reloader)

