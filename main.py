# [START imports]
import os
import urllib

from google.appengine.api import users

from jinja2 import Environment,  FileSystemLoader
import webapp2
# [END imports]


# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/management')
            return
            #url = users.create_logout_url('/')
            #self.redirect(url)

        JINJA_ENVIRONMENT = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        template = JINJA_ENVIRONMENT.get_template('index.html')
        greeting = users.create_login_url('/')
        template_values = {
            'greeting': greeting
        }

        self.response.write(template.render(template_values))
# [END main_page]


class Logout(webapp2.RequestHandler):
    def get(self):
        url = users.create_logout_url('/')
        self.redirect(url)


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/logout', Logout),
], debug=True)
# [END app]
