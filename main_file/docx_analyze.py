import re
import spacy
from docx import Document
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
import sys

# 尝试加载spacy模型
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("无法加载spacy模型，请确保模型已正确安装。")
    nlp = None


def extract_keywords_text_rank(text):
    """
    使用TextRank算法提取文本中的关键词
    """
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        keywords = summarizer(parser.document, 10)  # 提取10个关键词
        return [keyword.word for keyword in keywords]
    except Exception as e:
        print(f"关键词提取时发生错误: {e}")
        return []


# 解析.docx文件
def parse_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"解析.docx文件时出错: {e}")
        return ""


# 使用NER识别品牌名称、热门关键词、流行趋势
def ner_analysis(text):
    if nlp is None:
        return [], []
    doc = nlp(text)
    brand_names = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            brand_names.append(ent.text)
    keywords = extract_keywords_text_rank(text)
    return brand_names, keywords


# 结合搜索引擎排序算法，筛选最具影响力的营销内容
# 这里简单以文本长度和关键词出现次数作为排序依据
def sort_marketing_content(html_content, keywords):
    try:
        sections = re.split(r'\n+|\s{2,}', html_content.strip())
        content_scores = []
        for section in sections:
            keyword_count = sum([section.count(keyword) for keyword in keywords])
            score = len(section) + keyword_count
            content_scores.append((section, score))
        sorted_content = sorted(content_scores, key=lambda item: item[1], reverse=True)
        return [c[0] for c in sorted_content]
    except Exception as e:
        print(f"筛选营销内容时发生错误: {e}")
        return []


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供.docx文件路径作为命令行参数")
        sys.exit(1)
    docx_file_path = sys.argv[1]
    docx_text = parse_docx(docx_file_path)
    if docx_text:
        brand_names_docx, keywords_docx = ner_analysis(docx_text)
        print("识别到的.docx文件中的品牌名称:", brand_names_docx)
        print("识别到的.docx文件中的热门关键词:", keywords_docx)
        sorted_marketing_docx = sort_marketing_content(docx_text, keywords_docx)
        print("最具影响力的.docx文件中的营销内容:")
        for content in sorted_marketing_docx[:5]:
            print(content)