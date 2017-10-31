Team NOOBS Solution - 秒针&数问 品牌安全黑客马拉松
======
比赛相关页面：https://dataquestion.com/competition/miaozhen-prize

简介
======
这个 Repository 包含我们在比赛当天所使用的全部代码以及语料库。由于节省空间的考虑，parsed_pages/ 文件夹被包含在了 .gitignore 文件中，因此测试之前请自行建立该文件夹


方案架构
======
我们的解决方案由一系列 microservice 组成。每一个 microservice 对应 lib 文件夹下的一个模块，包括：

**1. URL 列表获取 (URL list fetching)**

**用途：访问数问官方接口并返回 URL 列表**

  [lib/downloader.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/downloader.py)

*调用模块: requests*


**2. 多进程页面爬取以及页面元素提取 (Webpage parsing & Feature extraction)**

  [lib/parser.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/parser.py)
  [lib/main_parse.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/main_parse.py)

*调用模块: requests, BeautifulSoup, multiprocessing*


**3. 特征工程 (Feature Engineering)**
    
    lib/transformer.py

*调用模块:* 

* synonyms (最好的中文近义词工具包 https://github.com/huyingxi/Synonyms)
* jieba (“结巴”中文分词 https://github.com/fxsjy/jieba)
* zhconv (中文简繁转换 https://github.com/siuying/zhconv)

**4. 模型分类 (Classification)**

    lib/classifier.py

*调用模块: sklearn, numpy, math* 

**5. 人工判定模糊结果 (Manual labelling)**

    lib/misc.py/manual_rate
    lib/selenium_helper

*调用模块: selenium* 

**6. 合并结果并提交 (Result ensembling & Submission)**

    lib/submitter

*调用模块: requests*

使用方法
======
1. 设定参数

由于各个 microservice 均有可供调整的设置参数，我们决定将各部分所用的参数集中在一处 (`config.json`) 并于脚本起始处载入以便于管理

2. 运行`demo.py`

我们的脚本有两个模式，`p`模式 (production) 用于正式比赛提交窗口期间，会调用 downloader 模块下载 URL 列表并且爬取页面； `t`模式 (testing) 用于调试期间，此模式下脚本会读取本地自定义 URL 列表进行爬取
