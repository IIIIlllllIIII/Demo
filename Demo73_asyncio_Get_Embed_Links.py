# aiohttp(Asynchronous I/O HTTP)
# Asynchronous get links embedded in multiple pages
import asyncio
import logging
import re
import sys
from typing import IO
import urllib.error
import urllib.parse

import aiofiles
import aiohttp
from aiohttp import ClientSession   # 引入ClientSession

