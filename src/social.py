import webapp2
import os

from google.appengine.api import users
from jinja2 import Environment, FileSystemLoader


class Social(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
            return

        error = {
            'msg_1': "Error: ",
            'msg_2': "You tried to create a new stream",
            'msg_3': "whose name is the same as an existing stream;",
            'msg_4': "operation did not complete",
            'msg_5': "Or this page does not exist"
        }
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        template = env.get_template('social.html')

        self.response.write(template.render(error))


app = webapp2.WSGIApplication([
    ('/social', Social),
    ('/.*', Social),
], debug=True)
