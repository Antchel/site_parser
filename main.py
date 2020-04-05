import requests
from bs4 import BeautifulSoup
from collections import namedtuple

InnerBlock = namedtuple('Block', 'Country, Name , ICAO, Mail , Phone')

source_url = 'https://airport.airlines-inform.ru'


class Block(InnerBlock):

    def __str__(self):
        return f'{self.Country}\t{self.Name}\t{self.ICAO}\t{self.Mail}\t{self.Phone}'


class Block1(InnerBlock):

    def __str__(self):
        return f'{self.Country}\t{self.Name}\t{self.Mail}\t{self.Phone}'

    x = InnerBlock(Country='Russia', Name='Balandino', ICAO="AAA", Mail='golan94@mail.ru', Phone='+7-982-345-40-77')
    print(x)

    y = InnerBlock(Country='Russia', Name='Balandino', ICAO="AAA", Mail='golan94@mail.ru', Phone='+7-982-345-40-77')
    print(y)


class AirportParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept-Language': 'en-US', }

    def get_page(self, page: int = None):
        params = {
        }
        url = [0] * 8
        url[0] = 'https://airport.airlines-inform.ru/russia/'
        url[1] = 'https://airport.airlines-inform.ru/cis/'
        url[2] = 'https://airport.airlines-inform.ru/europe/'
        url[3] = 'https://airport.airlines-inform.ru/asia/'
        url[4] = 'https://airport.airlines-inform.ru/america/'
        url[5] = 'https://airport.airlines-inform.ru/latin_america/'
        url[6] = 'https://airport.airlines-inform.ru/australia_and_oceania/'
        url[7] = 'https://airport.airlines-inform.ru/africa/'
        if page and page > 1:
            # url = 'https://airport.airlines-inform.ru/russia/' + page.__str__() + '.html'
            url[0] = url[0] + page.__str__() + '.html'
        print(url[0])
        r = self.session.get(url[0], params=params)
        return r.text

    def getPaginationLimit(self):
        text = self.get_page()
        soup = BeautifulSoup(text, 'html.parser')
        container = soup.select('a.pageVisibleTrue')
        last_button = container[-1]
        last_page = last_button.string.strip()
        print(last_page)
        return int(last_page)

    def parse_all_pages(self):
        limit = self.getPaginationLimit()
        # limit = 7
        print(f'All pages:{limit}')
        for i in range(1, limit + 1):
            self.getBlocks(page=i)

    def getBlocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = BeautifulSoup(text, 'html.parser')
        container = soup.select('a.airlines')
        for item in container:
            block = self.parse_block(item=item)
            print(block)

    def get_page_info(self, url):
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        mailBlock = soup.find(text='E-mail:')
        cityBlock = soup.find(text='Код ИКАО:')
        info = soup.select('p strong')
        phones = soup.find('span', itemprop='telephone')

        if phones:
            phone = phones.next
        else:
            phone = "None"

        if info[0].next:
            airportName = info[0].next
        else:
            airportName = 'None'

        if mailBlock:
            email = mailBlock.next
        else:
            email = 'None'

        if info[2].next:
            country = info[2].next
        else:
            country = 'None'

        if cityBlock:
            icaoCode = cityBlock.next
        else:
            icaoCode = 'None'

        return Block(
            Country=country,
            Name=airportName,
            ICAO=icaoCode,
            Mail=email,
            Phone=phone
        )

    # @staticmethod
    def parse_block(self, item):
        href = item.get('href')
        if href:
            url = source_url + href
        else:
            url = None
        text = self.get_page_info(url)
        return text


def main():
    p = AirportParser()
    p.parse_all_pages()


# p.getBlocks()


if __name__ == '__main__':
    main()
