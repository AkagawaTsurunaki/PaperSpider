import requests
from lxml import html

from util import check_risk_ctrl


def fetch_detail_page(journalid: str):
    url = f"https://www.letpub.com.cn/index.php?journalid={journalid}&page=journalapp&view=detail"
    response = requests.get(url)
    response.raise_for_status()
    result = response.content.decode("utf-8")
    check_risk_ctrl(result)
    return result


def parse_detail(html_doc: str):
    tree = html.fromstring(html_doc)
    # 中科院分区
    cas2025_type = None
    cas2025_type_elms = tree.xpath('//*[@id="yxyz_content"]/table[3]/tbody/tr[29]/td[2]/table/tr[2]/td[1]')
    if len(cas2025_type_elms) == 1:
        cas2025_type = cas2025_type_elms[0].text.strip()

    cas2025_rank = None
    cas2025_rank_elms = tree.xpath('//*[@id="yxyz_content"]/table[3]/tbody/tr[29]/td[2]/table/tr[2]/td[1]/span[2]')
    if len(cas2025_rank_elms) == 1:
        cas2025_rank = cas2025_rank_elms[0].text.strip()

    cas2023_type = None
    cas2023_type_elms = tree.xpath('//*[@id="yxyz_content"]/table[3]/tbody/tr[30]/td[2]/table/tr[2]/td[1]')
    if len(cas2023_type_elms) == 1:
        cas2023_type = cas2023_type_elms[0].text.strip()

    cas2023_rank = None
    cas2023_rank_elms = tree.xpath('//*[@id="yxyz_content"]/table[3]/tbody/tr[30]/td[2]/table/tr[2]/td[1]/span[2]')
    if len(cas2023_rank_elms) == 1:
        cas2023_rank = cas2023_rank_elms[0].text.strip()

    cas2022_type = None
    cas2022_type_elms = tree.xpath('//*[@id="yxyz_content"]/table[3]/tbody/tr[31]/td[2]/table/tr[2]/td[1]')
    if len(cas2022_type_elms) == 1:
        cas2022_type = cas2022_type_elms[0].text.strip()

    cas2022_rank = None
    cas2022_rank_elms = tree.xpath('//*[@id="yxyz_content"]/table[3]/tbody/tr[31]/td[2]/table/tr[2]/td[1]/span[2]')
    if len(cas2022_rank_elms) == 1:
        cas2022_rank = cas2022_rank_elms[0].text.strip()

    result = {}

    if cas2025_type is None and cas2025_rank is None:
        result['中国科学院期刊分区（2025年3月最新升级版）'] = "-"
    else:
        result['中国科学院期刊分区（2025年3月最新升级版）'] = f"{cas2025_type}-{cas2025_rank}"

    if cas2023_type is None and cas2023_rank is None:
        result['中国科学院期刊分区（2023年12月升级版）'] = '-'
    else:
        result['中国科学院期刊分区（2023年12月升级版）'] = f"{cas2023_type}-{cas2023_rank}"

    if cas2022_type is None and cas2022_rank is None:
        result['中国科学院期刊分区（2022年12月旧的升级版）'] = '-'
    else:
        result['中国科学院期刊分区（2022年12月旧的升级版）'] = f"{cas2022_type}-{cas2022_rank}"

    return result
