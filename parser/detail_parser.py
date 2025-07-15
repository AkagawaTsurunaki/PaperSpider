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
    cas_result = []
    # [!WARNING] 这里可能需要修改，但是目前它能跑，主要问题在于详细页面可能会少几行或者多几行
    for i in range(20, 50):
        cas_type = tree.xpath(f'//*[@id="yxyz_content"]/table[3]/tbody/tr[{i}]/td[2]/table/tr[2]/td[1]')
        if len(cas_type) == 1:
            cas_type = cas_type[0].text
            if cas_type is not None:
                cas_result.append(cas_type.strip())
        cas_rank = tree.xpath(f'//*[@id="yxyz_content"]/table[3]/tbody/tr[{i}]/td[2]/table/tr[2]/td[1]/span[2]')
        if len(cas_rank) == 1:
            cas_rank = cas_rank[0].text
            if cas_rank is not None:
                cas_result.append(cas_rank.strip())
    cas2025_type, cas2025_rank = cas_result[0], cas_result[1]
    cas2023_type, cas2023_rank = cas_result[2], cas_result[3]
    cas2022_type, cas2022_rank = cas_result[4], cas_result[5]
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
