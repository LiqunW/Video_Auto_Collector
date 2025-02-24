import sys
import time

import qbittorrentapi
import json
import os


class SetRule:
    def __init__(self, config):
        with open("../config/bangumi.json") as f:
            self.bangumi_info = json.load(f)
        self.rss_link = config["rss_link"]
        self.host_ip = config["host_ip"]
        self.user_name = config["user_name"]
        self.password = config["password"]
        self.download_path = config["download_path"]
        self.qb = qbittorrentapi.Client(host=self.host_ip, username=self.user_name, password=self.password)
        try:
            self.qb.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)

    def set_rule(self, bangumi_name, season):
        rule = {
            'enable': True,
            'mustContain': bangumi_name,
            'mustNotContain': '720',
            'useRegx': True,
            'episodeFilter': '',
            'smartFilter': False,
            'previouslyMatchedEpisodes': [],
            'affectedFeeds': [self.rss_link],
            'ignoreDays': 0,
            'lastMatch': '',
            'addPaused': False,
            'assignedCategory': 'Bangumi',
            'savePath': str(os.path.join(self.download_path, bangumi_name, season))
            }
        self.qb.rss_set_rule(rule_name=bangumi_name, rule_def=rule)

    def add_rss_feed(self):
        try:
            self.qb.rss_add_feed(self.rss_link)
            sys.stdout.write(f"[{time.strftime('%Y-%m-%d %X')}]  Successes adding RSS Feed." + "\n")
        except ConnectionError:
            sys.stdout.write(f"[{time.strftime('%Y-%m-%d %X')}]  Error with adding RSS Feed." + "\n")

    def run(self):
        sys.stdout.write(f"[{time.strftime('%Y-%m-%d %X')}]  Start adding rules." + "\n")
        sys.stdout.flush()
        for info in self.bangumi_info:
            self.set_rule(info["title"], info["season"])
        sys.stdout.write(f"[{time.strftime('%Y-%m-%d %X')}]  Finished." + "\n")
        sys.stdout.flush()

