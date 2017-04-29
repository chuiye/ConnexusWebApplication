import webapp2

from google.appengine.api import mail
from google.appengine.api import users

from jinja2 import Environment, PackageLoader
from components import Stream, streambook_key, Author


class Create(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
            return

        env = Environment(loader=PackageLoader('main', 'templates'))
        template = env.get_template('create.html')
        self.response.write(template.render())


class NewStream(webapp2.RequestHandler):
    def post(self):
        stream = Stream(parent=streambook_key())
        user = users.get_current_user()
        if user:
            stream.author = Author(
                identity=user.user_id(),
                email=user.email())
        stream_name = self.request.get('streamname').strip()
        if not stream_name:
            self.redirect('/management')
            return

        streams = Stream.query(
            Stream.name == stream_name,
            ancestor=streambook_key()) \
            .fetch()
        if streams:
            self.redirect('/social')
            return

        stream.name = stream_name
        stream.num_of_views = 0
        stream.num_of_imgs = 0
        subscriber = self.request.get('subscriber')
        if subscriber:
            stream.subscriber = subscriber.split(',')
            if user.email() in stream.subscriber:
                stream.subscriber.remove(user.email())
        else:
            stream.subscriber = []
        stream.invite_msg = self.request.get('message')
        stream.tag = self.request.get('tag').split(',')
        stream.cover_img = self.request.get('urlcover')
        if not stream.cover_img:
            stream.cover_img = "img/no_image_available.png"

        for sub in stream.subscriber:
            message = mail.EmailMessage()
            message.to = sub
            message.body = """
            %s invites you to subscribe Stream:%s
            From %s: %s
            """ % (stream.author.email, stream.name, stream.author.email, stream.invite_msg)
            message.sender = stream.author.email
            message.subject = "Invitation Email from miniproject-js.appspot.com"
            message.send()

        stream.put()
        self.redirect('/management')


app = webapp2.WSGIApplication([
    ('/create', Create),
    ('/new_stream', NewStream),
], debug=True)
