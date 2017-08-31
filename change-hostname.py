#!/usr/bin/python

# Author: James S
# Version: 1.1

import os, subprocess, sys
from time import sleep

# Colour set up
PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'	

try: # This is so exit message is displayed on KeyboardInterrupt

	def main(): 
		os.system("clear")

		# Main Menu
		while True:
			print ("\n\t\t%s%s%sHOSTNAME CHANGER%s") % (BLUE, BOLD, UNDERLINE, END)
			print ("\n%s%sMade by: %sJames S%s") % (RED, BOLD, BLUE, END)

			# Checks whether the user is root
			is_root = subprocess.check_output(["whoami"], shell=True).rstrip("\n")
			if (is_root != "root"):
				print ("\n%sError: %sPlease run with root privilages. Try with sudo:%s") % (RED, BLUE, END)
				print ("\t%s%s$ sudo python change-hostname.py%s\n")% (GREEN, BOLD, END)
				sys.exit()

			while True:
				print ("\n\nDo you want to:\n")
				print ("\t%s[%s1%s]%s View Hostname") % (CYAN, RED, CYAN, END)
				print ("\t%s[%s2%s]%s Change Hostname") % (CYAN, RED, CYAN, END)
				print ("\t%s[%s3%s]%s Exit") % (CYAN, RED, CYAN, END)
				menu = raw_input(BOLD + "> "+ END)
				# User chooses an option
				if menu == "1":
					check()
				elif menu == "2":
					change()
					break
				elif menu == "3":
					print ("\n%s%sExiting...%s\n") % (BOLD, RED, END)
					sleep(0.5)
					sys.exit()
				else:
					print "\n\n%s%sPlease select a valid option.\n%s" % (BOLD, GREEN, END)


	def check():
		hostname = subprocess.check_output(["cat /etc/hostname"], shell=True) # Reads host file
		print ("\n\nYour current hostname is: %s%s" + hostname + "%s") % (BOLD, GREEN, END) 
		sleep(1)

	def change():
		# User enters a new hostname
		new_hostname = raw_input(BLUE + "\nEnter a new hostname: " + END) 
		f = open("/etc/hostname", "w") # Program opens host file 1
		f.write(new_hostname) # Program writes new hostname to this file
		f.write("\n")
		f.close
		
		# Makes a copy of host file 2
		line1 = subprocess.check_output(["awk 'FNR==1 {print}' /etc/hosts"], shell=True).rstrip("\n")
		# This line only goes up to the 2nd field as the 3rd is the old hostname
		line2 = subprocess.check_output(["awk 'FNR==2 {print $1,$2}' /etc/hosts"], shell=True).rstrip("\n")
		line3 = subprocess.check_output(["awk 'FNR==3 {print}' /etc/hosts"], shell=True).rstrip("\n")
		line4 = subprocess.check_output(["awk 'FNR==4 {print}' /etc/hosts"], shell=True).rstrip("\n")
		line5 = subprocess.check_output(["awk 'FNR==5 {print}' /etc/hosts"], shell=True).rstrip("\n")
		line6 = subprocess.check_output(["awk 'FNR==6 {print}' /etc/hosts"], shell=True).rstrip("\n")
		line7 = subprocess.check_output(["awk 'FNR==7 {print}' /etc/hosts"], shell=True).rstrip("\n")

		newline2 = line2 + " " + new_hostname #This is re-making line 2 by adding the new hostname into the old hostnames position
		f = open("/etc/hosts", "w") # Program opens host file 2
		f.write(line1) # Program re-writes the file but with edited line 2
		f.write("\n")
		f.write(newline2)
		f.write("\n")
		f.write(line3)
		f.write("\n")
		f.write(line4)
		f.write("\n")
		f.write(line5)
		f.write("\n")
		f.write(line6)
		f.write("\n")
		f.write(line7)
		f.write("\n")
		f.close()

		check_hostname1 = subprocess.check_output(["cat /etc/hostname"], shell=True) # Checks to see if hostname has been changed
		check_hostname2 = subprocess.check_output(["awk 'FNR==2{print $3}' /etc/hosts"], shell=True) 
		sleep(1)
		
		# Tells user if the hostname has been changed
		if new_hostname.rstrip("\n") == check_hostname1.rstrip("\n") and new_hostname.rstrip("\n") == check_hostname2.rstrip("\n"):
			print ("\n%s%sYour host name has been changed successfully :)%s\n") % (GREEN, BOLD, END)
			print ("%sDo you want to restart your network-manager to fully change your hostname?%s%s (recommended)%s (Y/n)%s") % (RED,BOLD, YELLOW, BLUE, END)
			while True:
				network_reset = raw_input (BOLD + "> " + END)
				# Restarts network-manager so changes appear on network
				if network_reset == "Y" or network_reset == "y" or network_reset == "":
					print ("\n%s%sRestarting network-manager...%s") % (BOLD, PURPLE, END)
					os.system("service network-manager restart")
					sleep(2)
					print ("\n%s%sDONE!%s") % (GREEN, BOLD, END)
					sleep(2)
					os.system("clear")
					break
				elif network_reset == "n" or network_reset == "N":
					sleep(1)
					print ("\n%sYou will need to manually do this for the change to be visible.") % (RED)
					print ("%s%sTry disconnecting and reconnecting to the access point%s") % (BOLD, GREEN, END)
					sleep(3)
					break
				else:
					print "\n%s%sPlease select a valid option.\n%s" % (BOLD, GREEN, END)
		else:
			print ("\n%s%sError: %sUnable to change hostname. Try again%s") % (RED, BOLD, BLUE, END)
		
	main()
except KeyboardInterrupt: # Exit message if KeyboardInterrupt
	print ("\n\n%s%sExiting...%s\n") % (BOLD, RED, END)
	sleep(0.5)
