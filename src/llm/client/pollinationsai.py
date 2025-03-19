# -*- coding:utf-8 -*-
# /usr/bin/python
'''
-------------------------------------------------------------------------
@File Name      :  pollinationsai.py
@Run Script     :  python3  pollinationsai.py
@Envs           :  pip install httpx, python-dotenv
-------------------------------------------------------------------------
@Author         :  yaozhangrui, 18860016897
@CodeStyle      :  standard, readable, maintainable and portable!
-------------------------------------------------------------------------
@Description
    调用本地大模型请求器
-------------------------------------------------------------------------
@History
    v1.0    yaozhangrui,  2025/02/19 16:50:40
-------------------------------------------------------------------------
'''
__author__ = 'yaozhangrui'

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import json
import httpx
import asyncio
from typing import Dict, List, Optional

from dotenv import load_dotenv

from src.llm.client.base import BaseClient
from src.llm.types import NotGiven, NOT_GIVEN

class PollinationsAIClient(BaseClient):
    def __init__(self, url: str = None):
        if not os.getenv("POLLINATIONS_URL"):
            load_dotenv()

        self.url = url or os.getenv("POLLINATIONS_URL")
        if not self.url:
            self.url = "https://text.pollinations.ai/"

        self.default_model = os.getenv("POLLINATIONS_API_MODEL", "openai")

        # print(self.url, self.default_model)
    
    def completions(self,
                    messages: List[Dict[str, str]],
                    model: Optional[str] | NotGiven = NOT_GIVEN,
                    ) -> str:
        if model == NOT_GIVEN:
            model = self.default_model
        data = {
            "messages": messages,
            "model": model,
            "seed": 128,
        }
        # print(data)
        headers = { "Content-Type": "application/json", "Connection": "keep-alive", "Accept": "*/*" }
        with httpx.Client(timeout=500) as client:
            response = client.post(self.url, data=json.dumps(data), headers=headers)
            
        # response = requests.post(self.url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            content = response.text
                
        return content


if __name__ == "__main__":
    messages = [
        {"role": "system", "content": "你是一个夸夸助手,你会各种夸奖技巧,能提供十足的情绪价值,你的任务就是安抚我的情绪,给我提供十足的情绪价值."},
        {"role": "user", "content": "我被解雇了"},
    ]
    lc = PollinationsAIClient()
    model = "openai"
    print(lc.completions(messages, model))
