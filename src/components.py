from google.appengine.ext import ndb

DEFAULT_STREAMBOOK_NAME = 'default_streambook'


def streambook_key(streambook_name=DEFAULT_STREAMBOOK_NAME):
    return ndb.Key('Stream', streambook_name)


class Author(ndb.Model):
    identity = ndb.StringProperty()
    email = ndb.StringProperty()


class Photo(ndb.Model):
    name = ndb.StringProperty()
    lat = ndb.FloatProperty()
    long = ndb.FloatProperty()
    date = ndb.DateTimeProperty()
    img_key = ndb.BlobKeyProperty()


class Stream(ndb.Model):
    author = ndb.StructuredProperty(Author)
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    view_dates = ndb.DateTimeProperty(repeated=True)
    tag = ndb.StringProperty(repeated=True)
    subscriber = ndb.StringProperty(repeated=True)
    num_of_views = ndb.IntegerProperty()
    invite_msg = ndb.StringProperty()
    cover_img = ndb.StringProperty()
    last_img_date = ndb.DateTimeProperty()
    num_of_imgs = ndb.IntegerProperty()

