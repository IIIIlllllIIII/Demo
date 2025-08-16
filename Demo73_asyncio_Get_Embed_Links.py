# aiohttp(Asynchronous I/O HTTP)使用aiohttp库实现的异步爬虫程序，用于抓取多个页面中的链接，并将结果写入文件。
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
from aiohttp import ClientSession   # 引入ClientSession，默认ClientSession的大小为100个任务，默认超时时间为30秒
import aiohttp.http_exceptions  

# 配置日志记录器，format格式、level级别、datafmt时间戳格式、stream输出流
logging.basicConfig(
    format= "%(asctime)s %(levelname)s:%(name)s %(message)s",   # asctime(ascent time)日志消息的时间部分的格式化字符串
    level= logging.DEBUG,
    datefmt= "%H:%M:%S",
    stream= sys.stderr,
)

logger= logging.getLogger('areq')   # 创建名为areq的日志记录器，
logging.getLogger('chardet.charsetprober').disabled = True  # 禁用chardet.charsetprober的日志记录器，该记录器用于检测字符集编码

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
        aiohttp.ClientError,    # ClientErro客户端错误，用于捕获与客户端请求相关的异常
        aiohttp.http_exceptions.HttpProcessingError,    # 用于表示HTTP请求处理过程中的异常，例如无效的请求和服务器错误
    ) as e:
        logger.error(
            'aiohttp exception for %s [%s]: %s',
            url,
            getattr(e, 'status', None),     # 获取异常的状态码，getattr()函数用于获取对象的status属性，如果属性不存在，则返回默认值None
            getattr(e, 'message', None),
        )
        return found
    
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured: %s", getattr(e, "__dict__", {})
        )
        return found
    
    else:
        for link in HREF_RE.findall(html):  # findall()函数用于在字符串中搜索匹配href的属性，并将所有匹配项返回一个列表
            try:
                abslink = urllib.parse.urljoin(url, link)   # urljoin()函数用于将相对URL转换为绝对URL，这个绝对URL是基于某个基本URL的
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s")
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        
        return found

# 将从url获取到的HREFs写入文件file
async def write_one(file: IO, url: str, **kwargs) -> None:  # 这里的**kwargs表示可变参数，bulk_crawl_and_write中传递的session被**kwargs接收，并传递给parse()方法
    res = await parse(url= url, **kwargs)   # 调用parse()方法，获取url对应的页面HTML中的HREFs
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")
        logger.info("Wrote results for source URL: %s", url)

# (bulk大量的, crawl抓取)
async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:  # 其中的IO是输入/输出流对象的抽象，它不是一个具体的数据类型而是用于类型注解的标记
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
    with open(outpath, "w+") as outfile:    # w+表示打开文件，如果文件不存在则创建，如果存在文件则先全部删除再进行写入操作
        outfile.write("source_url\tfound_url\n")
        
    asyncio.run(bulk_crawl_and_write(file= outpath, urls= urls))