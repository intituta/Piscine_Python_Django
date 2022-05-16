#!/usr/bin/python3
def numbers():
	with open("numbers.txt", "r") as file:
		numbers = file.read().split(",")
		for elem in numbers:
			print(elem.strip())
if __name__ == '__main__':
	numbers()
