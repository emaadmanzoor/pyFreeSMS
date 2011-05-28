"""
	PyFreeSMS :: The 160by2 Module v1.0.0
	
	For more info: http://halfclosed.wordpress.com/
	
	Copyright (C) 2011  Emaad Ahmed Manzoor
	
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.
"""

import urllib2
import urllib
import socket
import re

socket.setdefaulttimeout(10)

headers = {'User-Agent': 'iPhone 4.0',
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Connection':'Keep-Alive',
			'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8',
			'Accept-Language':'en-us,en;q=0.5',
			'Accept-Encoding':'gzip,deflate',
			'Keep-Alive':'300',
			'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7'}
			
'''
	Sends a message to the number specified by 'phonenumber'.
	Uses the username/password/message specified.
'''			
def sendMessage(username, password, phonenumber, message):
	if (username=='' or password=='' or message==''):
		print "Unspecified username, phone number, password or message."
		return
	
	''' Build the login POST query '''
	params = urllib.urlencode( { 'l': '1', 
							'txt_msg': '', 
							'mno':'', 
							'txtUserName': username,
							'txtPasswd': password, 
							'RememberMe': 'Yes', 
							'cmdSubmit': 'Login' } )
						
	request = urllib2.Request('http://m.160by2.com/LoginCheck.asp', params, headers)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	opener.addheaders = [('User-Agent', 'iPhone 4.0')]
	urllib2.install_opener(opener)
	
	''' DEBUG '''
	urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
	
	''' LOGIN '''
	print "Logging in to 160by2 as " + username
	try:
		data = opener.open(request).read()
		if (re.search("""<font size="1" style="color:Red;">Invalid password</font>""", data) != None):
			print "Invalid password."
			return
		if (re.search("""<font size="1" style="color:Red;">Invalid username</font>""", data) != None):
			print "Invalid username."
			return
	except urllib2.HTTPError, e:
		print "Login failed. HTTP Error: " + str(e.code)
		return
	except urllib2.URLError, e:
		print "Login failed. URL Error: " + str(e.reason)
		return
	
	''' Get the message ID '''
	print "Login successful. Getting MID..."
	pattern="mymenu.asp\?l=2&Msg=([a-zA-Z0-9]+)"
	matches = re.search(pattern, data)

	try:
		mid = matches.group(1).strip()
	except AttributeError:
		try:
			pattern = "index.asp\?ErrMsg=([a-zA-Z0-9]+)"
			matches = re.search(pattern, data)
			error = matches.group(1).strip()
			print "Error getting MID: " + error
			return
		except AttributeError:
			print "Unknown error getting MID."
			return
	
	''' Build send message POST query '''
	print "MID successfully retreived. Sending message..."
	params = urllib.urlencode( { 'l': '1', 
							'txt_mobileno': phonenumber, 
							'txt_msg': message, 
							'cmdSend': 'Send+SMS',
							'TID': '', 
							'T_MsgId': '', 
							'Msg': mid } )
						
	request = urllib2.Request('http://m.160by2.com/SaveCompose.asp', params, headers)
	try:
		data = opener.open(request).read()
	except urllib2.HTTPError, e:
		print "Login failed. HTTP Error: " + str(e.code)
		return
	except urllib2.URLError, e:
		print "Login failed. URL Error: " + str(e.reason)
		return

	success = re.search("Successfully", data)
	if success != None:
		print "SMS Sent Successfully."
	else:
		print "SMS Unsuccessful"
