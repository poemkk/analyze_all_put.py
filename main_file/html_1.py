from bs4 import BeautifulSoup


def parse_html(html_file_path):
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')

            # 提取页面标题
            title = soup.title.string if soup.title else None

            # 提取所有链接
            links = [a.get('href') for a in soup.find_all('a') if a.get('href')]

            # 提取所有段落文本
            paragraphs = [p.get_text() for p in soup.find_all('p')]

            # 提取所有图片链接
            images = [img.get('src') for img in soup.find_all('img') if img.get('src')]

            result = {
                'title': title,
                'links': links,
                'paragraphs': paragraphs,
                'images': images
            }
            return result
    except FileNotFoundError:
        print(f"错误: 文件 {html_file_path} 未找到。")
    except Exception as e:
        print(f"错误: 发生未知错误 {e}。")


if __name__ == "__main__":
    file_path = '/Users/kankan/Desktop/scikit-learn.html'  # 替换为实际的文件路径
    result = parse_html(file_path)
    if result:
        print("页面标题:", result['title'])
        print("\n提取的链接如下:")
        for link in result['links']:
            print(link)
        print("\n提取的段落如下:")
        for para in result['paragraphs']:
            print(para)
        print("\n提取的图片链接如下:")
        for img in result['images']:
            print(img)

