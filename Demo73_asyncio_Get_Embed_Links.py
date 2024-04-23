# aiohttp(Asynchronous I/O HTTP)
# Asynchronous get links embedded in multiple pages
import asyncio
import logging  # 引入logging，日志库
import re   # 引入re(regular expression)正则表达式
import sys
from typing import IO   
import urllib.error
import urllib.parse

import aiofiles # 引入aiofiles
import aiohttp
from aiohttp import ClientSession   # 引入ClientSession
import aiohttp.http_exceptions  

# 配置日志记录器，format格式、level级别、datafmt时间戳格式、stream输出流
logging.basicConfig(
    format= "%(asctime)s %(levelname)s:%(name)s %(message)s",
    level= logging.DEBUG,
    datefmt= "%H:%M:%S",
    stream= sys.stderr,
)

logger= logging.getLogger('areq')   # 创建名为areq的日志记录器，
logging.getLogger('chardet.charsetprober').disabled = True  # 禁用chardet.charsetprober的日志记录器

HREF_RE = re.compile(r'href="(.*?)"')   # 创建正则表达式，匹配href属性的值

# 获取页面HTML的GET请求包装器，kwargs被传递到session.request()方法
async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    resp = await session.request(method= "GET", url= url, **kwargs) # 发送请求
    resp.raise_for_status() # 抛出异常
    
    logger.info("Got response [%s] for URL: %s", resp.status, url)  # 输出日志信息，这里用','合法是因为是logger.info()方法，不是print()方法
    html = await resp.text()
    
    return html

# 获取url对应的页面HTML中的HREFs，并返回一个集合(set)类型
async def parse(url: str, session: ClientSession, **kwargs) -> set:
    found = set()   # 创建一个空集合，set表示无序且元素唯一的集合
    
    try:
        html = await fetch_html(url= url, session= session, **kwargs)
    except(
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        logger.error(
            'aiohttp exception for %s [%s]: %s',
            url,
            getattr(e, 'status', None),
            getattr(e, 'message', None),
        )
        return found
    
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured: %s", getattr(e, "__dict__", {})
        )
        return found
    
    else:
        for link in HREF_RE.findall(html):  # 匹配href的属性并将所有匹配项返回一个列表
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s")
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        
        return found

# 将从url获取到的HREFs写入文件file
async def write_one(file: IO, url: str, **kwargs) -> None:
    res = await parse(url= url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)

# (bulk大量的, crawl抓取)
async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file= file, url= url, session= session, **kwargs)
            )

        await asyncio.gather(*tasks)

if __name__ == '__main__':
    import pathlib
    import sys
    
    assert sys.version_info >= (3, 7)   # 需要3.7以上版本Python
    here = pathlib.Path(__file__).parent    # 获取当前文件路径
    
    with open(here.joinpath("urls.txt")) as infile:
        urls = set(map(str.strip, infile))  # 创建一个集合，将infile中的内容转换为字符串，并去除空格
        
    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tfound_url\n")
        
    asyncio.run(bulk_crawl_and_write(file= outpath, urls= urls))