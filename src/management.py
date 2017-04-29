import webapp2

from google.appengine.api import users
from google.appengine.ext import blobstore
from jinja2 import Environment, PackageLoader

from components import streambook_key, Stream, Photo


class Management(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
            return

        env = Environment(loader=PackageLoader('main', 'templates'))
        template = env.get_template('management.html')

        streams = Stream.query(
            Stream.author.identity == user.user_id(),
            ancestor=streambook_key()) \
            .order(-Stream.date) \
            .fetch()

        all_streams = Stream.query(
            ancestor=streambook_key()) \
            .order(-Stream.date) \
            .fetch()

        for stream in streams:
            imgs = Photo.query(
                ancestor=stream.key) \
                .order(-Photo.date) \
                .fetch()
            if imgs:
                stream.last_img_date = imgs[0].date
                stream.num_of_imgs = len(imgs)
                stream.put()

        sub_streams = []
        for stream in all_streams:
            if user.email() in stream.subscriber:
                sub_streams.append(stream)

        management_values = {
            'streams': streams,
            'sub_streams': sub_streams,
        }

        self.response.write(template.render(management_values))


class CreateStream(webapp2.RequestHandler):
    def post(self):
        self.redirect('/create')


class DeleteStream(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        streams = Stream.query(
            Stream.author.identity == user.user_id(),
            ancestor=streambook_key()) \
            .fetch()

        for stream in streams:
            if self.request.get(stream.name) == 'on':
                imgs = Photo.query(
                    ancestor=stream.key) \
                    .fetch()
                for img in imgs:
                    blobstore.delete(img.img_key)
                    img.key.delete()
                stream.key.delete()

        self.redirect('/management')


class Unsubscribe(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        streams = Stream.query(
            ancestor=streambook_key()) \
            .fetch()

        for stream in streams:
            if self.request.get(stream.name) == 'on':
                stream.subscriber.remove(user.email())
                stream.put()

        self.redirect('/management')


app = webapp2.WSGIApplication([
    ('/management', Management),
    ('/create_stream', CreateStream),
    ('/delete_stream', DeleteStream),
    ('/unsubscribe', Unsubscribe),
], debug=True)
