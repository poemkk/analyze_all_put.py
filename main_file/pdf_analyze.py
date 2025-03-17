import re
import spacy
import PyPDF2
import logging


# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 解析.pdf文件
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
    except Exception as e:
        logging.error(f"解析.pdf文件时出错: {e}")
        return ""


# 使用NER识别品牌名称、热门关键词、流行趋势
def ner_analysis(text):
    try:
        if not text or not isinstance(text, str):
            raise ValueError("无效的文本输入，文本必须是字符串类型")
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        brand_names = []
        keywords = []
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT"]:
                brand_names.append(ent.text)
        words = re.findall(r'\w+', text.lower())
        word_counts = {}
        for word in words:
            if len(word) > 2:
                word_counts[word] = word_counts.get(word, 0) + 1
        sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
        keywords = [w[0] for w in sorted_words[:10]]
        return brand_names, keywords
    except Exception as e:
        logging.error(f"NER分析时出错: {e}")
        return [], []


# 结合搜索引擎排序算法，筛选最具影响力的营销内容
# 这里简单以文本长度和关键词出现次数作为排序依据
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


if __name__ == "__main__":
    pdf_file_path = input("请输入PDF文件路径: ")
    pdf_text = parse_pdf(pdf_file_path)
    if pdf_text:
        brand_names_pdf, keywords_pdf = ner_analysis(pdf_text)
        print("识别到的.pdf文件中的品牌名称:", brand_names_pdf)
        print("识别到的.pdf文件中的热门关键词:", keywords_pdf)
        sorted_marketing_pdf = sort_marketing_content(pdf_text, keywords_pdf)
        print("最具影响力的.pdf文件中的营销内容:")
        for content in sorted_marketing_pdf[:5]:
            print(content)
