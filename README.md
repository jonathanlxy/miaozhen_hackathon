Team NOOBS Solution - 秒针&数问 品牌安全黑客马拉松
======
比赛相关页面：https://dataquestion.com/competition/miaozhen-prize

简介
======
这个 Repository 包含我们在比赛当天所使用的全部代码以及语料库。由于节省空间的考虑，parsed_pages/ 文件夹被包含在了 .gitignore 文件中，因此测试之前请自行建立该文件夹

我们在本次比赛中所有代码均编写于 Python 3.6 环境下

方案架构
======
我们的解决方案由一系列 microservice 组成。每一个 microservice 对应 lib 文件夹下的一个模块，包括：

**1. URL 列表获取 (URL list fetching)**

**用途：访问数问官方接口并返回 URL 列表**

  [lib/downloader.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/downloader.py)

*调用模块: requests*


**2. 多进程页面爬取以及页面元素提取 (Webpage parsing & Feature extraction)**

**用途：通过多进程进行页面爬取，并将结果以 list 形式返回 URL 列表**

  [lib/parser.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/parser.py)
  [lib/main_parse.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/main_parse.py)

*调用模块: requests, BeautifulSoup, multiprocessing*


**3. 特征工程 (Feature Engineering)**

**用途：将提取后的结果转换为 token2, token3, synonym2, synonym3 的 feature 以传入模型**
  [lib/transformer.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/transformer.py)

*调用模块:* 

* synonyms (最好的中文近义词工具包 https://github.com/huyingxi/Synonyms)
* jieba (“结巴”中文分词 https://github.com/fxsjy/jieba)
* zhconv (中文简繁转换 https://github.com/siuying/zhconv)

**4. 模型分类 (Classification)**

**用途：对每一个 URL 的 feature 进行判断分类并输出分类结果(0/1/-99)。-99代表不确定**

  [lib/classifier.py](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/classifier.py)

*调用模块: sklearn, numpy, math* 

**5. 人工判定模糊结果 (Manual labelling)**

**用途：通过人工阅读 title 进行分类，如果仍然不能确定，则通过 Selenium 在浏览器中打开页面进行进一步判断**

  [lib/misc.py/manual_rate](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/misc.py)
  [lib/selenium_helper](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/selenium_helper.py)

*调用模块: selenium* 

**6. 合并结果并提交 (Result ensembling & Submission)**

**用途：将最终结果转化为规定格式并通过POST进行提交**

  [lib/submitter](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/lib/submitter.py)

*调用模块: requests*

使用方法
======
1. 设定参数

由于各个 microservice 均有可供调整的设置参数，我们决定将各部分所用的参数集中在一处 (`config.json`) 并于脚本起始处载入以便于管理

2. 创建 html 缓存文件夹

在爬取页面的过程中, parser 模块会自动保存所访问过的页面，请根据 config.json 内的设定自行创建 parsed_pages/ 及其子文件夹

3. 运行`demo.py` (注：截图中`-i`是非必要的参数，作用是使脚本运行完成后不退出Python环境）

![Call Script](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/snapshots/call.png)

我们的脚本有两个模式，`p`模式 (production) 用于正式比赛提交窗口期间，会调用 downloader 模块下载 URL 列表并且爬取页面； `t`模式 (testing) 用于调试期间，此模式下脚本会读取本地自定义 URL 列表进行爬取。可以在启动脚本时将'p'或者't'通过命令行传入，也可以等脚本初始化完成后按照提示选择。

![Start](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/snapshots/start.png)
![Parsing](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/snapshots/parsing.png)

爬取结束之后脚本会自动尝试使用模型进行分类。此外，当模型预测结果过于模糊(详见 Classifier.predict() 的`diff_rate`参数)时，脚本将会调用手动打分工具，输出页面标题以进行人工辅助打分。

![Manual Rate]((https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/snapshots/manual_rate.png)

如果通过标题仍无法进行分类，或爬取步骤失败导致无法获取标题时，则通过 Selenium 在浏览器内打开 URL 尝试进一步人工识别

![Selenium](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/snapshots/manual_rate2.png)

在全部打分结束后，脚本将进行自动提交并返回结果与用时

![Submission](https://github.com/jonathanlxy/miaozhen_hackathon/blob/master/snapshots/submit.png)
