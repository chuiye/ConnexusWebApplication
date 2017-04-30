import webapp2
import os
import json
from google.appengine.api import users
from jinja2 import Environment, FileSystemLoader

from components import streambook_key, Stream


class Search(webapp2.RequestHandler):
    initial = True
    found = False
    search_tag = None

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
            return

        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        template = env.get_template('search.html')

        all_streams = Stream.query(
            ancestor=streambook_key()) \
            .order(-Stream.date) \
            .fetch()

        keywords = []

        for stream in all_streams:
            keywords.append(stream.name)
            for tags in stream.tag:
                if tags not in keywords:
                    keywords.append(tags)

        Search.initial = True

        init = {
            'initial': Search.initial,
            'keywords': json.dumps(keywords)
        }

        self.response.write(template.render(init))

    def post(self):
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        template = env.get_template('search.html')

        all_streams = Stream.query(
            ancestor=streambook_key()) \
            .order(-Stream.date) \
            .fetch()

        Search.found = False
        Search.initial = False
        streams = []
        keywords = []

        for stream in all_streams:
            keywords.append(stream.name)
            for tags in stream.tag:
                if tags not in keywords:
                    keywords.append(tags)

        Search.search_tag = self.request.get("tagsforsearch")

        for stream in all_streams:
            if Search.search_tag in stream.name:
                streams.append(stream)
                Search.found = True
            else:
                for tag in stream.tag:
                    if Search.search_tag in tag:
                        streams.append(stream)
                        Search.found = True
                        break

        num_stream = len(streams)
        if Search.search_tag == "":
            Search.found = False
            num_stream = 0

        stream_found = {
            'found': Search.found,
            'initial': Search.initial,
            'streams': streams,
            'num_stream': num_stream,
            'search_tags': Search.search_tag,
            'keywords': json.dumps(keywords)
        }

        self.response.write(template.render(stream_found))


class SearchMobile(webapp2.RequestHandler):
    def get(self):
        all_streams = Stream.query(
            ancestor=streambook_key()) \
            .order(-Stream.date) \
            .fetch()

        streams = []
        search_tag = self.request.get("search_tag")

        if search_tag:
            for stream in all_streams:
                if search_tag in stream.name:
                    streams.append(stream)
                else:
                    for tag in stream.tag:
                        if search_tag in tag:
                            streams.append(stream)
                            break

        stream_names = [stream.name for stream in streams]
        cover_img_urls = [stream.cover_img for stream in streams]

        data = {'CoverImageList': cover_img_urls, 'StreamNameList': stream_names}
        json_data = json.dumps(data)

        self.response.write(json_data)


class RebuildIndex(webapp2.RequestHandler):
    be_click = 0

    def post(self):
        RebuildIndex.be_click = 1
        self.redirect('/search')


class Cronrebuildindex_day(webapp2.RequestHandler):
    def get(self):
        if RebuildIndex.be_click == 1:
            if Search.initial == True:

                env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
                template = env.get_template('search.html')

                all_streams = Stream.query(
                    ancestor=streambook_key()) \
                    .order(-Stream.date) \
                    .fetch()

                keywords = []

                for stream in all_streams:
                    keywords.append(stream.name)
                    for tags in stream.tag:
                        if tags not in keywords:
                            keywords.append(tags)

                init = {
                    'initial': Search.initial,
                    'keywords': json.dumps(keywords)
                }

                # self.response.write('cron works')

                self.response.write(template.render(init))

            elif Search.initial == False:
                env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
                template = env.get_template('search.html')

                all_streams = Stream.query(
                    ancestor=streambook_key()) \
                    .order(-Stream.date) \
                    .fetch()

                streams = []
                keywords = []

                for stream in all_streams:
                    keywords.append(stream.name)
                    for tags in stream.tag:
                        if tags not in keywords:
                            keywords.append(tags)

                for stream in all_streams:
                    if Search.search_tag in stream.name:
                        streams.append(stream)
                        Search.found = True
                    else:
                        for tag in stream.tag:
                            if Search.search_tag in tag:
                                streams.append(stream)
                                Search.found = True
                                break

                num_stream = len(streams)

                stream_found = {
                    'found': Search.found,
                    'initial': Search.initial,
                    'streams': streams,
                    'num_stream': num_stream,
                    'search_tags': Search.search_tag,
                    'keywords': json.dumps(keywords)
                }

                self.response.write(template.render(stream_found))


app = webapp2.WSGIApplication([
    ('/search', Search),
    ('/search_mobile', SearchMobile),
    ('/rebuildindex.action', RebuildIndex),
    ('/cronrebuildindex_day', Cronrebuildindex_day)
], debug=True)
