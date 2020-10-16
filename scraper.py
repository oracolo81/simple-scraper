#!/usr/bin/python

from urllib.request import Request, urlopen
import urllib.error
from bs4 import BeautifulSoup
import csv
import re

# specify url
url = 'https://www.onlinecasinosonline.co.za'
data = []


def getHtml(pageUrl):
    global url
    html = ''
    req = Request(url + pageUrl, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        response = urlopen(req, timeout=20)
    except urllib.error.HTTPError as e:
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
        print('URLError: {}'.format(e.reason))
    else:
        html = response.read()

    return html


def getTracker(pageUrl):
    html = getHtml(pageUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    anchor = bsObj.find('a')
    if anchor:
        return anchor.attrs['href']


def getLink(pageUrl):
    req = Request(pageUrl, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urlopen(req, timeout=20)
    except urllib.error.HTTPError as e:
        print('HTTPError: {}'.format(e.code))
    except urllib.error.URLError as e:
        print('URLError: {}'.format(e.reason))
    else:
        html = response.read()
        bsObj = BeautifulSoup(html, "html.parser")
        table = bsObj.find('table', class_='review_casino')

        rows = table.find_all('tr')

        for row in rows:
            anchor = row.find('a')
            if anchor:
                cta = anchor.attrs['href']
                name = re.sub('\.html$', '', cta).replace('/goto/', '')
                print(name)
                review = re.sub('\.html$', '', pageUrl)
                tracker = getTracker(cta)
                data.append([name, review, cta, tracker])


def getLinks(pageUrl):
    global data
    html = getHtml(pageUrl)
    name = ''
    review = ''
    cta = ''
    tracker = ''

    bsObj = BeautifulSoup(html, 'html.parser')
    table = bsObj.find('table', id='cb1')
    rows = table.find_all('tr')

    for row in rows:
        col5 = row.find('td', class_='col5')
        col6 = row.find('td', class_='col6')
        if col5:
            anchor = col5.find('a')
            newPage = anchor.attrs['href']
            if 'review.html' in newPage:
                name = re.sub('\-review.html$', '', newPage).replace('/', '')
                review = re.sub('\.html$', '', newPage)
                print(name)
        if col6:
            anchor = col6.find('a')
            cta = anchor.attrs['href']
            tracker = getTracker(cta)
        if review:
            data.append([name, review, cta, tracker])


# populate pages array from the full list of casinos
# getLinks("/online-casino-directory.html")

# get tracker from the review page
with open('casino-reviews.csv', mode='r') as csvfile:
    reviews = csv.reader(csvfile, delimiter=',', quotechar='"')
    line_count = 0
    for row in reviews:
        if line_count == 0:
            line_count += 1
        else:
            getLink(row[0])
            line_count += 1

with open('operators.csv', mode='w') as file:
    operators = csv.writer(file, delimiter=',', quotechar='"')
    for line in data:
        operators.writerow([line[0], line[1], line[2], line[3]])
