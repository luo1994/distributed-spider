新闻结构化信息提取
=========
>功能：可提取新闻标题、时间、作者、正文等信息

1.标题提取
-------
1.1 如果是特殊的网站，使用指定的正则提取

1.2 否则在网页源代码中的title标签中提取，并去掉`_`、`-`、`|`之后的内容。多为网站名，如：<pre>谱写美丽中国的海南篇章--时政--人民网</pre>

1.3 如经过以上两步还没有匹配到标题，则在`h1`~`h4`标题标签中提取

2、时间提取
-------
2.1 枚举时间正则
    <pre>
    [
    　　"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    　　"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    　　"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    　　"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    　　"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    　　"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    　　"(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    　　"(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    　　"(\d{4}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    　　"(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    　　"(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    　　"(\d{2}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    　　"(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    　　"(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    　　"(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
    　　"(\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    　　"(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
    　　"(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
    　　"(\d{4}年\d{1,2}月\d{1,2}日)",
    　　"(\d{2}年\d{1,2}月\d{1,2}日)",
    　　"(\d{1,2}月\d{1,2}日)"
    ]</pre>
2.2 在正文附近提取（正文位置判断见 *4.正文提取*），这里我在正文上下10行内提取。如正文在 20~30 行 ，则在10~40行之内提取发布时间。（正文开始和结束段落位置不能保证百分百准确，所以暂时没有采用从正文开始位置往前逐行提取时间的方法）

2.3 若正文附近没有提取到时间，则在网页源代码中提取。

2.4 提取时间时，网页源代码需要把html标签替换为`<>`，因为html标签里边的文字可能符合时间正则，会被误提取出来，导致时间不准确

3. 作者提取
-------
3.1 同时间提取类似，枚举作者正则
    <pre>
    [
    　　"责编[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4e00-\u9fa5|:|：]",
    　　"作者[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4e00-\u9fa5|:|：]",
    　　"编辑[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4e00-\u9fa5|:|：]",
    　　"文[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4e00-\u9fa5|:|：]",
    　　"撰文[：|:| |丨|/]\s*([\u4E00-\u9FA5]{2,5})[^\u4e00-\u9fa5|:|：]"
    ]
    </pre>

3.2 在网页源代码中，根据以上正则提取作者信息

3.3 若没有匹配到，则将html标签替换为空格后进一步匹配，因为有的作者和名字中间有标签

3.4 仍没有匹配到，则在html的author标签中提取，正则为`(?i)<meta.*?author.*?content="(.*?)"`

4. 正文提取
-------
### 4.1 正文提取的方法有： ###

- 基于标签用途的正文提取算法（比如title或h1,h2标签一般用作标题，p一般表示正文段落，根据标签的含义去提取正文）
- 基于文本密度的正文提取算法（正文通常文字比较密集）
- 基于数据挖掘思想的网页正文抽取方法
- 基于视觉网页块分析技术的正文抽取

 >正文提取方法一准确度不高，后两种复杂度及学习成本高。此处采用基于文本密度算法提取正文，算法通俗易懂、提取速度快，且准确度在98%以上

### 4.2 基于文本密度正文提取算法讲解 ###

#### 4.1.1 论证： ####

由算法名的表面意思，我们可得知，正文与文本密度有关。统计一篇网上的新闻[http://news.cctv.com/2017/11/30/ARTIvCEUIYEZx9HTsTypXySQ171130.shtml](http://news.cctv.com/2017/11/30/ARTIvCEUIYEZx9HTsTypXySQ171130.shtml "田进：新时代网络视听要做到“四个牢牢把握”和“四个着力”")，行号与字数的对应关系如下：

![](https://i.imgur.com/yzzkdsL.png)

从图中可以看出207~242行之间文字比较密集，而事实上这段区间的内容正好是正文。

### 4.1.2 算法描述 ###
1. 处理html源代码（将html去标签，保留段落标签、图片标签等。将空格和换行符外的其他空白符去掉，空格在提取日期和作者中会用到，换行符用于分隔每行）；

2. 统计连续n段文字的长度，此处用于形容一定区域的文本密度；

3. 将文本最密集处当成正文的所在位置。如第i行~i+x行这段区间文本最密集，则初步将第i行当做正文所在位置；

4. 从正文所在位置向上查找、找到文本块密度小于等于正文文本密度阈值时，算为正文起始位置；

5. 在正文所在位置向下查找、找到文本密度小于等于正文文本密度阈值时，算为正文结束位置；

6. 判断是否为正文：正文一般都包含p标签。此处统计p标签内的文字个数占正文总文字数的比例，所占比例超过一定阈值且正文字数大于一定阈值，则算为正文

**举例说明：**

下图为[http://news.cctv.com/2017/11/30/ARTIvCEUIYEZx9HTsTypXySQ171130.shtml](http://news.cctv.com/2017/11/30/ARTIvCEUIYEZx9HTsTypXySQ171130.shtml "田进：新时代网络视听要做到“四个牢牢把握”和“四个着力”")文本块密度统计，这里将连续10行算一个文本块。则下标为0的文本块所在行数为0~9，下标为1的文本块所在行数为1~10，下标为2的文本块所在行数为2~11... 以此类推（文本块下标与行号相吻合, 一个段落为一行）

![田进：新时代网络视听要做到“四个牢牢把握”和“四个着力” 文本块密度统计](https://i.imgur.com/VNthtqV.png)

从图中可以看出下标为231的文本块文本密度最高。此时，将算法描述步骤3的i值设为231。然后参考步骤4，向前找文本密度块小于正文文本密度阈值的行号，为207行。最后参考步骤5，向后找文本密度块小于正文文本密度阈值的行号，为242行。这与行内文本密度统计图相吻合。所以207行到242行为新闻正文。

**问题1：**为什么不直接用行内文本密度的方法直接找正文所在位置，而是引用了文本块的概念？

**答：**因为网页多种多样，有的正文段落可能就是个图片，有的正文段落就几个字，也有的段落文字虽多但可能是导航或外链等信息。我们不能单纯的用最长段落做为正文所在位置，也不能单单的判断段落长度来定位正文的开始与结束位置。我们需要分析正文的特征，正文部分连续n段文本字数总和比较高，非正文部分连续n段文本字数总和比较低。我们根据文字最密集的文本块来定位正文所在位置，根据一定的阈值来分隔正文文本块与非正文部分。

**问题2：**为什么最后用p标签内文字个数占正文总文字数的比例作为判断是否为正文的依据？

**答：**p标签为段落标签，大多数新闻的正文段落都在p标签里。相反一些外链等文字一般在a标签里。我们用段落占比来判断是不是正文，并根据正文总字数删选，过滤掉新闻首页，中间导航页等非新闻信息。

### 4.1.2 算法实现 ###

1. 处理html源代码，保留p标签、img等标签
    <pre>
    def __replace_str(self, source_str, regex, replace_str = ''):
        '''
        @summary: 替换字符串
        ---------
        @param source_str: 原字符串
        @param regex: 正则
        @param replace_str: 用什么来替换 默认为''
        ---------
        @result: 返回替换后的字符串
        '''
        str_info = re.compile(regex)
        return str_info.sub(replace_str, source_str)

    def __del_html_tag(self, html, save_useful_tag = False):
        '''
        @summary:
        ---------
        @param html:
        @param save_useful_tag:保留有用的标签，如img和p标签
        ---------
        @result:
        '''
        html = self.__replace_str(html, '(?i)<script(.|\n)*?</script>') #(?i)忽略大小写
        html = self.__replace_str(html, '(?i)<style(.|\n)*?</style>')
        html = self.__replace_str(html, '<!--(.|\n)*?-->')
        html = self.__replace_str(html, '(?!&[a-z]+=)&[a-z]+;?', ' ') # 干掉&nbsp等无用的字符 但&xxx= 这种表示参数的除外

        if save_useful_tag:
            html = self.__replace_str(html, r'(?!{useful_tag})<(.|\n)+?>'.format(useful_tag = '|'.join(USEFUL_TAG)))
        else:
            html = self.__replace_str(html, '<(.|\n)*?>')

        html = self.__replace_str(html, '[\f\r\t\v]') # 将空格和换行符外的其他空白符去掉
        html = html.strip()
        return html
    </pre>

    保留的标签为
    <pre>
    USEFUL_TAG = [ # html 中需要保留的标签
        r'&lt;img(.|\n)+?>',

        r'&lt;p(.|\n)*?>',
        r'&lt;/p>',

        r'&lt;span(.|\n)+?>',
        r'&lt;/span>',

        r'&lt;strong.*?>',
        r'&lt;/strong>',

        r'&lt;br.*?/>'
    ]
    </pre>

2. 正文提取

    <pre>
    def get_content(self):
        '''
        @summary:
        基于文本密度查找正文
            1、将html去标签，将空格和换行符外的其他空白符去掉
            2、统计连续n段文字的长度，此处用于形容一定区域的文本密度
            3、将文本最密集处当成正文的开始和结束位置
            4、在正文开始处向上查找、找到文本密度小于等于正文文本密度阈值时，算为正文起始位置。该算法文本密度阈值值为文本密度值的最小值
            5、在正文开始处向下查找、找到文本密度小于等于正文文本密度阈值时，算为正文结束位置。该算法文本密度阈值值为文本密度值的最小值

        去除首页等干扰项：
            1、正文一般都包含p标签。此处统计p标签内的文字数占总正文文字数的比例。超过一定阈值，则算为正文
        待解决：
            翻页 如：http://mini.eastday.com/a/171205202028050-3.html
        ---------
        ---------
        @result:
        '''

        paragraphs = self._text.split('\n')
        # for i, paragraph in enumerate(paragraphs):
        #     print(i, paragraph)

        # 统计连续n段的文本密度
        paragraph_lengths = [len(self.__del_html_tag(paragraph)) for paragraph in paragraphs]
        # paragraph_lengths = [len(paragraph.strip()) for paragraph in paragraphs]
        paragraph_block_lengths = [sum(paragraph_lengths[i : i + MAX_PARAGRAPH_DISTANCE]) for i in range(len(paragraph_lengths))]  # 连续n段段落长度的总和（段落块），如段落长度为[0,1,2,3,4] 则连续三段段落长度为[3,6,9,3,4]

        content_start_pos = content_end_pos = paragraph_block_lengths.index(max(paragraph_block_lengths)) #文章的开始和结束位置默认在段落块文字最密集处
        min_paragraph_block_length = MIN_PARAGRAPH_LENGHT * MAX_PARAGRAPH_DISTANCE
        # 段落块长度大于最小段落块长度且数组没有越界，则看成在正文内。开始下标继续向上查找
        while content_start_pos >= 0 and paragraph_block_lengths[content_start_pos] > min_paragraph_block_length:
            content_start_pos -= 1

        # 段落块长度大于最小段落块长度且数组没有越界，则看成在正文内。结束下标继续向下查找
        while content_end_pos < len(paragraph_block_lengths) and paragraph_block_lengths[content_end_pos] > min_paragraph_block_length:
            content_end_pos += 1

        # 处理多余的换行和空白符
        content = paragraphs[content_start_pos : content_end_pos]
        content = '\n'.join(content)
        content = self.__del_unnecessary_character(content)

        # 此处统计p标签内的文字数占总正文文字数的比例。超过一定阈值，则算为正文
        paragraphs_text_len = len(self.__del_html_tag(''.join(tools.get_info(content, '&lt;p.*?>(.*?)&lt;/p>'))))
        content_text_len = len(self.__del_html_tag(content))
        if content_text_len and content_text_len > MIN_COUNTENT_WORDS and ((paragraphs_text_len / content_text_len) > MIN_PARAGRAPH_AND_CONTENT_PROPORTION):
            self._content_start_pos = content_start_pos
            self._content_end_pos = content_end_pos
            self._paragraphs = paragraphs
            return content
        else:
            return ''
    </pre>
