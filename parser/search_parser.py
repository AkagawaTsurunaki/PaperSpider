import re
from xml.etree.ElementTree import Element

import requests
from bs4 import BeautifulSoup
from lxml import html

from util import check_risk_ctrl


def fetch_search_page(searchissn: str = "") -> str:
    url = 'https://www.letpub.com.cn/index.php?page=journalapp&view=search'
    data = {
        "searchname": "",
        "searchissn": searchissn,
        "searchfield": "",
        "searchimpactlow": "",
        "searchimpacthigh": "",
        "searchscitype": "",
        "view": "search",
        "searchcategory1": "",
        "searchcategory2": "",
        "searchjcrkind": "",
        "searchopenaccess": "",
        "searchsort": "relevance"
    }

    response = requests.post(url, data=data)
    response.raise_for_status()
    result = response.content.decode("utf-8")
    check_risk_ctrl(result)
    return result


def parse_search_page(html_doc: str):
    result = {}

    soup = BeautifulSoup(html_doc, 'html.parser')
    container = soup.find_all('th', {'class': 'table_yjfx_th'})
    titles = []
    for title in container:
        titles.append(title.text)

    tree = html.fromstring(html_doc)
    values = []
    for i in range(1, len(titles) + 1):
        elements = tree.xpath(
            f'//*[@id="yxyz_content"]/table[2]/tr[3]/td[{i}]')
        if elements is not None and len(elements) == 1:
            value = _parse_text(elements[0]).strip(" \n")
            values.append(value)

    # Link
    link_elms = tree.xpath('//*[@id="yxyz_content"]/table[2]/tr[3]/td[2]/a')
    if link_elms is not None and len(link_elms) == 1:
        link = link_elms[0].attrib['href']
        journalid = _match_journalid(link)
        result['journalid'] = journalid
    else:
        result['journalid'] = None

    for k, v in zip(titles, values):
        result[k] = v

    return result


def _match_journalid(url: str) -> str | None:
    match = re.search(r'journalid=(\d+)', url)
    if match:
        journalid = match.group(1)
        return journalid
    return None


def _parse_text(element: Element) -> str:
    if element.tag.lower() in {'script', 'style'}:
        return ""

    parts = []

    if element.text and element.text.strip():
        parts.append(element.text.strip())

    for child in element:
        child_text = _parse_text(child)
        if child_text:
            parts.append(child_text)

    if element.tail and element.tail.strip():
        parts.append(element.tail.strip())

    return ' '.join(parts).strip()
