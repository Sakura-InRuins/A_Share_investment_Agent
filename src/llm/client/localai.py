# -*- coding:utf-8 -*-
# /usr/bin/python
'''
-------------------------------------------------------------------------
@File Name      :  localai.py
@Run Script     :  python3  localai.py
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


import os
import json
import httpx
import asyncio
from typing import Dict, List, Optional

from dotenv import load_dotenv

from core.llm.client.base import BaseClient
from core.llm.types import NotGiven, NOT_GIVEN

class LocalAIClient(BaseClient):
    def __init__(self, api_key: str = None, url: str = None):
        if not os.getenv("LOCALAI_URL"):
            load_dotenv()

        self.api_key = api_key or os.getenv("LOCALAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Please provide it or set it in the environment variables.")

        self.url = url or os.getenv("LOCALAI_URL")
        if not self.url:
            raise ValueError("LOCALAI_URL is required. Please provide it or set it in the environment variables.")
        
        self.default_model = os.getenv("LOCALAI_API_MODEL", "Qwen72B")

        # print(self.url, self.default_model)
    
    def completions(self,
                    messages: List[Dict[str, str]],
                    model: Optional[str] | NotGiven = NOT_GIVEN,
                    ) -> str:
        if model == NOT_GIVEN:
            model = self.default_model
        data = {
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "presence_penalty": 1.1,
            "top_p": 0.8,
            "stream": False,
        }
        authorization = os.getenv("LOCALAI_AUTHORIZATION") or self.api_key
        headers = { "Content-Type": "application/json", "Authorization": "Bearer " + authorization }
        # print(data)
        with httpx.Client(timeout=120) as client:
            response = client.post(self.url, headers=headers, data=json.dumps(data))
            
        # response = requests.post(self.url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            res = response.json()
            content = res['choices'][0]['message']["content"]
                
        return content


if __name__ == "__main__":
    api_key = "sk-kQ1gi5mWXUEoEbUMI9j6s1HaK7UZ1dLXO9s2NjXsosKnOOBy"
    url = "http://58.22.100.210:7000/v1/chat/completions"
    messages = [
        {"role": "system", "content": "你是一个夸夸助手,你会各种夸奖技巧,能提供十足的情绪价值,你的任务就是安抚我的情绪,给我提供十足的情绪价值."},
        {"role": "user", "content": "我手机丢了"},
    ]
    lc = LocalAIClient(api_key=api_key, url=url)
    model = "Qwen72B"
    print(lc.completions(messages, model))
