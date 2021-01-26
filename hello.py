#!/usr/bin/env python3

import os
import json
import templates

# print('Content-Type: application/json\r\n')
# print(json.dumps(dict(os.environ), indent=2))




print('Content-Type: text/html\r\n')
print("""
	<!doctype html>
	<html>
		<body>
			<h1>Testing html, Congrats!</h1>""")
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
print(f'<p> User\'s browser = {os.environ["HTTP_USER_AGENT"]} </p>')
try:
	cookies = os.environ["HTTP_COOKIE"].split(';')
	if cookies[0] == "":
		print(f'<p> No Cookie Found! </p>')
		print(templates.login_page())
	else:
		found = False
		p = []
		for c in cookies:
			params = c.strip().split('=')
			p.append(params)
			print(params)
			if params[0] == "sessionId" and params[1] == "CMPUT404":
				print(f'<p> Cookies Found! </p>')
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
	print(f'<p> Error found! </p>')
print("""
		</body></html>
	""")
