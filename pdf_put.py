import re
import spacy
import PyPDF2
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 解析.pdf文件的函数
def parse_pdf(file_path):
    try:
        if not file_path or not isinstance(file_path, str):
            raise ValueError("无效的文件路径，路径必须是字符串类型")
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text
    except FileNotFoundError:
        logging.error(f"文件未找到: {file_path}")
        return ""
    except PyPDF2.utils.PdfReadError as e:
        logging.error(f"PDF文件格式错误或损坏: {e}")
        return ""
    except Exception as e:
        logging.error(f"解析.pdf文件时出错: {e}")
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
        # 可以考虑返回一个默认的空列表，避免后续函数出错
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
# 结合搜索引擎排序算法，筛选最具影响力的营销内容的函数
def sort_marketing_content(html_content, keywords):
    try:
        if not html_content or not isinstance(html_content, str) or not keywords or not isinstance(keywords, list):
            # 可以选择返回一个空列表或者给出更友好的提示
            logging.warning("输入不符合要求，无法进行营销内容筛选。")
            return []
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


def pdf_main():
    pdf_file_path = input("请输入你的PDF文件路径: ")
    if not pdf_file_path or not isinstance(pdf_file_path, str) or not pdf_file_path.endswith('.pdf'):
        logging.error("无效的文件路径，请输入有效的.pdf文件路径")
        return
    pdf_text = parse_pdf(pdf_file_path)
    if pdf_text:
        brand_names_pdf, keywords_pdf = ner_analysis(pdf_text)
        print("识别到的.pdf文件中的品牌名称:", brand_names_pdf)
        print("识别到的.pdf文件中的热门关键词:", keywords_pdf)
        sorted_marketing_pdf = sort_marketing_content(pdf_text, keywords_pdf)
        print("最具影响力的.pdf文件中的营销内容:")
        for content in sorted_marketing_pdf[:5]:
            print(content)


# 防止自动执行主逻辑
if __name__ == "__main__":
    pdf_main()