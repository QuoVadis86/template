from typing import Dict, List, Optional, Tuple
from playwright.async_api import Cookie


def convert_cookies(cookies: Optional[List[Cookie]]) -> Tuple[str, Dict]:
    if not cookies:
        return "", {}
    cookies_str = ";".join([f"{cookie.get('name')}={cookie.get('value')}" for cookie in cookies])
    cookie_dict = dict()
    for cookie in cookies:
        cookie_dict[cookie.get("name")] = cookie.get("value")
    return cookies_str, cookie_dict
