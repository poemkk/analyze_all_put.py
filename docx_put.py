import re
import spacy
from docx import Document
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 解析.docx文件的函数
def parse_docx(file_path):
    try:
        if not file_path or not isinstance(file_path, str):
            raise ValueError("无效的文件路径，路径必须是字符串类型")
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except FileNotFoundError:
        logging.error(f"文件未找到: {file_path}")
        return ""
    except Exception as e:
        logging.error(f"解析.docx文件时出错: {e}")
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
        # 使用更大的模型
        nlp = spacy.load("en_core_web_lg")
        doc = nlp(text)
        brand_names = []
        for ent in doc.ents:
            logging.info(f"实体: {ent.text}, 标签: {ent.label_}")
            if ent.label_ in ["ORG", "PRODUCT"]:
                brand_names.append(ent.text)
        keywords = extract_keywords(text)
        return brand_names, keywords
    except Exception as e:
        logging.error(f"NER分析时出错: {e}")
        return [], []


# 结合搜索引擎排序算法，筛选最具影响力的营销内容的函数
def sort_marketing_content(docx_content, keywords):
    try:
        if not docx_content or not isinstance(docx_content, str) or not keywords or not isinstance(keywords, list):
            raise ValueError("无效的输入，docx_content必须是字符串类型，keywords必须是列表类型")
        sections = re.split(r'\n+|\s{2,}', docx_content.strip())
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


def docx_main():
    docx_file_path = input("请输入你的docx文件路径: ")
    if not docx_file_path or not isinstance(docx_file_path, str) or not docx_file_path.endswith('.docx'):
        logging.error("无效的文件路径，请输入有效的.docx文件路径")
        return
    docx_text = parse_docx(docx_file_path)
    if docx_text:
        brand_names_docx, keywords_docx = ner_analysis(docx_text)
        print("识别到的.docx文件中的品牌名称:", brand_names_docx)
        print("识别到的.docx文件中的热门关键词:", keywords_docx)
        sorted_marketing_docx = sort_marketing_content(docx_text, keywords_docx)
        print("最具影响力的.docx文件中的营销内容:")
        for content in sorted_marketing_docx[:5]:
            print(content)


# 防止自动执行主逻辑
if __name__ == "__main__":
    docx_main()
