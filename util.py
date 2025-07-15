import os
import re

from bs4 import BeautifulSoup


class AccessLimitError(RuntimeError):
    pass


def check_risk_ctrl(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    text = soup.getText()
    if "您请求页面的速度过快" in text:
        raise AccessLimitError(
            "⚠️ 对方服务器检测到我们已达到访问限制，建议等待较长一段时间后重试，或调整 `sleepInterval` 值到更大后重试。")


def to_valid_filename(name: str) -> str:
    name = re.sub(r'[\/:*?"<>|\x00-\x1f]', '_', name)
    name = name.replace(' ', '_')
    name = name.strip().strip('.')
    name = re.sub(r'_+', '_', name)
    name = re.sub(r'\.+', '.', name)
    return name


def save_html(name: str, html_doc: str):
    if not os.path.exists("data"):
        os.mkdir("data")
    path = f"data/{name}.html"
    if os.path.exists(path):
        os.remove(path)
    with open(path, mode='w+', encoding='utf-8') as file:
        file.write(html_doc)


def read_html(name: str) -> str:
    with open(f"data/{name}.html", mode='r', encoding='utf-8') as file:
        result = file.read()
        return result
