#!/usr/bin/python3

from local_lib.path import Path

def main():
	try:
		Path.mkdir_p(Path('Dir'))
		with Path.open(Path('Dir/file.txt'),'w') as file:
			file.write('Hello World')
		with Path.open("Dir/file.txt", "r") as file:
			print (file.read())
	except:
		return print("bad file")

if __name__ == '__main__':
	main()
