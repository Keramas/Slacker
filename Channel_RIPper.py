import requests
import csv
import argparse
import sys

URL = "https://slack.com/api/channels.list"

GREEN = '\033[32m'
END = '\033[0m'


def get_args():
    parser = argparse.ArgumentParser(description="Channel RIPper",epilog="Invading your Slack channel since 2019.")
    parser.add_argument('-t','--token',type=str, help="Slack API token", required=True)
    args = parser.parse_args()
    api_token = args.token
    return api_token


def channelRIP(token):
    s = requests.get(URL + "?token=" + api_token + "&pretty=1")
    slack_channels = s.json()
    count = 0
    with open('channel_dictionary.csv', mode ='a+') as channel_dictionary:
        channel_writer = csv.writer(channel_dictionary, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        channel_writer.writerow(["ID","Name"])
        while count >= 0:
            try:
                channel_IDs = slack_channels["channels"][count]["id"]
                channel_Names = slack_channels["channels"][count]["name"]
                channel_writer.writerow([channel_IDs,channel_Names])
                count += 1
            except IndexError:
                channel_IDs = 'null'
                channel_Names = 'null'
                break


if __name__=="__main__":
    api_token = get_args()
    channelRIP(api_token)
    print GREEN + "[!] Channel dictionary saved to 'channel_dictionary.csv'" + END
    sys.exit(0)
