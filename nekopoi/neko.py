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
            poi.title = self.text.tsplit(info.img.get("title"))
            poi.thumbnail = info.img.get("srcset").split()[-2]
            poi.sinopsis = info.select("p")[1].text
            poi.genre = [g.strip() for g in info.select("p")[2].b.next_sibling.split(",")]
            poi.producers = info.select("p")[4].b.next_sibling.lstrip(": ")
            if (vidbin := search("http?s://videobin.co/(.*?).html", parse.prettify())):
                if (res := search("http?s://(.*?)/(.*?).mp4", self.get(vidbin.group()).text)):
                    poi.stream = res.group().split("\"")[-1]
            poi.download = {}
            for x in parse.select("div[class=\"liner\"]"):
                poi.download[self.text.reso(x.div.text)] = {}
                for y in x.select("a"):
                    poi.download[self.text.reso(x.div.text)].update({y.text.lower(): y.get("href")})
            return poi
        except Exception as e:
            print(e)
            return Exception("Invalid link")
