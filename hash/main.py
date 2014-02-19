import hashlib
import random
import string
import time
import sys
import os
import math
from multiprocessing import Process
#returns random string, less chars makes this program faster but too few and you can easily run through all the posible combinations
#string combinations = len(chars) ** size
def id_generator(size=8, chars=string.letters + string.digits + string.punctuation.replace("\n", "").replace("\t", "")):
	return ''.join(random.choice(chars) for x in range(size))
def check_hash(threadID, curID, curHash):
	times = 50000000 #number of hashes each core will go through
	start = time.time()#used to keep track of hashes per second
	for i in range(times):
		newID = id_generator()
		newHash = hashlib.sha512(newID).hexdigest()
		#if the new hash is lower than the current one check the new one against the one on disk
		if newHash < curHash:
			__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
			fo = open(os.path.join(__location__, 'hash.txt'), "r")
			diskID = fo.readline()
			diskHash = fo.readline()
			fo.close()
			#if the new hash is lower than the one on disk write the new one to the disk and print it to the screen else curID and curHash are replaced with their disk counterparts
			if newHash < diskHash:
				curID = newID
				curHash = newHash
				print("%i - %i:\n%s\n%s\n" % (threadID, i, newID, newHash))
				fo = open(os.path.join(__location__, 'hash.txt'), "w")
				fo.write(newID + "\n")
				fo.write(newHash)
				fo.close();
			else:
				curID = diskID
				curHash = diskHash
		#prints out how many hashes done compared to the total and also prints hashes per second
		if i % (times / 4) == 0 and i > 0 or i == 500000:
			end = time.time()
			et = end - start
			lps = i / et
			print "hashes per second for this core = %f" % (lps)
			print("%i - %i/%i...\n" % (threadID, i, times))
if __name__ == '__main__':
	#read starting id and hash from file
	__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
	fo = open(os.path.join(__location__, 'hash.txt'), "r")
	curID = fo.readline()
	curHash = fo.readline()
	fo.close()
	print("%i - %i:\n%s\n%s\n" % (0, 0, curID, curHash))
	#start up the 4 new Processes, 1 for each cpu core my computer has
	process0 = Process(target = check_hash, args = (0, curID, curHash))
	process1 = Process(target = check_hash, args = (1, curID, curHash))
	process2 = Process(target = check_hash, args = (2, curID, curHash))
	process3 = Process(target = check_hash, args = (3, curID, curHash))
	process0.start()
	process1.start()
	process2.start()
	process3.start()
	process0.join()
	process1.join()
	process2.join()
	process3.join()