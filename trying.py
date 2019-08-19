import lxml.html as lh
from lxml import etree
import time
from selenium import webdriver
from googlesearch import search
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


class AssertDirectors:
    def __init__(self, movies, sites):
        self.movies = movies
        self.sites = sites

    driver = webdriver.Chrome(r"C:\Users\ManageLocal\chromedriver_win32\chromedriver.exe")

    _wiki_directed_by_txt = "directed by"
    _imdb_directed_by_txt = "director:"
    _wiki_directed_by_sel = r"#mw-content-text > div > table.infobox.vevent > tbody > tr:nth-child(3) > th"
    _wiki_director_sel = r"#mw-content-text > div > table.infobox.vevent > tbody > tr:nth-child(3) > td > a"
    _imdb_directed_by_sel = r"#title-overview-widget > div.plot_summary_wrapper > div.plot_summary > div:nth-child(2) > h4"
    _imdb_director_sel = r"#title-overview-widget > div.plot_summary_wrapper > div.plot_summary > div:nth-child(2) > a"
    _wiki_movie_name_sel = r"#firstHeading > i"
    _imdb_movie_name_sel = r"#title-overview-widget > div.vital > div.title_block > div > div.titleBar > div.title_wrapper > h1"

    def valid_link(self, link, movie, soup):
        if "wikipedia.org" in link:
            movie_name_sel = self._wiki_movie_name_sel
        elif "imdb.com" in link:
            movie_name_sel = self._imdb_movie_name_sel
        site_movie_name = soup.select(movie_name_sel)
        if len(site_movie_name) > 0:
            site_movie_name = site_movie_name[0].get_text().lower()
            match_ratio = SequenceMatcher(None, movie.lower(), site_movie_name).ratio()
            if match_ratio > 0.65:
                return True
            else:
                return False
        else:
            return False

    def get_movie_directors(self):
        movie_directors = {}
        for movie in self.movies:
            movie_directors[movie] = {}
            time.sleep(0.5)
            for site in self.sites:
                time.sleep(0.5)
                query = f"site:{site} {movie} the movie"
                for link in search(query, tld="co.in", num=10, stop=2, pause=2):
                    time.sleep(0.5)
                    self.driver.get(link)
                    content = self.driver.page_source
                    soup = BeautifulSoup(content, 'lxml')
                    if self.valid_link(link, movie, soup):
                        movie_directors[movie][site] = [link, self.get_director(link, soup)]
                        break
                    else:
                        movie_directors[movie][site] = None
            print(f"{movie}: {movie_directors[movie]}")
        self.driver.quit()
        return movie_directors

    def get_director(self, link, soup):
        if "wikipedia.org" in link:
            directed_by_txt = self._wiki_directed_by_txt
            directed_by_sel = self._wiki_directed_by_sel
            director_sel = self._wiki_director_sel
        elif "imdb.com" in link:
            directed_by_txt = self._imdb_directed_by_txt
            directed_by_sel = self._imdb_directed_by_sel
            director_sel = self._imdb_director_sel
        if not soup.select(directed_by_sel)[0].get_text().lower() == directed_by_txt:
            print("WRONG PAGE")
            return None
        else:
            director = soup.select(director_sel)[0].get_text().lower()
            return(director)
