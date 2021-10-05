from cloudscraper import create_scraper
from typing import Union

class Req:

    def __init__(self) -> None:
        scraper = create_scraper(delay=10)
        self.get = scraper.get

class Texto:

    def __init__(self) -> None:
        pass

    def tsplit(self, text: Union[str]) -> str:
        """
        Get title hentai and delete blablabla
        :text: String
        """
        for i in ["[3D]","[NEW Release]","[Uncensored]"]:
            if i in text:
                text = text.split(i)[1].strip()
        return text.split("Episode")[0].strip()

    def reso(self, text: Union[str]) -> str:
        """
        Get resoluion only
        :text: String
        """
        return text.split("Indonesia")[1].strip(" [").strip("]") if "Indonesia" in text else text.split()[-1].strip("[").strip("]")
