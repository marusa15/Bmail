#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo
from google.appengine.api import users



template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            logiran = True
            logout_url = users.create_logout_url('/')
            params = {"logiran": logiran, "logout_url": logout_url, "user": user}
        else:
            logiran = False
            login_url = users.create_login_url('/')

            params = {"logiran": logiran, "login_url": login_url, "user": user}

        return self.render_template("hello.html", params=params)

class VnosHandler(BaseHandler): #poslje vnesene podatke v bazo
    def post(self):
        sender = self.request.get("Posiljatelj")
        recipient = self.request.get("Naslovnik")
        message_ = self.request.get("Message")

        sporocilo = Sporocilo(Posiljatelj = sender, Naslovnik = recipient, Message = message_)
        sporocilo.put()

        self.write("Sporocilo je bilo uspesno poslano")

class PoslanoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        seznam_poslano = Sporocilo.query(Sporocilo.Posiljatelj == user.email()).fetch()
        params = {"seznam_poslano": seznam_poslano, "user": user}
        self.render_template("Poslano.html", params=params)

class PrejetoHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        seznam_prejeto = Sporocilo.query(Sporocilo.Naslovnik == user.email()).fetch()
        params = {"seznam_prejeto": seznam_prejeto, "user": user}
        self.render_template("Prejeto.html", params=params)




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnos', VnosHandler),
    webapp2.Route('/poslano', PoslanoHandler, name = "poslano"),
    webapp2.Route('/prejeto', PrejetoHandler, name = "prejeto"),
], debug=True)
