import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from dataclasses import dataclass
from config.settings.base import CUSTOM_LOGGER


@dataclass
class Content:
    type: str
    special: str


class MetaHandler:
    def __init__(self,url):
        self.url = url
        self.ua = UserAgent()
        self.parsed_url = None
        self.content_types = [
            Content('title', 'h1'),
            Content('description', 'p'),
            Content('image', 'img'),
        ]

    @property
    def is_url(self):
        try:
            self.parsed_url = urlparse(self.url)
            return True
        except:
            return False

    def get_content(self):
        try:
            response = requests.get(self.url,
                                    # headers={'user-agent':self.ua.random},
                                    timeout=10)
            html = BeautifulSoup(response.text,'html.parser')
            result = {}
            for content in self.content_types:
                result[content.type] = None
                if html.find('meta', property='og:'+content.type):
                    result[content.type] = html.find('meta',property='og:'+content.type).get('content')
                elif html.find('meta', property='twitter:'+content.type):
                    result[content.type] = html.find('meta',property='twitter:'+content.type).get('content')
                else:
                    if content.type == 'image':
                        if element := html.find(content.special, src=True):
                            result[content.type] = element.get('src')
                        else:
                            if element := html.find(content.special):
                                result[content.type] = element.string
                    elif content.type == 'title':
                        result[content.type] = html.title.string
            return result
        except requests.exceptions.Timeout:
            CUSTOM_LOGGER.construct(
                title="UrlSharing",
                description="TimeOut ERROR",
                level="info",
                metadata={
                    "Metrics": {
                        "url": self.url,
                        "max wait for response ": "10.0 sec",
                    },
                },
            )
        except Exception as e:
            CUSTOM_LOGGER.construct(
                title="UrlSharing",
                description="Exception",
                level="error",
                metadata={
                    "Metrics": {
                        "url": self.url,
                        "max wait for response ": "10.0 sec",
                    },
                    "Error":e
                },
            )
        finally:
            CUSTOM_LOGGER.construct(
                title='UrlSharing using',
                description='UrlSharing using info',
                level='info',
                metadata={
                    "Metrics": {
                        "url": self.url,
                        "max wait for response ": "10.0 sec",
                    },
                    'content_types': [content_type.__dict__ for content_type in self.content_types]
                }

            )
            CUSTOM_LOGGER.send()