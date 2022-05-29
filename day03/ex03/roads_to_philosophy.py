#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup

def print_road(road):
	for line in road:
		print(line)
	print(f"{len(road)} roads from {road[0]} to philosophy !")

def get_new_url(document, road):
	end = None
	for p in document.find_all('p'):
		for a in p.find_all('a'):
			if a.parent.name == 'p':
				if a.get('href') is not None and a['href'].startswith('/wiki/') \
						and not a['href'].startswith('/wiki/Wikipedia:') and not a['href'].startswith('/wiki/Help:')\
						and '.' not in a['href'] and ':' not in a['href']:
					end = a['href'].replace('/wiki/', '')
					if end.replace('_', ' ') in road:
						print("It leads to an infinite loop !")
						sys.exit()
					else:
						return f"https://en.wikipedia.org/wiki/{end}"
	if end is None:
		print("It leads to a dead end !")
		sys.exit()
	return f"https://en.wikipedia.org/wiki/{end}"

def main():
	if len(sys.argv) != 2:
		print("error: bad arguments")
		sys.exit()
	url = f"https://en.wikipedia.org/wiki/{sys.argv[1]}"
	philosophy = "Philosophy"
	road = []
	while True:
		try:
			r = requests.get(url)
			if not r.ok:
				print("It's a dead end !")
				sys.exit()
			document = BeautifulSoup(r.text, 'html.parser')
			title = document.find(id='firstHeading').text
			road.append(title)
			if title == philosophy:
				print_road(road)
				break
			else:
				url = get_new_url(document.find(id='mw-content-text'), road)
				if not url:
					raise Exception
		except ConnectionError as e:
			print(e)
			sys.exit()
		except Exception as e:
			print(e)
			sys.exit()

if __name__ == '__main__':
	main()
