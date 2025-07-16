import json
import os.path
import time

import pandas as pd
from loguru import logger
from tqdm import tqdm

from config import read_config
from parser.detail_parser import parse_detail, fetch_detail_page
from parser.search_parser import fetch_search_page, parse_search_page
from util import read_html, save_html, to_valid_filename, remove_html

_config = read_config()
_database = {}
_result_json_path = "result.json"
_excel_output_path = "result.xlsx"


def analyze_base_info():
    # 第一阶段先获取基础信息
    for searchissn in tqdm(set(_config.issnList), desc="分析论文基础信息"):
        html_doc = None
        if not _config.overwriteExistedHtml:
            try:
                html_doc = read_html(to_valid_filename(searchissn))
            except FileNotFoundError:
                pass
        if html_doc is None:
            html_doc = fetch_search_page(searchissn=searchissn)
            save_html(to_valid_filename(searchissn), html_doc)
            time.sleep(_config.sleepInterval)
        result = parse_search_page(html_doc)
        if result['journalid'] is None:
            logger.warning(f"😭 ISSN 为 {searchissn} 的内容未找到，请检查您的 ISSN 后重试：journalid 为 null")
            remove_html(to_valid_filename(searchissn))

        _database[result['journalid']] = result

    for searchname in tqdm(set(_config.nameList)):
        html_doc = None
        if not _config.overwriteExistedHtml:
            try:
                html_doc = read_html(to_valid_filename(searchname))
            except FileNotFoundError:
                pass
        if html_doc is None:
            html_doc = fetch_search_page(searchname=searchname)
            save_html(to_valid_filename(searchname), html_doc)
            time.sleep(_config.sleepInterval)
        result = parse_search_page(html_doc)
        if result['journalid'] is None:
            logger.warning(f"😭 期刊/会议名为 {searchname} 的内容未找到，请检查您输入的名称后重试：journalid 为 null")
            remove_html(to_valid_filename(searchname))
        _database[result['journalid']] = result

    logger.info("✅️ 基础信息获取完毕！")


def analyze_detail_info():
    # 细粒度地获取历年指标
    for journalid, result in tqdm(_database.items(), desc="分析论文详细信息"):
        html_doc = None
        if not _config.overwriteExistedHtml:
            try:
                html_doc = read_html(to_valid_filename(f"detail-{journalid}"))
            except FileNotFoundError:
                pass
        if html_doc is None:
            html_doc = fetch_detail_page(journalid)
            save_html(to_valid_filename(f"detail-{journalid}"), html_doc)
            time.sleep(_config.sleepInterval)

        detail = parse_detail(html_doc)
        for key, value in detail.items():
            result[key] = value
        _database[journalid] = result

    logger.info("✅️ 详细信息获取完毕！")


def save_data():
    with open(_result_json_path, mode='w+', encoding='utf-8') as file:
        file.write(json.dumps(_database, indent=4, ensure_ascii=False))
    logger.info(f"💾 解析的 JSON 数据已保存至：{os.path.abspath(_result_json_path)}")


def json_to_excel():
    with open(_result_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    records = [
        {"journalid": jid, **info}
        for jid, info in data.items()
    ]

    df = pd.DataFrame(records)
    df.to_excel(_excel_output_path, index=False)
    logger.info(f"💾 转换的 Excel 文件已保存至: {os.path.abspath(_excel_output_path)}")


if __name__ == "__main__":
    try:
        analyze_base_info()
        analyze_detail_info()
        save_data()
        json_to_excel()
        logger.info("📑 PaperSpider 运行完毕！")
    except Exception as e:
        logger.exception(e)
        logger.error("❌ PaperSpider 运行失败！请查看错误原因。")
