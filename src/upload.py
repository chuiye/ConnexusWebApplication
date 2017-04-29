# -*- coding: utf-8 -*-
#
# jQuery File Upload Plugin GAE Python Example
# https://github.com/blueimp/jQuery-File-Upload
#
# Copyright 2011, Sebastian Tschan
# https://blueimp.net
#
# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT
#
import datetime
import logging

from google.appengine.api import memcache
from google.appengine.ext import blobstore, ndb
from google.appengine.ext.webapp import blobstore_handlers
import json
import os
import re
import urllib
import webapp2
from components import Photo, Stream, streambook_key

DEBUG = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')
WEBSITE = '/'
MIN_FILE_SIZE = 1  # bytes
# Max file size is memcache limit (1MB) minus key size minus overhead:
MAX_FILE_SIZE = 999000  # bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES
THUMB_MAX_WIDTH = 80
THUMB_MAX_HEIGHT = 80
THUMB_SUFFIX = '.' + str(THUMB_MAX_WIDTH) + 'x' + str(THUMB_MAX_HEIGHT) + '.png'
EXPIRATION_TIME = 300  # seconds
# If set to None, only allow redirects to the referer protocol+host.
# Set to a regexp for custom pattern matching against the redirect value:
REDIRECT_ALLOW_TARGET = None


class CORSHandler(webapp2.RequestHandler):
    def cors(self):
        headers = self.response.headers
        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Methods'] = \
            'OPTIONS, HEAD, GET, POST, DELETE'
        headers['Access-Control-Allow-Headers'] = \
            'Content-Type, Content-Range, Content-Disposition'

    def initialize(self, request, response):
        super(CORSHandler, self).initialize(request, response)
        self.cors()

    def json_stringify(self, obj):
        return json.dumps(obj, separators=(',', ':'))

    def options(self, *args, **kwargs):
        pass


class UploadHandler(CORSHandler, blobstore_handlers.BlobstoreUploadHandler):
    def validate(self, file):
        if file['size'] < MIN_FILE_SIZE:
            file['error'] = 'File is too small'
        elif file['size'] > MAX_FILE_SIZE:
            file['error'] = 'File is too big'
        elif not ACCEPT_FILE_TYPES.match(file['type']):
            file['error'] = 'Filetype not allowed'
        else:
            return True
        return False

    def validate_redirect(self, redirect):
        if redirect:
            if REDIRECT_ALLOW_TARGET:
                return REDIRECT_ALLOW_TARGET.match(redirect)
            referer = self.request.headers['referer']
            if referer:
                from urlparse import urlparse
                parts = urlparse(referer)
                redirect_allow_target = '^' + re.escape(
                    parts.scheme + '://' + parts.netloc + '/'
                )
            return re.match(redirect_allow_target, redirect)
        return False

    @ndb.transactional
    def write_data(self, stream, img_upload):
        img_name = img_upload.filename[:-4]
        img_key = img_upload.key()
        img_date = datetime.datetime.now()
        img_entity_key = ndb.Key(Photo, img_name, parent=stream.key)
        img = Photo(key=img_entity_key, name=img_name, date=img_date,
                    lat=0, long=0, img_key=img_key)
        img.put()

    def handle_upload(self):
        results = []
        stream_name = self.request.get('name')
        stream = Stream.query(
            Stream.name == stream_name,
            ancestor=streambook_key()) \
            .fetch()[0]
        for img_upload in self.get_uploads():
            result = {'name': urllib.unquote(img_upload.filename),
                      'type': img_upload.content_type,
                      'size': img_upload.size}
            if self.validate(result):
                self.write_data(stream, img_upload)
            results.append(result)

        return results

    def head(self):
        pass

    def get(self):
        self.redirect(WEBSITE)

    def post(self):
        result = {'files': self.handle_upload()}
        s = self.json_stringify(result)
        redirect = self.request.get('redirect')
        if self.validate_redirect(redirect):
            return self.redirect(str(
                redirect.replace('%s', urllib.quote(s, ''), 1)
            ))
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        self.response.write(s)


class UploadHandlerMobile(UploadHandler):
    def handle_upload(self):
        results = []
        stream_name = self.request.get('name')
        stream = Stream.query(
            Stream.name == stream_name,
            ancestor=streambook_key()) \
            .fetch()[0]

        img_name = self.request.get('photoCaption')
        img_lat = float(self.request.get('location[latitude]'));
        img_long = float(self.request.get('location[longitude]'));
        img_upload = self.get_uploads()[0]
        result = {'name': img_name,
                  'type': img_upload.content_type,
                  'size': img_upload.size}
        logging.debug("name = %s, type = %s, size = %d , lat = %f, long = %f"
                      % (result['name'], result['type'], result['size'], img_lat, img_long))
        if self.validate(result):
            img_key = img_upload.key()
            img_date = datetime.datetime.now()
            img_entity_key = ndb.Key(Photo, img_name, parent=stream.key)
            img = Photo(key=img_entity_key, name=img_name, date=img_date,
                        lat=img_lat, long=img_long, img_key=img_key)
            img.put()
        results.append(result)

        return results

    def post(self):
        result = {'files': self.handle_upload()}
        s = self.json_stringify(result)
        redirect = self.request.get('redirect')
        if self.validate_redirect(redirect):
            return self.redirect(str(
                redirect.replace('%s', urllib.quote(s, ''), 1)
            ))
        self.response.write(s)


class FileHandler(CORSHandler):
    def normalize(self, str):
        return urllib.quote(urllib.unquote(str), '')

    def get(self, content_type, data_hash, file_name):
        content_type = self.normalize(content_type)
        file_name = self.normalize(file_name)
        key = content_type + '/' + data_hash + '/' + file_name
        data = memcache.get(key)
        if data is None:
            return self.error(404)
        # Prevent browsers from MIME-sniffing the content-type:
        self.response.headers['X-Content-Type-Options'] = 'nosniff'
        content_type = urllib.unquote(content_type)
        if not IMAGE_TYPES.match(content_type):
            # Force a download dialog for non-image types:
            content_type = 'application/octet-stream'
        elif file_name.endswith(THUMB_SUFFIX):
            content_type = 'image/png'
        self.response.headers['Content-Type'] = content_type
        # Cache for the expiration time:
        self.response.headers['Cache-Control'] = 'public,max-age=%d' \
                                                 % EXPIRATION_TIME
        self.response.write(data)


class UploadUrlHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload-handler')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write('"' + upload_url + '"')


class GetUploadURL(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload_mobile')

        data = {'upload_url': upload_url}
        json_data = json.dumps(data)

        self.response.write(json_data)


app = webapp2.WSGIApplication(
    [
        ('/get_upload_url', GetUploadURL),
        ('/upload_mobile', UploadHandlerMobile),
        ('/upload-handler', UploadHandler),
        ('/upload-url-handler', UploadUrlHandler),
        ('/(.+)/([^/]+)/([^/]+)', FileHandler),
    ],
    debug=DEBUG
)
