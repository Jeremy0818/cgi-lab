#!/usr/bin/env python3

import os
import json
import templates
import sys
import secret

#  Use json to inspect all environment variables
# print('Content-Type: application/json\r\n')
# print(json.dumps(dict(os.environ), indent=2))

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
	# print("""
	# 		</body></html>
	# 	""")
else:

	#  Create HTTP response and report QUERY_STIRNG, HTTP_USER_AGENT, AND HTTP_COKIE if exists
	print('Content-Type: text/html\r\n')
	print("""
		<!doctype html>
		<html>
			<body>
				<h1>Hello There!</h1>""")
	#  report query string
	try:
		print(f'<p> QUERY_STRING </p>')
		print("<ul>")
		for parameter in os.environ["QUERY_STRING"].split('&'):
			(name, value) = parameter.split('=')
			print(f'<li>{name} = {value}</li>')
		print("</ul>")
	except:
		print("</ul>")
		print(f'<p> No Query Found! </p>')
	#  report user's browser
	try:
		print(f'<p> User\'s browser = {os.environ["HTTP_USER_AGENT"]} </p>')
	except:
		print(f'<p> No User Agent Found! </p>')
#  report HTTP cookies
try:
	cookies = os.environ["HTTP_COOKIE"].split(';')
	if cookies[0] == "":
		print(f'<p> No Cookie Found! </p>')
		print(templates.login_page())
	else:
		#  There is cookies, check if there is the cookie the server is looking for
		found = False
		p = []
		for c in cookies:
			print(f'Got some cookies, let\'s see...')
			params = c.strip().split('=')
			p.append(params)
			print(f'<p> {params} </p>')
			if params[0] == "sessionId" and params[1] == "CMPUT404":
				print(f'<p> Key Cookies Found! </p>')
				found = True
			elif params[0] == "username":
				username = params[1]
			elif params[0] == "password":
				password = params[1]
		if found:
			print(templates.secret_page(username, password))
		else:
			print(f'<p> Wrong Cookies Found! </p>')
			print(templates.login_page())
except BaseException as e:
	print(str(e))
	print(f'<p> Unable to access Cookies </p>')
print("""
		</body></html>
	""")
