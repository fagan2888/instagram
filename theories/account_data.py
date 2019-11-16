#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
from time import sleep
import pandas as pd
import csv
from infos import verified_unfollow_log
from datetime import datetime


class Insta_Info_Scraper:

    def getinfo(self, url):
        # specify 
        html = urllib.request.urlopen(url, context=self.ctx).read()
        # make soup
        soup = BeautifulSoup(html, 'html.parser')
        # identify interest 
        data = soup.find_all('meta', attrs={'property': 'og:description'})
        
        # tag & bag data 
        text = data[0].get('content').split()
        
        # user name as account calls itself
        user = '%s %s' % (text[-3], text[-2])
        
        # number of followers
        followers = text[0]
        # scan for number abbreviatiions
        if 'k' in followers or 'm' in followers:
            # keep exactly how is, for study
            followers = followers
        # if there are no indicators 
        else:
            # report with an int
            followers = int(followers.replace(',',''))
        
        # number of accounts followed
        following = text[2]
        # scan for number abbreviatiions
        if 'k' in followers or 'm' in following:
            # keep exactly how is, for sutdy
            following = following
        # if there are no inficators
        else:
            # report with an int
            following = int(following.replace(',',''))
        
        # number of posts
        posts = int(text[4].replace(',',''))

        # output user/username with #posts, #followers, and #accounts that user is following 
        return user, posts, followers, following

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        
        # load the record log
        df = verified_unfollow_log
        # determine number of iterations
        n = len(df[:int(len(df)/3)])
        # display number of iterations
        print(n)
        
        # set up nan check count
        nan_check = 0
        # set up nan break count
        nan_break = 0

        # que through n accounts in records
        for _ in range(n):
            # every 10 accounts
            if _ % 10 == 0 and _ != 0:
                # take a pause
                sleep(10)
                # reset nan check
                nan_check = 0
                # every 100 accounts
                if _ % 100 == 0:
                    # provide status update
                    print(f'{_}/{n} : {int((_/n)*100)}%')
                    # and take extra pause
                    sleep(20)
                # every 300 accounts
                if _ % 300 == 0:
                    # double the pause time
                    sleep(30)
            
            # check nan check
            if nan_check > 7:
                # too many nans
                print(f'nan check = {nan_check}\nnan break = {nan_break}\ncurrent iteration = {_}\ntaking 10 min off')
                # take significant time off
                sleep(601)
                # and reset nan check
                nan_check = 0
                # note how many times this has happened 
                nan_break += 1
                # has this happened more than 3 times?
                if nan_break > 3:
                    # woah
                    print('NAN BREAK ; STOPPING FOR AN HOUR')
                    # let's take a serious break
                    sleep(900)
                    # how long has it been
                    print('NAN BREAK ; 45 MINUTES REMAINING')
                    sleep(900)
                    # how long has it been
                    print('NAN BREAK ; 30 MINUTES REMAINING')
                    sleep(900)
                    # how long has it been
                    print('NAN BREAK ; 15 MINUTES REMAINING')
                    sleep(840)
                    # how long has it been
                    print('NAN BREAK; 60 SECONDS REMAINING')
                    sleep(60)
                    # we done, let's continue
                    print('End NAN BREAK')
                    
            # focus whichever account is up
            account = df.loc[_]
            # list out it's datapoints
            datas = [i for i in account]
            
            # will fail if 404 
            try:
                # pull metrics on that account via url
                metrics = list(self.getinfo(account.user_profile))
            # so for the potential 426 fails (on full df)
            except:
                # real metrics (probably) don't exist
                metrics = ['nan','nan','nan','nan']
                # note in nan check
                nan_check += 1 

            # note the time these metrics were recorded
            metrics.append(datetime.now()) 
            # go through each metric
            for metric in metrics:
                # add it to the account's datapoints 
                datas.append(metric)
            
            '''record the transaction
            '''  
            # open up the csv
            with open('data/made/test_account_data.csv', 'a') as file:
                # fit the writer
                writer = csv.writer(file)
                # document the transaction
                writer.writerow(datas)
            # slight break time
            sleep(2)


if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()