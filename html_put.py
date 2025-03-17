import re
import spacy
from bs4 import BeautifulSoup
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 解析HTML文件的函数
def parse_html(file_path):
    try:
        if not file_path or not isinstance(file_path, str):
            raise ValueError("无效的文件路径，路径必须是字符串类型")
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = soup.get_text()
            return text_content
    except FileNotFoundError:
        logging.error(f"文件未找到: {file_path}")
        return ""
    except UnicodeDecodeError:
        logging.error(f"文件编码错误: {file_path}，请检查文件编码是否为utf-8")
        return ""
    except Exception as e:
        logging.error(f"解析HTML文件时出错: {e}")
        return ""


# 使用TextRank算法提取关键词
def extract_keywords(text):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("无效的文本输入，文本必须是字符串类型")
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        keywords = summarizer(parser.document, 10)
        return [keyword.word for keyword in keywords]
    except Exception as e:
        logging.error(f"关键词提取时出错: {e}")
        return []


# 使用NER识别品牌名称、热门关键词、流行趋势的函数
def ner_analysis(text):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("无效的文本输入，文本必须是字符串类型")
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        brand_names = []
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                brand_names.append(ent.text)
        keywords = extract_keywords(text)
        return brand_names, keywords
    except Exception as e:
        logging.error(f"NER分析时出错: {e}")
        return [], []


# 结合搜索引擎排序算法，筛选最具影响力的营销内容的函数
def sort_marketing_content(html_content, keywords):
    try:
        if not html_content or not isinstance(html_content, str) or not keywords or not isinstance(keywords, list):
            raise ValueError("无效的输入，html_content必须是字符串类型，keywords必须是列表类型")
        sections = re.split(r'\n+|\s{2,}', html_content.strip())
        content_scores = []
        for section in sections:
            keyword_count = sum([section.count(keyword) for keyword in keywords])
            score = len(section) + keyword_count
            content_scores.append((section, score))
        sorted_content = sorted(content_scores, key=lambda item: item[1], reverse=True)
        return [c[0] for c in sorted_content]
    except Exception as e:
        logging.error(f"筛选营销内容时出错: {e}")
        return []


def html_main():
    html_file_path = input("请输入你的html文件路径: ")
    if not html_file_path or not isinstance(html_file_path, str) or not html_file_path.endswith('.html'):
        logging.error("无效的文件路径，请输入有效的.html文件路径")
        return
    html_text = parse_html(html_file_path)
    if html_text:
        brand_names_html, keywords_html = ner_analysis(html_text)
        print("识别到的.html文件中的品牌名称:", brand_names_html)
        print("识别到的.html文件中的热门关键词:", keywords_html)
        sorted_marketing_html = sort_marketing_content(html_text, keywords_html)
        print("最具影响力的.html文件中的营销内容:")
        for content in sorted_marketing_html[:5]:
            print(content)


# 防止自动执行主逻辑
if __name__ == "__main__":
    html_main()