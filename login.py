#!/usr/bin/env python3

import os
import json
import sys
import secret
import templates

#  Get posted value from standard input before sending the HTTP response
p = []
checkLogin = [False, False]
posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
if posted_bytes:
	posted = sys.stdin.read(int(posted_bytes))
	for line in posted.splitlines():
		cookies = line.split('&')
		for cookie in cookies:
			(name, value) = cookie.split('=')
			p.append(value)
			#  Check if the client posted the correct username and password
			if name == "username" and value == secret.username:
				checkLogin[0] = True
			elif name == "password" and value == secret.password:
				checkLogin[1] = True

#  Modify the website message and HTTP response header according to the login state
msg = "Log in Unsuccessful, please try again..."
if checkLogin[0] == True and checkLogin[1] == True:
	print('Set-Cookie:sessionId=CMPUT404' + '; Max-Age=30')
	print(f'Set-Cookie:username={p[0]}; Max-Age=30')
	print(f'Set-Cookie:password={p[1]}; Max-Age=30')
	msg = "Log in Successful, Congrats!"
print('Content-Type: text/html\r\n')
print("""
	<!doctype html>
	<html>
		<body>
			<h1>""" + msg + """</h1>""")
print(f'<h2> Posted data </h2>')
print(f"<h3> POSTED: <pre>")
print("username:", p[0], "\npassword:", p[1])
print("</pre></h3>")
print("""
		</body></html>
	""")
