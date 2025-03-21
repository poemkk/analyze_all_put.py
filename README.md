# 文件解析与文本分析工具

## 简介
该Python项目旨在提供一个多功能的文件解析与文本分析工具。它能够处理多种常见文件格式（如PDF、DOCX、HTML、DJVU），提取其中的文本内容，并对提取的文本进行命名实体识别、关键词提取、句法分析、词法化和词干化等分析操作。

## 功能特性
- **文件解析**：支持解析PDF、DOCX、HTML、DJVU格式的文件，准确提取文本内容。
- **文本分析**：
    - **命名实体识别（NER）**：识别文本中的品牌名称、组织和产品等实体。
    - **关键词提取**：运用TextRank算法提取文本中的热门关键词。
    - **句法分析**：分析文本中词元的词性、依存关系等句法信息。
    - **词法化与词干化**：对文本进行词法化和词干化处理，规范文本词汇形式。

## 运行环境
- **操作系统**：理论上支持Windows、macOS、Linux等主流操作系统。
- **Python版本**：建议使用Python 3.6 - 3.10版本，以确保对相关库的良好兼容性。

## 依赖安装
### 安装Python依赖库
在项目目录下，使用以下命令安装所需的Python库：
```bash
pip install -r requirements.txt
```
如果没有`requirements.txt`文件，可依次安装以下库：
- `spacy`：用于自然语言处理，包括命名实体识别、词性标注等功能。安装命令：`pip install spacy` ，并根据需要下载对应语言模型（如`python -m spacy download zh_core_web_sm` 、`python -m spacy download ru_core_news_sm` 、`python -m spacy download en_core_web_sm` ）。
- `PyPDF2`：用于解析PDF文件，安装命令：`pip install PyPDF2` 。
- `python-docx`：用于处理DOCX文件，安装命令：`pip install python-docx` 。
- `BeautifulSoup4`：用于解析HTML文件，安装命令：`pip install beautifulsoup4` 。
- `sumy`：用于文本摘要和关键词提取，安装命令：`pip install sumy` 。
- `langdetect`：用于检测文本语言，安装命令：`pip install langdetect` 。
- `jieba`：用于中文分词，安装命令：`pip install jieba` 。
- `nltk`：自然语言处理工具包，安装命令：`pip install nltk` ，并运行`nltk.download('wordnet')` 下载所需语料库。

### 安装系统依赖（针对DJVU文件解析）
如果需要解析DJVU文件，需安装`djvutxt`工具：
- **macOS**：使用Homebrew安装，命令为`brew install djvulibre` 。
- **Ubuntu/Debian**：使用命令`sudo apt-get install djvulibre-bin` 安装。
- **Windows**：从[DjVuLibre官网](https://sourceforge.net/projects/djvu/files/)下载安装包进行安装。

## 代码方法介绍
### 加载停用词相关
- **`load_stopwords`**
    - **功能**：从指定路径的文件中读取停用词，将每一行的停用词去除首尾空格后，添加到一个集合中并返回。
    - **参数**：`file_path` 为存储停用词的文件路径，要求文件以UTF - 8编码，每行一个停用词。
    - **应用场景**：在文本处理中，用于获取特定语言的停用词集合，后续在关键词提取等操作中，可用于过滤掉无实际意义的常见词汇。
### 文件解析相关
- **`parse_pdf`**
    - **功能**：接收一个PDF文件路径作为参数，以二进制只读模式打开PDF文件，使用`PyPDF2`库逐页提取文本内容，并将所有页的文本累加到一个字符串中返回。如果在解析过程中出现异常，记录错误日志并返回空字符串。
    - **参数**：`file_path` 为要解析的PDF文件的路径。
    - **应用场景**：当需要从PDF格式的文档中提取文本进行后续分析时使用。
- **`parse_docx`**
    - **功能**：接受一个DOCX文件路径作为参数，使用`python - docx`库打开文件，遍历文件中的每个段落，将段落文本提取出来添加到列表中，最后将列表中的文本用换行符连接并返回。若解析过程出错，记录错误日志并返回空字符串。
    - **参数**：`file_path` 为要解析的DOCX文件的路径。
    - **应用场景**：用于从DOCX格式的文档中提取文本内容，以便进一步分析。
- **`parse_html`**
    - **功能**：以只读模式打开指定路径的HTML文件，使用`BeautifulSoup`库结合`html.parser`解析器对文件内容进行解析，提取其中的文本内容并返回。若文件未找到或解析过程中出现其他异常，记录错误日志并返回空字符串。
    - **参数**：`file_path` 为要解析的HTML文件的路径。
    - **应用场景**：用于从HTML格式的文档中提取文本，为后续的文本分析做准备。
- **`parse_djvu`**
    - **功能**：尝试使用`subprocess`模块调用`djvutxt`命令行工具来解析DJVU文件。运行该命令并捕获输出，若命令执行成功（返回码为0），则返回提取的文本内容；否则记录错误日志并返回空字符串。若在调用过程中出现异常，同样记录错误日志并返回空字符串。
    - **参数**：`file_path` 为要解析的DJVU文件的路径。
    - **应用场景**：用于从DJVU格式的文件中提取文本，前提是系统已正确安装`djvutxt`工具。
### 文本分析相关
- **`ner_analysis`**
    - **功能**：首先使用`langdetect`库检测输入文本的语言，然后根据检测到的语言加载相应的`spacy`语言模型。使用加载的模型对文本进行处理，遍历文本中的命名实体，若实体标签为“ORG”（组织）或“PRODUCT”（产品），则将其添加到品牌名称列表中。最后调用`extract_keywords`函数提取关键词，并返回品牌名称列表和关键词列表。若在分析过程中出现异常，记录错误日志并返回空的品牌名称和关键词列表。
    - **参数**：`text` 为要进行分析的文本内容。
    - **应用场景**：用于识别文本中的品牌名称等实体以及提取相关关键词，可应用于市场调研、文本信息挖掘等场景。
- **`extract_keywords`**
    - **功能**：先使用`langdetect`库检测文本语言，对于中文文本，使用`jieba`库进行分词并重新拼接成新文本；对于其他语言文本，直接使用原文本。手动创建一个简单的分词器，实现句子分割和单词分割方法。然后使用`sumy`库的`PlaintextParser`结合分词器解析文本，再通过`TextRankSummarizer`提取10个关键句子。遍历这些关键句子，过滤掉停用词后，将单词添加到关键词列表中并返回。若在提取过程中出现异常，记录错误日志并返回空列表。
    - **参数**：`text` 为要提取关键词的文本。
    - **应用场景**：用于从文本中提取具有代表性的关键词，可帮助快速了解文本核心内容，适用于文本摘要、信息检索等领域。
- **`syntax_analysis`**
    - **功能**：使用`langdetect`库检测文本语言，根据检测结果加载相应的`spacy`语言模型。使用加载的模型对文本进行处理，遍历处理后的文本中的每个词元（token），打印出词元的文本、词性、依存关系和头词信息。若在句法分析过程中出现异常，记录错误日志。
    - **参数**：`text` 为要进行句法分析的文本。
    - **应用场景**：用于深入分析文本的语法结构，了解词与词之间的关系，在自然语言处理研究、语言教学等方面有一定应用价值。
### 文本预处理相关
- **`lemmatize_text`**
    - **功能**：使用`nltk`库的`WordNetLemmatizer`对输入文本进行词法化处理。将文本按单词分割，对每个单词进行词法化操作，然后将处理后的单词重新拼接成文本并返回。
    - **参数**：`text` 为要进行词法化处理的文本。
    - **应用场景**：在文本预处理阶段，将单词还原为其基本形式，便于后续的文本分析和处理，例如在文本分类、情感分析等任务中规范文本词汇。
- **`stem_text`**
    - **功能**：使用`nltk`库的`PorterStemmer`对输入文本进行词干化处理。将文本按单词分割，对每个单词进行词干提取操作，然后将处理后的单词重新拼接成文本并返回。
    - **参数**：`text` 为要进行词干化处理的文本。
    - **应用场景**：在文本预处理中，去除单词的词缀，提取词干，减少词汇的形态变化，有助于提高文本分析的效率和准确性，常用于信息检索、文本聚类等场景。

## 注意事项
- 确保在运行程序前已正确安装所有依赖库和系统依赖工具，否则可能导致程序运行出错。
- 不同语言模型的下载可能需要一定的网络环境和时间，请耐心等待。

## 贡献与反馈
欢迎各位开发者为项目贡献代码、提出问题或建议。如果在使用过程中遇到任何问题，或者有新的功能需求，可在GitHub仓库的Issues板块中提交相关内容。 
