from requests import Session
from typing import Union

class Req(Session):

    def __init__(self) -> None:
        super().__init__()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate'}

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
        return text.split("Indonesia")[1].strip(" [").strip("]")
