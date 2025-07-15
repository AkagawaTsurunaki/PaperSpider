import json
import time

import pandas as pd
from loguru import logger
from tqdm import tqdm

from config import read_config
from parser.detail_parser import parse_detail, fetch_detail_page
from parser.search_parser import fetch_search_page, parse_search_page
from util import read_html, save_html

_config = read_config()
_database = {}
_result_json_path = "result.json"
_excel_output_path = "result.xlsx"


def analyze_base_info():
    # 第一阶段先获取基础信息
    for searchissn in tqdm(_config.issnList):
        html_doc = None
        if not _config.overwriteExistedHtml:
            try:
                html_doc = read_html(searchissn)
            except FileNotFoundError:
                pass
        if html_doc is None:
            html_doc = fetch_search_page(searchissn)
            save_html(searchissn, html_doc)
            time.sleep(_config.sleepInterval)
        result = parse_search_page(html_doc)
        _database[result['journalid']] = result
        logger.info(
            f"完成了对 {searchissn} 的搜索：\n{json.dumps(result, ensure_ascii=False, indent=4)}")

    logger.info("基础信息获取完毕！")


def analyze_detail_info():
    # 细粒度地获取历年指标
    for journalid, result in tqdm(_database.items()):
        html_doc = None
        if not _config.overwriteExistedHtml:
            try:
                html_doc = read_html(f"detail-{journalid}")
            except FileNotFoundError:
                pass
        if html_doc is None:
            html_doc = fetch_detail_page(journalid)
            save_html(f"detail-{journalid}", html_doc)
            time.sleep(_config.sleepInterval)

        detail = parse_detail(html_doc)
        for key, value in detail.items():
            result[key] = value
        _database[journalid] = result

    logger.info("详细信息获取完毕！")


def save_data():
    with open(_result_json_path, mode='w+', encoding='utf-8') as file:
        file.write(json.dumps(_database, indent=4, ensure_ascii=False))
    logger.info(f"解析的 JSON 数据已保存至：{_result_json_path}")


def json_to_excel():
    df = pd.read_json(_result_json_path)
    df.to_excel(_excel_output_path, index=False)
    logger.info(f"转换的 Excel 文件已保存至: {_excel_output_path}")


if __name__ == "__main__":
    analyze_base_info()
    analyze_detail_info()
    save_data()
    logger.info("所有数据保存完毕！")
