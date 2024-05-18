from bs4 import BeautifulSoup
import requests
from requests.models import Response


INVALID_CHARACTERS = "'/.!"


class AZLyrics():
    """
    Scrape song's lyrics from:

        https://www.azlyrics.com

    """
    def __init__(self, artist: str, song: str):
        self._artist = artist
        self._song = song

    def _parse_artist(self) -> str:
        """
        url' syntax requires artist name to be:
            - no spaces
            - all lower case
        """
        return self._artist.lower().replace(" ", "")

    def _parse_song(self) -> str:
        """
        url' syntax requires song name to be:
            - no spaces
            - all lower case
            - without invalid characters
        """
        out = self._song.lower().replace(" ", "")
        for c in INVALID_CHARACTERS:
            out = out.replace(c, "")
        return out

    def scrape(self) -> str:
        """
        Retrives url's content
        """
        response = requests.get(self.url())

        lyrics = None

        if response.ok:
            lyrics = self._scrape_lyrics(response)

        return lyrics

    def url(self) -> str:
        url_syntax = "https://www.azlyrics.com/lyrics/{}/{}.html"
        return url_syntax.format(self._parse_artist(), self._parse_song())

    def _scrape_lyrics(self, r: Response) -> str:
        """
        Lyrics are always found in the DOM's body, more
        precisely there is a div belonging to the class
        col-xs-12 col-lg-8 text-center which contains
        several divs, among them the target is found

        euristics: even if there are some other <div>
        containig <br>, the target has by far the largest
        number of <br>
        """
        dom = BeautifulSoup(r.text, "html.parser")
        body = dom.body
        divs = body.find_all(
                "div", {"class": "col-xs-12 col-lg-8 text-center"}
        )[0]

        target = {0: 0}

        for i, d in enumerate(divs):
            try:
                query = d.find_all("br")
                n_br = len(query)
                if n_br > list(target.values())[0]:
                    target = {i: n_br}
            except:
                pass

        target = list(target.keys())[0]
        lyrics = list(divs.children)[target].text

        return lyrics