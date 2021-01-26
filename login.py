#!/usr/bin/env python3

import os
import json
import sys
import secret
import templates

p = []
checkLogin = [False, False]
posted_bytes = os.environ.get("CONTENT_LENGTH", 0)
if posted_bytes:
	posted = sys.stdin.read(int(posted_bytes))
	for line in posted.splitlines():
		params = line.split('&')
		for param in params:
			(name, value) = param.split('=')
			p.append(value)
			#print(name, ": ", value)
			if name == "username" and value == secret.username:
				checkLogin[0] = True
			elif name == "password" and value == secret.password:
				checkLogin[1] = True



# print('Content-Type: application/json\r\n')
# print(json.dumps(dict(os.environ), indent=2))

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
