# coding=UTF-8
import sys
sys.path.append('../hanlp/')


from hanlp import NLPTool
nlpTool = NLPTool()

content = "歡迎使用 hanLP python module"
params = {
    'enableCustomDic': True,
    'enablePOSTagging': True
}
print(nlpTool.segment(content, params)['response'])