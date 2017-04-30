import webapp2
import datetime
import os

from google.appengine.api import users
from google.appengine.api import mail
from jinja2 import Environment, FileSystemLoader

from components import streambook_key, Stream


class Trend(webapp2.RequestHandler):
    highlight = 0
    info = []

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect('/')
            return

        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
        template = env.get_template('trending.html')

        streams = Stream.query(
            ancestor=streambook_key()) \
            .order(-Stream.date) \
            .fetch()

        firststream = Stream(parent=streambook_key())
        secondstream = Stream(parent=streambook_key())
        thirdstream = Stream(parent=streambook_key())

        del Trend.info[:]

        for stream in streams:
            # self.response.write(stream.name)
            temp_num_views = 0
            present = datetime.datetime.now()
            # last_view_time = stream.view_dates[:-1]
            for time in stream.view_dates:
                time_diff = present - time
                if time_diff.days == 0:
                    if time_diff.seconds <= 3600:
                        temp_num_views = temp_num_views + 1
                    else:
                        stream.view_dates.remove(time)
                else:
                    stream.view_dates.remove(time)
            stream.put()
            if temp_num_views >= len(firststream.view_dates):
                thirdstream = secondstream
                secondstream = firststream
                firststream = stream
            elif temp_num_views >= len(secondstream.view_dates):
                thirdstream = secondstream
                secondstream = stream
            elif temp_num_views >= len(thirdstream.view_dates):
                thirdstream = stream
                # self.response.write(stream.view_dates)

        if len(streams) >= 3:
            top3 = {
                'firststream': firststream,
                'secondstream': secondstream,
                'thirdstream': thirdstream,
                'num_stream': 3,
                'highlight': Trend.highlight
            }
            f_tuple = (firststream.name, len(firststream.view_dates))
            s_tuple = (secondstream.name, len(secondstream.view_dates))
            t_tuple = (thirdstream.name, len(thirdstream.view_dates))
            Trend.info.append(f_tuple)
            Trend.info.append(s_tuple)
            Trend.info.append(t_tuple)
            self.response.write(template.render(top3))
        elif len(streams) >= 2:
            top3 = {
                'firststream': firststream,
                'secondstream': secondstream,
                'num_stream': 2,
                'highlight': Trend.highlight
            }
            f_tuple = (firststream.name, len(firststream.view_dates))
            s_tuple = (secondstream.name, len(secondstream.view_dates))
            Trend.info.append(f_tuple)
            Trend.info.append(s_tuple)
            self.response.write(template.render(top3))
        elif len(streams) >= 1:
            top3 = {
                'firststream': firststream,
                'num_stream': 1,
                'highlight': Trend.highlight
            }
            f_tuple = (firststream.name, len(firststream.view_dates))
            Trend.info.append(f_tuple)
            self.response.write(template.render(top3))
        else:
            top3 = {
                'num_stream': 0,
                'highlight': Trend.highlight
            }
            self.response.write(template.render(top3))


class TrendRight(webapp2.RequestHandler):
    email_func = 0
    email = ""

    def post(self):
        button = self.request.get("rate")

        user = users.get_current_user()
        TrendRight.email = user.email()
        Trend.highlight = 0

        if button == "no":
            Trend.highlight = 1
            TrendRight.email_func = 0
        elif button == "min":
            Trend.highlight = 2
            TrendRight.email_func = 1
        elif button == "hour":
            Trend.highlight = 3
            TrendRight.email_func = 2
        elif button == "day":
            Trend.highlight = 4
            TrendRight.email_func = 3
        self.redirect('/trending')


class Cronemail_min(webapp2.RequestHandler):
    def get(self):
        if TrendRight.email_func == 1:

            message = mail.EmailMessage()
            if len(Trend.info) == 3:

                message.body = """
				Five mins report:
				#1 Stream: %s     Number of Views in past hour: %s
				#2 Stream: %s	  Number of Views in past hour: %s
				#3 Stream: %s	  Number of Views in past hour: %s
			""" % (Trend.info[0][0], Trend.info[0][1], Trend.info[1][0], Trend.info[1][1], Trend.info[2][0],
                   Trend.info[2][1])
            elif len(Trend.info) == 2:
                message.body = """
				Five mins report:
				#1 Stream: %s     Number of Views in past hour: %s
				#2 Stream: %s	  Number of Views in past hour: %s	
			""" % (Trend.info[0][0], Trend.info[0][1], Trend.info[1][0], Trend.info[1][1])
            elif len(Trend.info) == 1:
                message.body = """
				Five mins report:
				#1 Stream: %s	  Number of Views in past hour: %s
			""" % (Trend.info[0][0], Trend.info[0][1])

            else:
                message.body = """
				Five mins report:
				No stream in Database yet
			"""
            message.sender = TrendRight.email
            message_to = ['nima.dini@utexas.edu', 'kevzsolo@gmail.com', 'songshuang1990@utexas.edu',
                          'lingxiao.jia@utexas.edu']
            for to in message_to:
                message.to = to
                message.send()


class Cronemail_hour(webapp2.RequestHandler):
    def get(self):
        if TrendRight.email_func == 2:
            message = mail.EmailMessage()
            if len(Trend.info) == 3:

                message.body = """
				Five mins report:
				#1 Stream: %s     Number of Views in past hour: %s
				#2 Stream: %s	  Number of Views in past hour: %s
				#3 Stream: %s	  Number of Views in past hour: %s
			""" % (Trend.info[0][0], Trend.info[0][1], Trend.info[1][0], Trend.info[1][1], Trend.info[2][0],
                   Trend.info[2][1])
            elif len(Trend.info) == 2:
                message.body = """
				Five mins report:
				#1 Stream: %s     Number of Views in past hour: %s
				#2 Stream: %s	  Number of Views in past hour: %s	
			""" % (Trend.info[0][0], Trend.info[0][1], Trend.info[1][0], Trend.info[1][1])
            elif len(Trend.info) == 1:
                message.body = """
				Five mins report:
				#1 Stream: %s	  Number of Views in past hour: %s
			""" % (Trend.info[0][0], Trend.info[0][1])

            else:
                message.body = """
				Five mins report:
				No stream in Database yet
			"""
            message.sender = TrendRight.email
            message_to = ['nima.dini@utexas.edu', 'kevzsolo@gmail.com', 'songshuang1990@utexas.edu',
                          'lingxiao.jia@utexas.edu']
            for to in message_to:
                message.to = to
                message.send()


class Cronemail_day(webapp2.RequestHandler):
    def get(self):
        if TrendRight.email_func == 3:
            message = mail.EmailMessage()
            if len(Trend.info) == 3:

                message.body = """
				Five mins report:
				#1 Stream: %s     Number of Views in past hour: %s
				#2 Stream: %s	  Number of Views in past hour: %s
				#3 Stream: %s	  Number of Views in past hour: %s
			""" % (Trend.info[0][0], Trend.info[0][1], Trend.info[1][0], Trend.info[1][1], Trend.info[2][0],
                   Trend.info[2][1])
            elif len(Trend.info) == 2:
                message.body = """
				Five mins report:
				#1 Stream: %s     Number of Views in past hour: %s
				#2 Stream: %s	  Number of Views in past hour: %s	
			""" % (Trend.info[0][0], Trend.info[0][1], Trend.info[1][0], Trend.info[1][1])
            elif len(Trend.info) == 1:
                message.body = """
				Five mins report:
				#1 Stream: %s	  Number of Views in past hour: %s
			""" % (Trend.info[0][0], Trend.info[0][1])

            else:
                message.body = """
				Five mins report:
				No stream in Database yet
			"""
            message.sender = TrendRight.email
            message_to = ['nima.dini@utexas.edu', 'kevzsolo@gmail.com', 'songshuang1990@utexas.edu',
                          'lingxiao.jia@utexas.edu']
            for to in message_to:
                message.to = to
                message.send()


class TrendLeft(webapp2.RequestHandler):
    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/trending', Trend),
    ('/trending_left', TrendLeft),
    ('/trending_right', TrendRight),
    ('/cronemail_min', Cronemail_min),
    ('/cronemail_hour', Cronemail_hour),
    ('/cronemail_day', Cronemail_day),
], debug=True)
