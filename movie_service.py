import requests
from bs4 import BeautifulSoup


class MovieService:
    def __init__(self, movie_name):
        self.movie_name = movie_name

    def get_full_movie_info(self):
        soup = self._get_imdb_movie_soup()
        movie_info = {
            'rating': self.get_movie_rating(soup),
            'year': self.get_movie_year(soup),
            'duration': self.get_movie_duration(soup),
            'director': self.get_movie_director(soup),
        }
        return movie_info

    def get_movie_rating(self, soup):
        try:
            rating = soup.find(
                'span',
                class_='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV'
            ).text
            return rating.replace('.', ',')
        except AttributeError:
            print('a error')

    def get_movie_year(self, soup):
        try:
            int_data = self._get_int_data(soup)
            year = int_data.findAll('li')[0].span.text
            return year
        except AttributeError:
            print('a error')

    def get_movie_duration(self, soup):
        try:
            int_data = self._get_int_data(soup)
            duration = int_data.findAll('li')[2].text
            return duration
        except AttributeError:
            print('a error')
        except IndexError:
            print('i error')

    def get_movie_director(self, soup):
        try:
            director = soup.find(
                'a',
                class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link'
            ).text
            return director
        except AttributeError:
            print('a error')

    def _get_google_soup(self):
        url = f'https://www.google.com/search?q=imdb+{self.movie_name}'
        page = requests.get(url)
        return BeautifulSoup(page.text, "html.parser")

    def _get_imdb_movie_soup(self):
        try:
            movie_url = self._get_first_link()
            movie_page = requests.get(movie_url.split("=")[1])
            return BeautifulSoup(movie_page.text, "html.parser")
        except requests.exceptions.MissingSchema:
            print('missing schema')

    def _get_first_link(self):
        soup = self._get_google_soup()
        links = soup.findAll("a")
        res = []

        for link in links:
            if link.find('h3') is not None:
                res.append(link.get('href').split('&')[0])

        movie_url = res[0]
        return movie_url

    def _get_int_data(self, soup):
        int_data = soup.find(
            'ul',
            class_='ipc-inline-list ipc-inline-list--show-dividers TitleBlockMetaData__MetaDataList-sc-12ein40-0 dxizHm baseAlt'
        )
        return int_data
