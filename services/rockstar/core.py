
import asyncio
import os
import random
import time
from asyncio import Task
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from utils.tools import convert_cookies

from playwright.async_api import BrowserContext
from playwright.async_api import BrowserType
from playwright.async_api import Page
from playwright.async_api import async_playwright

from .client import RockStarClient



class KuaishouCrawler():
    context_page: Page
    ks_client: RockStarClient
    browser_context: BrowserContext

    def __init__(self):
        self.index_url = "https://www.kuaishou.com"
        self.user_agent = utils.get_user_agent()

    async def start(self):
        async with async_playwright() as playwright:
            # Launch a browser context.
            chromium = playwright.chromium
            self.browser_context = await self.launch_browser(chromium, None, self.user_agent, headless=config.HEADLESS)
            # stealth.min.js is a js script to prevent the website from detecting the crawler.
            await self.browser_context.add_init_script(path="spider/MediaCrawler/libs/stealth.min.js")
            self.context_page = await self.browser_context.new_page()
            await self.context_page.goto(f"{self.index_url}?isHome=1")

            # Create a client to interact with the kuaishou website.
            self.ks_client = await self.create_ks_client()
            if not await self.ks_client.pong():
                login_obj = KuaishouLogin(
                    login_type=config.LOGIN_TYPE,
                    login_phone=httpx_proxy_format,
                    browser_context=self.browser_context,
                    context_page=self.context_page,
                    cookie_str=config.COOKIES_KS,
                )
                await login_obj.begin()
                await self.ks_client.update_cookies(browser_context=self.browser_context)
            return await func(**kwargs)

    async def search(self):
        ks_limit_count = 20  # kuaishou limit page fixed value
        if config.CRAWLER_MAX_NOTES_COUNT < ks_limit_count:
            config.CRAWLER_MAX_NOTES_COUNT = ks_limit_count
        start_page = config.START_PAGE
        for keyword in config.KEYWORDS.split(","):
            # source_keyword_var.set(keyword)
            page = 1
            while (page - start_page + 1) * ks_limit_count <= config.CRAWLER_MAX_NOTES_COUNT:
                if page < start_page:
                    page += 1
                    continue
                video_id_list: List[str] = []
                videos_res = await self.ks_client.search_info_by_keyword(
                    keyword=keyword,
                    pcursor=str(page),
                )
                if not videos_res:
                    continue

                vision_search_photo: Dict = videos_res.get("visionSearchPhoto")
                if vision_search_photo.get("result") != 1:
                    continue

                for video_detail in vision_search_photo.get("feeds"):
                    video_id_list.append(video_detail.get("photo", {}).get("id"))
                    # await kuaishou_store.update_kuaishou_video(video_item=video_detail)

                # batch fetch video comments
                page += 1
                await self.batch_get_video_comments(video_id_list)

    async def get_specified_videos(self):
        """Get the information and comments of the specified post"""
        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        task_list = [self.get_video_info_task(video_id=video_id, semaphore=semaphore) for video_id in config.KS_SPECIFIED_ID_LIST]
        video_details = await asyncio.gather(*task_list)
        for video_detail in video_details:
            if video_detail is not None:
                pass
                # await kuaishou_store.update_kuaishou_video(video_detail)
        await self.batch_get_video_comments(config.KS_SPECIFIED_ID_LIST)

    async def get_video_info_task(self, video_id: str, semaphore: asyncio.Semaphore) -> Optional[Dict]:
        """Get video detail task"""
        async with semaphore:
            try:
                result = await self.ks_client.get_video_info(video_id)
                return result.get("visionVideoDetail")
            except DataFetchError as ex:
                return None
            except KeyError as ex:
                return None

    async def batch_get_video_comments(self, video_id_list: List[str]):
        """
        batch get video comments
        :param video_id_list:
        :return:
        """
        if not config.ENABLE_GET_COMMENTS:
            return

        semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
        task_list: List[Task] = []
        for video_id in video_id_list:
            task = asyncio.create_task(self.get_comments(video_id, semaphore), name=video_id)
            task_list.append(task)

        # comment_tasks_var.set(task_list)
        await asyncio.gather(*task_list)

    async def get_comments(self, video_id: str, semaphore: asyncio.Semaphore):
        """
        get comment for video id
        :param video_id:
        :param semaphore:
        :return:
        """
        async with semaphore:
            try:
                await self.ks_client.get_video_all_comments(
                    photo_id=video_id,
                    crawl_interval=random.random(),
                    # callback=kuaishou_store.batch_update_ks_video_comments,
                    max_count=config.CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES,
                )
            except DataFetchError as ex:
            except Exception as e:
                # use time.sleeep block main coroutine instead of asyncio.sleep and cacel running comment task
                # maybe kuaishou block our request, we will take a nap and update the cookie again
                # current_running_tasks = comment_tasks_var.get()
                # for task in current_running_tasks:
                #     task.cancel()
                # time.sleep(20)
                await self.context_page.goto(f"{self.index_url}?isHome=1")
                await self.ks_client.update_cookies(browser_context=self.browser_context)

    @staticmethod
    def format_proxy_info(ip_proxy_info: IpInfoModel) -> Tuple[Optional[Dict], Optional[Dict]]:
        """format proxy info for playwright and httpx"""
        playwright_proxy = {
            "server": f"{ip_proxy_info.protocol}{ip_proxy_info.ip}:{ip_proxy_info.port}",
            "username": ip_proxy_info.user,
            "password": ip_proxy_info.password,
        }
        httpx_proxy = {f"{ip_proxy_info.protocol}": f"http://{ip_proxy_info.user}:{ip_proxy_info.password}@{ip_proxy_info.ip}:{ip_proxy_info.port}"}
        return playwright_proxy, httpx_proxy

    async def create_client(self, httpx_proxy: Optional[str]) -> RockStarClient:
        """Create ks client"""
        cookie_str, cookie_dict = convert_cookies(await self.browser_context.cookies())
      
        client = RockStarClient(
            headers={
                "User-Agent": self.user_agent,
                "Cookie": cookie_str,
                "Origin": self.index_url,
                "Referer": self.index_url,
                "Content-Type": "application/json;charset=UTF-8",
            },
            playwright_page=self.context_page,
            cookie_dict=cookie_dict,
        )
        return client

    async def launch_browser(
        self, chromium: BrowserType, playwright_proxy: Optional[Dict], user_agent: Optional[str], headless: bool = True
    ) -> BrowserContext:
        """Launch browser and create browser context"""
        if config.SAVE_LOGIN_STATE:
            user_data_dir = os.path.join(os.getcwd(), "browser_data", config.USER_DATA_DIR % config.PLATFORM)  # type: ignore
            browser_context = await chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                accept_downloads=True,
                headless=headless,
                proxy=playwright_proxy,  # type: ignore
                viewport={"width": 1920, "height": 1080},
                user_agent=user_agent,
            )
            return browser_context
        else:
            browser = await chromium.launch(headless=headless, proxy=playwright_proxy)  # type: ignore
            browser_context = await browser.new_context(viewport={"width": 1920, "height": 1080}, user_agent=user_agent)
            return browser_context

    async def get_creator_profile(self, user_id) -> None:
        """Get creator's videos and retrieve their comment information."""

        createor_info = await self.ks_client.get_creator_info(user_id=user_id)
        # print("-----------creatinfo",createor_info)
        # print("-----------creatinfo",createor_info['visionProfile']["userProfile"])
        return createor_info["visionProfile"]["userProfile"]

    async def get_creator_videos(self, user_id, pcursor) -> None:
        """Get creator's videos and retrieve their comment information."""
        # Get all video information of the creator
        video_list = await self.ks_client.get_videos_by_creator(user_id=user_id, pcursor=pcursor)
        return video_list

    async def fetch_creator_video_detail(self, video):
        """
        Concurrently obtain the specified post list and save the data
        """
        return await self.ks_client.get_video_info(video.get("photo", {}).get("id"))
        # task_list = self.get_video_info_task(video_list.get("photo", {}).get("id"), semaphore)

    # async def fetch_creator_video_detail(self, video_list: List[Dict]):
    #     """
    #     Concurrently obtain the specified post list and save the data
    #     """
    #     semaphore = asyncio.Semaphore(config.MAX_CONCURRENCY_NUM)
    #     task_list = self.get_video_info_task(video_list.get("photo", {}).get("id"), semaphore)

    #     # task_list = [
    #     #     self.get_video_info_task(post_item.get("photo", {}).get("id"), semaphore) for post_item in video_list
    #     # ]

    #     # video_details = await asyncio.gather(*task_list)
    #     # for video_detail in video_details:
    #     #     if video_detail is not None:
    #     #         await kuaishou_store.update_kuaishou_video(video_detail)

    async def close(self):
        """Close browser context"""
        await self.browser_context.close()
