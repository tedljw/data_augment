# data_augment
NLP的数据增强Demo

这是一个数据增强的代码，思路来源于[Easy Data Augmentation Techniques](https://github.com/jasonwei20/eda_nlp)，然后对这个代码转了中文支持。具体原理可查看[NLP中一些简单的数据增强技术](https://blog.csdn.net/hero00e/article/details/89523970)。

## 需要安装的库

这里使用的是hanlp分词，所以你需要安装hanlp。
本代码使用[同义词词林](https://github.com/yaleimeng/Final_word_Similarity)做同义词查询，原版是使用nltk做英文的同义词查询，我尝试使用过python的同义词包synonyms，但是效果不是很好，其他同学可以尝试一下，或者推荐更好的同义词库给我，谢谢。
停用词使用的百度和哈工大的停用词表。

## 使用方法

```bash
python augment.py --input=test_input.csv --output=test_output.csv --num_aug=20 --alpha=0.05
```

## 添加一个翻译的方法

```bash
python translate.py 

中文转英文: Hello
英文转中文: 你好
```
