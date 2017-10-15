# coding: utf8
# scrapping tripadvisor ver. 2
import requests
import csv
from bs4 import BeautifulSoup


class Page:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'
        }

    def __init__(self, name=None, link=None, list_count=0):
        self.name = name
        self.link = link
        self.list_count = list_count
        self.urls = [self.link.replace('-Reviews-', '-Reviews-'+'or'+str(i*10)+'-') for i in range(1, self.list_count)]
        self.urls.append(self.link)

        self.csv_file = open(self.name + '.csv', 'wb')
        self.writer = csv.writer(self.csv_file, delimiter=',')

    # only for test purposes
    @property
    def get_link(self): return self.link

    # only for test purposes
    @property
    def get_list_count(self): return self.list_count

    # only for test purposes
    @property
    def get_other_urls(self): return self.urls

    def get_full_page(self, link):
        self.r = requests.get(link, headers=Page.headers)
        return self.r.text.encode('utf8')

    def get_soup(self, file): return BeautifulSoup(file, 'html.parser')

    def run(self):

        for c, link in enumerate(self.urls):
            print 'Script is scrapping {count} page of {total} from {name}'.format(count=c+1, total=self.list_count, name=self.name)
            # self.row = []
            self.file = self.get_full_page(link)
            self.soup = self.get_soup(self.file)
            self.text = self.soup.find_all('div', class_='review')
            for block in self.text:
                self.row = []
                self.row.append(self.get_date(block).encode('utf8'))
                self.row.append(self.get_name(block).encode('utf8'))
                if self.get_age(block) is not None:
                    self.row.append(self.get_age(block).encode('utf8'))
                else:
                    self.row.append('Возраст не указан')
                self.row.append(self.get_rate(block))
                self.row.append(self.get_title(block).encode('utf8'))
                self.row.append(self.get_text(block).encode('utf8'))

                self.writer.writerow(self.row)

        self.end_parse()

    def get_date(self, block):
        self.date = block.find_all('span', class_='date')
        for d in self.date:
            return d.text

    def get_name(self, block):
        self.username = block.find_all('a', class_='author')
        for u in self.username:
            return u.text

    def get_title(self, block):
        self.title = block.find_all('div', class_='title')
        for t in self.title:
            return t.text.strip()

    def get_rate(self, block):
        self.rating = block.find_all('div', class_='ui_bubble_rating')
        for r in self.rating:
            if 'bubble_40' in r.get('class'):
                return 4
            elif 'bubble_50' in r.get('class'):
                return 5
            elif 'bubble_30' in r.get('class'):
                return 3
            elif 'bubble_20' in r.get('class'):
                return 2
            elif 'bubble_10' in r.get('class'):
                return 1

    def get_text(self, block):
        self.descr = block.find_all('div', class_='body')
        for d in self.descr:
            return d.text

    def get_age(self, block):
        self.usr_url = 'https://www.tripadvisor.ru{}'.format(block.find('a', class_='user-details').get('href'))
        self.usr_file = self.get_full_page(self.usr_url)
        self.usr_soup = self.get_soup(self.usr_file)
        self.user_age = self.usr_soup.find_all('div', class_='subtext')
        for age in self.user_age:
            if u'возраст' in age.text:
                return age.text.strip()

    def end_parse(self):
        print 'Scrapping done for {name}, results in {filename} \n'.format(name=self.name, filename=(self.name + '.csv'))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    file = parser.parse_args()
    with open(file.source) as f:
        params = csv.reader(f, delimiter=',')
        for row in params:
            engine = Page(name=str(row[0]), link=str(row[1]), list_count=int(row[2]))
            engine.run()
