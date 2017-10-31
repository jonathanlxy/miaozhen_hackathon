Team NOOBS Solution - 秒针&数问 品牌安全黑客马拉松
======
比赛相关页面：https://dataquestion.com/competition/miaozhen-prize

简介
======
这个 Repository 包含我们在比赛当天所使用的全部代码以及语料库。由于节省空间的考虑，parsed_pages/ 文件夹被包含在了 .gitignore 文件中，因此测试之前请自行建立该文件夹

我们的解决方案由一系列 microservice 组成。每一个 microservice 对应 lib 文件夹下的一个 py 脚本，包括：

**1. URL 列表获取 (URL list fetching)**

    - lib/downloader.py

**2. 多进程页面爬取以及页面元素提取 (Webpage parsing & Feature extraction)**

    - lib/parser.py
    - lib/main_parse.py

**3. 特征工程 (Feature Engineering)**

    - lib/transformer.py

**4. 模型分类 (Classification)**

    - lib/classifier.py

**5. 人工判定模糊结果 (Manual labelling)**

    - lib/misc.py/manual_rate
    - lib/selenium_helper

**6. 合并结果并提交 (Result ensembling & Submission)**

    - lib/submitter
