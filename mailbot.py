import urllib2 as ul2
import urllib
import cookielib
import json
import datetime
import re

class Mailbot:

	base_url = 'FULL URL FOR BASE POMMO FOLDER'
	login_url = base_url + '/index.php'
	status_url = base_url + '/ajax/status_poll.php'
	restart_url = base_url + '/ajax/status_cmd.php?cmd=restart'

	username = 'A POMMO ADMIN USERNAME'
	password = 'PASSWORD'

	# the number of minutes since the last update
	# to trigger a restart of the MTA
	threshold = 3

	cookies = cookielib.LWPCookieJar()
	opener = False
	content = ""
	status = False

	def __init__(self):
		# attempt to login
		values = {'username' : self.username,
							'password' : self.password,
							'referer'  : '/newsletter/admin.php',
							'submit'   : 'Log In' }
		data = urllib.urlencode(values)

		handlers = [
			ul2.HTTPHandler(),
			ul2.HTTPSHandler(),
			ul2.HTTPCookieProcessor(self.cookies)
			]
		self.opener = ul2.build_opener(*handlers)

		req = ul2.Request(self.login_url, data)
		response = self.opener.open(req)
		self.content = response.read()

	def get_status(self):
		req = ul2.Request(self.status_url)
		response = self.opener.open(req)
		self.content = response.read()
		self.status = json.loads(self.content)

		if self.status['status'] != 1:
			""" 
			1 => Pommo::_T('Processing'),
			2 => Pommo::_T('Stopped'),
			3 => Pommo::_T('Frozen'),
			4 => Pommo::_T('Finished')
			"""
			return 0

		i = -1
		err = True
		while err:
			# find the last timestamp in the logging mechanism
			last_notice = self.status['notices'][i]
			logtime = last_notice.split(' ')[0]

			try:
				last_notice_time = datetime.datetime.strptime(logtime, '%H:%M:%S')
			except:
				i -= 1
			else:
				current_time = datetime.datetime.now().replace(year = 1900, month = 1, day = 1)
				# too long since last update?
				if (current_time - last_notice_time) > datetime.timedelta(minutes = self.threshold):
					return str(current_time - last_notice_time)
				err = False

		return 0

	def restart(self):
		req = ul2.Request(self.restart_url)
		response = self.opener.open(req)
		self.content = response.read()

if __name__ == '__main__':
	m = Mailbot()
	timediff = m.get_status()
	if timediff != 0:
		print "Last status %s ago; restarting mailer" % (timediff)
		m.restart()

