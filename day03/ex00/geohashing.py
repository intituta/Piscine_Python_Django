#!/usr/bin/python3

import sys
import antigravity

def main():
	if (len(sys.argv) == 4):
		try:
			antigravity.geohash(float(sys.argv[1]), float(sys.argv[2]), sys.argv[3].encode('utf-8'))
		except:
				return print("bad arguments")
	else:
		print("bad arguments")

if __name__ == '__main__':
	main()
