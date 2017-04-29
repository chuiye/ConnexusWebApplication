import webapp2
import datetime
import json

from google.appengine.api import users
from google.appengine.api import images

from jinja2 import Environment, PackageLoader

from components import streambook_key, Stream, Photo


class ViewAllStream(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
            return

        env = Environment(loader=PackageLoader('main', 'templates'))
        template = env.get_template('view.html')

        streams = Stream.query(
            ancestor=streambook_key()) \
            .order(Stream.date) \
            .fetch()

        all_stream = {
            'streams': streams,
        }

        self.response.write(template.render(all_stream))


class ViewAllStreamMobile(webapp2.RequestHandler):
    def get(self):
        streams = Stream.query(
            ancestor=streambook_key()) \
            .order(Stream.date) \
            .fetch()

        stream_names = [stream.name for stream in streams]
        cover_img_urls = [stream.cover_img for stream in streams]

        data = {
            'CoverImageList': cover_img_urls,
            'StreamNameList': stream_names
        }
        json_data = json.dumps(data)

        self.response.write(json_data)


class ViewSubscribedStreamMobile(webapp2.RequestHandler):
    def get(self):
        user_email = self.request.get("email")

        all_streams = Stream.query(
            ancestor=streambook_key()) \
            .order(-Stream.date) \
            .fetch()

        sub_streams = []
        for stream in all_streams:
            if user_email in stream.subscriber:
                sub_streams.append(stream)

        stream_names = [stream.name for stream in sub_streams]
        cover_img_urls = [stream.cover_img for stream in sub_streams]

        data = {
            'CoverImageList': cover_img_urls,
            'StreamNameList': stream_names
        }
        json_data = json.dumps(data)

        self.response.write(json_data)


class ViewStream(webapp2.RequestHandler):
    not_view = 0

    def get(self):
        try:
            user = users.get_current_user()
            if not user:
                self.redirect('/')
                return

            env = Environment(loader=PackageLoader('main', 'templates'))
            template = env.get_template('stream.html')

            stream_name = self.request.get("name")
            stream = Stream.query(
                Stream.name == stream_name,
                ancestor=streambook_key()) \
                .fetch()
            if stream:
                stream = stream[0]

            image_id = self.request.get("id")
            if image_id:
                image_id = int(image_id)
            else:
                image_id = 0

            more_images = True
            imgs = Photo.query(
                ancestor=stream.key) \
                .order(-Photo.date) \
                .fetch()
            num_image = len(imgs)

            if num_image > 3:
                last_id = num_image
                if last_id > image_id + 3:
                    imgs = imgs[image_id:image_id + 3]
                else:
                    imgs = imgs[image_id:last_id]
                    more_images = False

            subscribed = False
            user_id = user.user_id()
            user_email = user.email()

            if user_id == stream.author.identity:
                user_true = True
            else:
                user_true = False
                if user_email in stream.subscriber:
                    subscribed = True
                if ViewStream.not_view == 0:
                    stream.num_of_views += 1
                    stream.view_dates.append(datetime.datetime.now())
                else:
                    ViewStream.not_view = 0
                stream.put()

            img_thumburls = [images.get_serving_url(img.img_key) for img in imgs]
            img_urls = [img_url + '=s0' for img_url in img_thumburls]
            img_with_urls = zip(imgs, img_urls, img_thumburls)

            view_stream = {
                'id': image_id,
                'imgs': img_with_urls,
                'stream': stream,
                'num_image': num_image,
                'more_images': more_images,
                'user_true': user_true,
                'subscribed': subscribed,
            }

            self.response.write(template.render(view_stream))

        except:
            self.redirect('/social')

    def post(self):
        ViewStream.not_view = 1
        stream_name = self.request.get("name")
        image_id = int(self.request.get("id"))

        self.redirect('/stream?name=%s&id=%s' % (stream_name, image_id))


class ViewStreamMobile(webapp2.RequestHandler):
    def get(self):
        stream_name = self.request.get("name")
        stream = Stream.query(
            Stream.name == stream_name,
            ancestor=streambook_key()) \
            .fetch()
        if stream:
            stream = stream[0]

        imgs = Photo.query(
            ancestor=stream.key) \
            .order(-Photo.date) \
            .fetch()

        stream.num_of_views += 1
        stream.view_dates.append(datetime.datetime.now())
        stream.put()

        img_urls = [images.get_serving_url(img.img_key) for img in imgs]
        img_caps = [img.name for img in imgs]

        data = {
            'ImageList': img_urls,
            'ImageCaptionList': img_caps,
            'UserEmail': stream.author.email
        }
        json_data = json.dumps(data)

        self.response.write(json_data)


class Subscribe(webapp2.RequestHandler):
    def post(self):
        json_str = self.request.body
        json_obj = json.loads(json_str)
        stream_name = json_obj['name']
        user_email = users.get_current_user().email()

        stream = Stream.query(
            Stream.name == stream_name,
            ancestor=streambook_key()) \
            .fetch()
        if stream:
            stream = stream[0]
        if user_email not in stream.subscriber:
            stream.subscriber.append(user_email)
            stream.put()


class Unsubscribe(webapp2.RequestHandler):
    def post(self):
        json_str = self.request.body
        json_obj = json.loads(json_str)
        stream_name = json_obj['name']
        user_email = users.get_current_user().email()

        stream = Stream.query(
            Stream.name == stream_name,
            ancestor=streambook_key()) \
            .fetch()
        if stream:
            stream = stream[0]
        if user_email in stream.subscriber:
            stream.subscriber.remove(user_email)
            stream.put()


app = webapp2.WSGIApplication([
    ('/view', ViewAllStream),
    ('/view_all_streams', ViewAllStreamMobile),
    ('/view_subscribed_streams', ViewSubscribedStreamMobile),
    ('/stream', ViewStream),
    ('/view_a_stream', ViewStreamMobile),
    ('/subscribe.action', Subscribe),
    ('/unsubscribe.action', Unsubscribe),
], debug=True)
