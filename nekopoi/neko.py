from bs4 import BeautifulSoup as bs
from re import search
from typing import Union
from .poi import PoiInfo
from .utils import Req, Texto

class Hent(Req):

    def __init__(self, url: Union[str]) -> None:
        """
        :url: String
        :e.g:
        from nekopoi import Hent
        hentai = Hent("https://nekopoi.care/torokase-orgasm-the-animation-episode-1-subtitle-indonesia/").getto
        hentai.to_json
        """
        super().__init__()
        self.url = url
        self.text = Texto()

    @property
    def getto(self) -> PoiInfo:
        try:
            parse = bs(self.get(self.url).text, "html.parser")
            poi = PoiInfo()
            info = parse.find("div", {"class": "contentpost"})
            oppai = info.select("p[class=\"separator\"]")
            poi.title = self.text.tsplit(info.img.get("title"))
            poi.thumbnail = info.img.get("srcset").split()[-2]
            poi.synopsis = oppai[0].b.next.next.next.text.strip()
            poi.genre = [g.strip() for g in oppai[1].b.next_sibling.split(",")]
            poi.producers = oppai[3].b.next_sibling.lstrip(": ")
            poi.duration = oppai[4].b.next_sibling
            if (vidbin := search("https://videobin.co/.+?.html", parse.prettify())):
                if (res := search("https://.+?/.+?.mp4", self.get(vidbin.group()).text)):
                    poi.stream = res.group().split("\"")[-1]
            poi.download = {}
            for x in parse.select("div[class=\"liner\"]"):
                poi.download[self.text.reso(x.div.text)] = {}
                for y in x.select("a"):
                    poi.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
            return poi
        except Exception as e:
            print(e)
            return Exception("Maybe url invalid")

class Jav(Req):

    def __init__(self, url: Union[str]) -> None:
        """
        :url: String
        :e.g:
        from nekopoi import Jav
        jav = Jav("https://nekopoi.care/ipx-700-jav-miu-shiramine-a-super-luxury-mens-beauty-treatment-salon-that-makes-beautiful-legs-glamorous-testicles/").getto
        jav.to_json
        """
        super().__init__()
        self.url = url
        self.text = Texto()

    @property
    def getto(self) -> PoiInfo:
        try:
            parse = bs(self.get(self.url).text, "html.parser")
            jav = PoiInfo()
            info = parse.find("div", {"class": "contentpost"})
            jav.title = info.img.get("title")
            jav.thumbnail = info.img.get("srcset").split()[-2]
            jav.movie_id = info.select("p")[1].text.split(":")[1].strip()
            jav.producers = info.select("p")[2].text.split(":")[1].strip()
            jav.artist = info.select("p")[3].text.split(":")[1].strip()
            jav.genre = [g.strip() for g in info.select("p")[4].b.next_sibling.split(",")]
            jav.duration = info.select("p")[5].b.next_sibling
            if (vidbin := search("https://videobin.co/.+?.html", parse.prettify())):
                if (res := search("https://.+?/.+?.mp4", self.get(vidbin.group()).text)):
                    jav.stream = res.group().split("\"")[-1]
            jav.download = {}
            for x in parse.select("div[class=\"liner\"]"):
                jav.download[self.text.reso(x.div.text)] = {}
                for y in x.select("a"):
                    jav.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
            return jav
        except Exception as e:
            print(e)
            return Exception("Maybe url invalid")
