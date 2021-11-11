from bs4 import BeautifulSoup as bs
from re import search
from requests import Session
from typing import Union
from .poi import PoiInfo
from .utils import Texto

class Hent(Session):

    def __init__(self, url: Union[str], proxy: Union[dict]={}) -> None:
        """
        :url: String
        :proxy: Dict
        :e.g:
        from nekopoi import Hent
        hentai = Hent("https://nekopoi.care/torokase-orgasm-the-animation-episode-1-subtitle-indonesia/").getto
        hentai.to_json
        """
        super().__init__()
        if proxy:
            self.proxies = proxy
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
                    poi.stream = {}
                    poi.stream["url"] = res.group().split("\"")[-1]
                    poi.stream["headers"] = self.headers
            poi.download = {}
            for x in parse.select("div[class=\"liner\"]"):
                poi.download[self.text.reso(x.div.text)] = {}
                for y in x.select("a"):
                    poi.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
            return poi
        except Exception as e:
            print(e)
            return Exception("Maybe url invalid")

class Jav(Session):

    def __init__(self, url: Union[str], proxy: Union[dict]={}) -> None:
        """
        :url: String
        :Proxy: Dict
        :e.g:
        from nekopoi import Jav
        jav = Jav("https://nekopoi.care/ipx-700-jav-miu-shiramine-a-super-luxury-mens-beauty-treatment-salon-that-makes-beautiful-legs-glamorous-testicles/").getto
        jav.to_json
        """
        super().__init__()
        if proxy:
            self.proxies = proxy
        self.url = url
        self.text = Texto()

    @property
    def getto(self) -> PoiInfo:
        try:
            parse = bs(self.get(self.url).text, "html.parser")
            jav = PoiInfo()
            info = parse.find("div", {"class": "contentpost"})
            oppai = info.select("p")
            jav.title = text.tsplit(info.img.get("title"))
            jav.thumbnail = info.img.get("srcset").split()[-2]
            jav.movie_id = oppai[0 if len(oppai) == 6 else 1].text.split(":")[1].strip()
            jav.producers = oppai[1 if len(oppai) == 6 else 2].text.split(":")[1].strip()
            jav.artist = oppai[2 if len(oppai) == 6 else 3].text.split(":")[1].strip()
            genres = oppai[3].text.split(":")[1].strip().split(",") if len(oppai) == 6 else oppai[3].text.split(":")[1].strip(".").split(",")
            jav.genre = [g.strip() for g in genres]
            jav.duration = oppai[4 if len(oppai) == 6 else 5].text.split(":")[1].strip()
            if (vidbin := search("https://videobin.co/.+?.html", parse.prettify())):
                if (res := search("https://.+?/.+?.mp4", self.get(vidbin.group()).text)):
                    jav.stream = {}
                    jav.stream["url"] = res.group().split("\"")[-1]
                    jav.stream["headers"] = self.headers
            jav.download = {}
            for x in parse.select("div[class=\"liner\"]"):
                jav.download[self.text.reso(x.div.text)] = {}
                for y in x.select("a"):
                    jav.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
            return jav
        except Exception as e:
            print(e)
            return Exception("Maybe url invalid")
