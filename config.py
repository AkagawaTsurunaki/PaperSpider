import json
from dataclasses import dataclass


@dataclass
class Config:
    issnList: list[str]
    overwriteExistedHtml: bool
    sleepInterval: float


def read_config():
    with open("./config.json", mode='r', encoding='utf-8') as file:
        config = json.loads(file.read())
        return Config(
            issnList=config['issnList'],
            overwriteExistedHtml=config['overwriteExistedHtml'],
            sleepInterval=config['sleepInterval']
        )
