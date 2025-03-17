import requests
from bs4 import BeautifulSoup
import spacy
import re


# 1. 解析HTML页面
def parse_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        return text_content
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return ""


# 2. 使用NER识别品牌名称、热门关键词、流行趋势
def ner_analysis(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    brand_names = []
    keywords = []
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            brand_names.append(ent.text)
    # 简单提取高频词作为热门关键词（实际可优化）
    words = re.findall(r'\w+', text.lower())
    word_counts = {}
    for word in words:
        if len(word) > 2:
            word_counts[word] = word_counts.get(word, 0) + 1
    sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    keywords = [w[0] for w in sorted_words[:10]]
    return brand_names, keywords


# 3. 结合搜索引擎排序算法，筛选最具影响力的营销内容
# 这里简单以文本长度和关键词出现次数作为排序依据
def sort_marketing_content(html_content, keywords):
    sections = re.split(r'\n+|\s{2,}', html_content.strip())
    content_scores = []
    for section in sections:
        keyword_count = sum([section.count(keyword) for keyword in keywords])
        score = len(section) + keyword_count
        content_scores.append((section, score))
    sorted_content = sorted(content_scores, key=lambda item: item[1], reverse=True)
    return [c[0] for c in sorted_content]


if __name__ == "__main__":
    target_url = "https://scikit-learn.org.cn/"  # 替换为实际的文件路径
    html_text = parse_html(target_url)
    if html_text:
        brand_names, keywords = ner_analysis(html_text)
        print("识别到的品牌名称:", brand_names)
        print("识别到的热门关键词:", keywords)
        sorted_marketing = sort_marketing_content(html_text, keywords)
        print("最具影响力的营销内容:")
        for content in sorted_marketing[:5]:
            print(content)
