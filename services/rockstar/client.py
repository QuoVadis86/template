import asyncio
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from playwright.async_api import BrowserContext
from playwright.async_api import Page
from  utils.tools import convert_cookies

class RockStarClient():
    def __init__(
        self,
        headers: Dict[str, str],
        playwright_page: Page,
        cookie_dict: Dict[str, str],
    ):
        self.headers = headers
        self._host = "https://www.rockstar.com/"
        self.playwright_page = playwright_page
        self.cookie_dict = cookie_dict

    async def login_status(self) -> bool:
        """get a note to check if login state is ok"""
      
        return False

    async def update_cookies(self, browser_context: BrowserContext):
        cookie_str, cookie_dict = convert_cookies(await browser_context.cookies())
        self.headers["Cookie"] = cookie_str
        self.cookie_dict = cookie_dict

    async def search_job(self, filters: str):
        """
        web search api
        :param filters: search filters
        :return:
        """
      
        return

    async def get_job(self, job_id: str) -> Dict:
        """
        rockstar web job detail api
        :param job_id:
        :return:
        """
        return   
    async def send_message(self,user_id: str, message: str):
        """
        send message to user
        :param user_id:
        :param message:
        :return:
        """
       
        return
