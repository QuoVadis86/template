import asyncio
import json
from playwright.async_api import async_playwright

async def test_cookie_with_playwright():
    """使用Playwright测试cookie是否有效"""
    # 从配置文件中读取cookie
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            cookie_str = config.get('cookie', '')
            user_agent = config.get('user_agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    except FileNotFoundError:
        print("错误: 找不到配置文件 config.json")
        return
    except json.JSONDecodeError:
        print("错误: 配置文件格式不正确")
        return

    if not cookie_str:
        print("错误: 未设置cookie")
        return

    # 解析cookie字符串为浏览器可接受的格式
    cookies = []
    cookie_pairs = cookie_str.split(';')
    for cookie_pair in cookie_pairs:
        if '=' in cookie_pair:
            cookie_part = cookie_pair.strip()
            if cookie_part:
                try:
                    name, value = cookie_part.split('=', 1)
                    # 只添加有实际域名的cookie
                    if name and value is not None:
                        cookies.append({
                            'name': name,
                            'value': value,
                            'domain': '.rockstargames.com',
                            'path': '/',
                            'httpOnly': False,
                            'secure': True
                        })
                except ValueError:
                    continue

    print(f"解析出 {len(cookies)} 个cookie")

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=user_agent)
        
        # 设置cookie
        if cookies:
            await context.add_cookies(cookies)
            print("Cookie设置完成")
        else:
            print("没有有效的cookie可设置")
        
        # 创建页面
        page = await context.new_page()
        
        print("正在测试使用Playwright访问Rockstar Games网站...")
        
        try:
            # 访问Rockstar Games主页
            response = await page.goto('https://www.rockstargames.com/')
            await page.wait_for_timeout(3000)  # 等待3秒加载
            
            # 检查响应状态
            status = response.status if response else "未知"
            print(f"Rockstar Games主页响应状态: {status}")
            
            # 检查当前URL
            current_url = page.url
            print(f"当前URL: {current_url}")
            
            # 获取页面标题
            title = await page.title()
            print(f"页面标题: {title}")
            
            # 检查页面内容是否包含用户相关元素
            try:
                # 查找页面上可能的用户相关元素
                account_link = await page.query_selector("a[href*='account']")
                if account_link:
                    print("✅ 页面包含账户链接，可能已登录")
                else:
                    print("⚠️  页面未找到账户链接")
            except:
                pass
                
            # 尝试访问Social Club
            print("\n正在测试访问Social Club...")
            response = await page.goto('https://socialclub.rockstargames.com/games/gtav/pc/career/overview/gtaonline')
            await page.wait_for_timeout(3000)  # 等待3秒加载
            
            # 检查响应状态
            status = response.status if response else "未知"
            print(f"Social Club页面响应状态: {status}")
            
            # 检查当前URL
            current_url = page.url
            print(f"Social Club URL: {current_url}")
            
            # 获取页面标题
            title = await page.title()
            print(f"页面标题: {title}")
            
            # 判断是否成功访问Social Club
            if 'socialclub.rockstargames.com' in current_url and 'signin' not in current_url and 'login' not in current_url:
                print("✅ Cookie有效! 成功访问Social Club")
                
                # 尝试查找用户相关信息
                try:
                    # 查找可能的用户名元素
                    user_elements = await page.query_selector_all("[class*='user'], [class*='profile'], [class*='account']")
                    if user_elements:
                        print(f"✅ 找到 {len(user_elements)} 个可能的用户相关元素")
                    else:
                        print("⚠️  未找到明显的用户相关元素")
                except Exception as e:
                    print(f"检查用户元素时出错: {e}")
                    
            elif 'signin' in current_url or 'login' in current_url:
                print("❌ Cookie无效或已过期，被重定向到登录页面")
            else:
                print(f"⚠️  被重定向到意外位置: {current_url}")
                
        except Exception as e:
            print(f"错误: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_cookie_with_playwright())