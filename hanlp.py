# coding=UTF-8
import sys, yaml
from jpype import *
from os.path import dirname, abspath
sys.path.append(abspath(dirname(__file__))+'/lib/')
import build

class NLPTool:
    modulePath = abspath(dirname(__file__))
    hanLPLibPath = modulePath+'/lib/hanlp-1.3.2/'
    javaClassPath = hanLPLibPath+'hanlp-1.3.2.jar'+':'+hanLPLibPath
    startJVM(getDefaultJVMPath(), '-Djava.class.path='+javaClassPath, '-Xms1g', '-Xmx1g')

    def __init__(self):
        build.properties()
        self._innerConvertEnable = True
        self.HanLP = JClass('com.hankcs.hanlp.HanLP')
        self.CustomDictionary = JClass('com.hankcs.hanlp.dictionary.CustomDictionary')
        self.modulePath = abspath(dirname(__file__))
        self._loadDictionary()

    def _innerConvert(self, inputString, mode):
        if self._innerConvertEnable:
            if mode == '2tc':
                return self.HanLP.convertToTraditionalChinese(inputString)
            elif mode == '2sc':
                return self.HanLP.convertToSimplifiedChinese(inputString)
            elif mode == '2hk':
                return self.HanLP.s2hk(inputString)
            elif mode == '2tw':
                return self.HanLP.s2tw(inputString)
            else:
                return self.HanLP.s2tw(inputString)
        else:
            return inputString
    def _loadDictionary(self, inputParams=None):
        params = {
            'configPath': self.modulePath + '/config/dictionaries.yaml',
            'dicsPath': self.modulePath + '/dics/',
        }

        if inputParams:
            params.update(inputParams)

        self.dicsPath = params['dicsPath']
        with open(params['configPath'], 'r') as stream:
            try:
                yamlFile = yaml.load(stream)

                for key, value in yamlFile['dictionaries'].items():

                    if len(value['parentPosTag']) > 0:
                        parentPosTag = ' '+value['parentPosTag']
                    else:
                        parentPosTag = ''

                    for dictionary in value['list']:
                        print('動態載入辭庫: ', dictionary)
                        with open(params['dicsPath']+dictionary, 'r') as inputTxt:
                            for word in inputTxt.readlines():
                                word = word.replace('\n', '')
                                if len(word) > 0:
                                    self.CustomDictionary.insert(word, key + ' 1' + parentPosTag);
            except yaml.YAMLError as exc:
                print(exc)

    def generalSetting(self, inputParams=None):
        Config = JClass('com.hankcs.hanlp.HanLP$Config')
        if inputParams['enablePOSTagging'] == False:
            Config.ShowTermNature = False
        else:
            Config.ShowTermNature = True
    def segment(self, content, inputParams=None):
        params = {
            'enableCustomDic': True,
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')

        if params['enableCustomDic'] == False:
            StandardTokenizer.SEGMENT.enableCustomDictionary(False)
        else:
            StandardTokenizer.SEGMENT.enableCustomDictionary(True)

        segemntTool = self.HanLP.segment
        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            segments = []
            for v in segemntTool(self._innerConvert(content, '2sc')):
                tempString = str(v).strip()
                segments.append(self._innerConvert(tempString, params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def tcSegment(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            segments = []
            tcTokenizer = JClass('com.hankcs.hanlp.tokenizer.TraditionalChineseTokenizer')
            for v in tcTokenizer.segment(content):
                segments.append(str(v))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def crfSegment(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            segments = []
            CRFSegment = JClass('com.hankcs.hanlp.seg.CRF.CRFSegment')
            segemntTool = CRFSegment().seg
            for v in segemntTool(self._innerConvert(content, '2sc')):
                tempString = str(v).strip()
                if len(tempString)>0:
                    segments.append(self._innerConvert(tempString, params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def jpNameRecognition(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            jpNameSegment = self.HanLP.newSegment().enableJapaneseNameRecognize(True)
            segments = []
            for v in jpNameSegment.seg(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}

    def translatedNameRecognition(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            tranNameSegment = self.HanLP.newSegment().enableTranslatedNameRecognize(True)
            segments = []
            for v in tranNameSegment.seg(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def indexTokenizer(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            IndexTokenizer = JClass('com.hankcs.hanlp.tokenizer.IndexTokenizer')
            segments = []
            for v in IndexTokenizer.segment(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}


    def _getListByTag(self, segResult, tags):
        tempList = []
        tempDict = {}
        returnList = []

        for v in segResult:
            tempString = str(v).strip()
            for tag in tags:
                if len(tempString)>0 and tempString.find('/'+tag)>1:
                    tempList.append(tempString)

        tempSet = set(tempList)
        for item in tempSet:
            tempDict[item] = tempList.count(item)

        import operator, re
        sortedList = sorted(tempDict.items(), key=operator.itemgetter(1))
        sortedList.reverse()

        for v in sortedList:
            tempString = re.sub(r'(\/)\w+', '', v[0])
            # print('tempString: ', tempString ,', ', len(tempString), ', ', v[0])
            if len(tempString) >= 2:
                returnList.append( tempString )

        return returnList
    def _keyword2File(self, words):
        try:
            print(self.dicsPath +'keyword-from-api.txt')
            f = open(self.dicsPath +'keyword-from-api.txt', 'r+')
            for word in words:
                self.CustomDictionary.insert(word, 'keyword 1');
                f.seek(0, 2)
                f.write(word+'\n')
            f.close()
            return 'succes'
        except ValueError:
            print('Add keyword failed!')
            return ValueError

    def keywordByLength(self, content, inputParams=None):
        # 用StandardTokenizer 取出名詞，字數多到少排序，通常字數越多越重要
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw',
            'num': 10
        }
        if inputParams:
            params.update(inputParams)

        if 'num' not in params:
            return {'error': { 'num': '必須輸入 num，為keyword數量'}}

        if isinstance(content, str) and len(content)>0:
            params['enablePOSTagging'] = True

            segResult = self.segment(content, params)
            segmentList = []

            for v in segResult['response']:
                tempString = str(v).strip()
                for tag in ['n', 'keyword', 'iguang']:
                    if len(tempString) > 0 and tempString.find('/'+tag) > 1:
                        segmentList.append(tempString)
            
            segmentList.sort(key = lambda s: len(s), reverse=True)
            keywordList = []
            for i in range(0,params['num']):
                if i < len(segmentList):
                    keywordList.append(self._innerConvert(segmentList[i], params['convertMode']))
                else:
                    break
            return {'response': keywordList}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}

    def keyword(self, content, inputParams=None):
        '''
            # hanLP 原生 keyword

            if isinstance(content, str) and len(content)>0:
                segments = []
                for v in self.HanLP.extractKeyword(self._innerConvert(content, '2sc'), int(params('num')):
                    segments.append(self._innerConvert(str(v), params['convertMode']))
                return {'response': segments}
            else:
                return {'error': { 'content': '長度不得為零的字串'}}
        '''
        # 用StandardTokenizer 取出名詞並統計數量，取重複次數多的
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw',
            'num': 10
        }
        if inputParams:
            params.update(inputParams)

        if 'num' not in params:
            return {'error': { 'num': '必須輸入 num，為keyword數量'}}

        if isinstance(content, str) and len(content)>0:
            params['enablePOSTagging'] = True

            segResult = self.segment(content, params)
            segmentList = self._getListByTag(segResult['response'], ['n', 'keyword', 'iguang'])
            keywordList = []
            for i in range(0,params['num']):
                if i < len(segmentList):
                    keywordList.append(self._innerConvert(segmentList[i], params['convertMode']))
                else:
                    break
            return {'response': keywordList}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def addKeyword(self, keywords):
        if len(keywords) == 0 :
            return {'error': {'keywords': '新增keyword所傳入的陣列，長度不得為0'}}

        newKeywords = []
        for keyword in keywords:
            w2sc = self._innerConvert(keyword, '2sc').lower()
            w2scPOStag= self.HanLP.segment(w2sc)
            if len(w2scPOStag)==1:
                tempString = str(w2scPOStag[0])
                postag = tempString[tempString.find('/')+1:len(tempString)]
                if postag != 'keyword':
                    newKeywords.append(w2sc)
            if len(w2scPOStag)>1:
                newKeywords.append(w2sc)

        if len(newKeywords)>0:
            result = self._keyword2File(newKeywords)
            if result == 'succes':
                return {'response': {'newKeywords': newKeywords}}
            else:
                apiLogging.error(result)
                return {'error': result}
        else:
            return {'response': {'info': '所有的keyword已經存在於詞庫中'}}
    def keywordPosition(self, content, keywords, inputParams=None):
        if (len(keywords) == 0):
            return {'error': {'keywords': 'keywords長度不得為0'}}
        if (len(content) == 0):
            return {'error': {'content': 'content長度不得為0'}}

        mode = 'index' ## default mode
        if (inputParams and 'mode' in inputParams):
            if (inputParams['mode'] == 'index'):
                mode = 'index'
                print('mode: ', mode)
            elif (inputParams['mode'] == 'percent'):
                mode = 'percent'
                print('mode: ', mode)
            else:
                return({'error': 'mode 只有 index, percent 兩種'})
                # print({'error': 'mode 只有 index, percent 兩種'})
        posDict = {}
        for keyword in keywords:
            if (len(keyword) == 0):
                continue

            posList = []
            pos = content.rfind(keyword)
            while (pos > 0):
                posList.append(pos)
                pos = content.rfind(keyword, 0, pos - 1)
            posList.sort()

            posDict[keyword] = posList


        if mode == 'index':
            return {'response': posDict}
        if mode == 'percent':
            contLen = len(content)
            prcDict = {}
            for keyword, posList in posDict:

                prcList = []
                for v in posList:
                    prcList.append("{:4.2f}".format(v/contLen*100))
                prcDict[keyword] = prcList
            return {'response': prcDict}

    def nlpTokenizer(self, content, inputParams=None):
        params = {
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            print(content)
            segments = []

            NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
            for v in NLPTokenizer.segment(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def urlTokenizer(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            sentence = []
            URLTokenizer = JClass('com.hankcs.hanlp.tokenizer.URLTokenizer')
            for v in URLTokenizer.segment(self._innerConvert(content, '2sc')):
                sentence.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': sentence}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}

    def notionalTokenizer(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            segments = []
            #去除停用词
            # print(NotionalTokenizer.segment(content))
            #去除停用词+斷句
            # print(NotionalTokenizer.seg2sentence(content))

            NotionalTokenizer = JClass('com.hankcs.hanlp.tokenizer.NotionalTokenizer')
            for v in NotionalTokenizer.segment(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def numberAndQuantifierRecognition(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            segments = []
            StandardTokenizer = JClass('com.hankcs.hanlp.tokenizer.StandardTokenizer')
            StandardTokenizer.SEGMENT.enableNumberQuantifierRecognize(True)
            for v in StandardTokenizer.segment(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def organizationRecognition(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            segments = []
            segemntTool = self.HanLP.newSegment().enableOrganizationRecognize(True)
            for v in segemntTool.seg(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def phraseExtractor(self, content, inputParams=None):
        params = {
            'convertMode': '2tw',
            'num': 10
        }
        if inputParams:
            params.update(inputParams)

        if 'num' not in params:
            return {'error': { 'num': '必須輸入 num，為keyword數量'}}

        if isinstance(content, str) and len(content)>0:
            segments = []
            for v in self.HanLP.extractPhrase(self._innerConvert(content, '2sc'), params['num']):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def placeRecognition(self, content, inputParams=None):
        params = {
            'enablePOSTagging': True,
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            self.generalSetting(params)
            segments = []
            segemntTool = self.HanLP.newSegment().enablePlaceRecognize(True)
            for v in segemntTool.seg(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def posTagging(self, content, inputParams=None):
        params = {
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            segments = []
            segemntTool = self.HanLP.newSegment().enablePartOfSpeechTagging(True)
            for v in segemntTool.seg(self._innerConvert(content, '2sc')):
                segments.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': segments}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}

    def rewrite(self, content, inputParams=None):
        params = {
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            CoreSynonymDictionary = JClass('com.hankcs.hanlp.dictionary.CoreSynonymDictionary')
            result = CoreSynonymDictionary.rewrite(self._innerConvert(content, '2sc'))
            return {'response': self._innerConvert(result, params['convertMode'])}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    '''
        def suggester(self, content, inputParams=None):
            mode = parser.parse_args()['mode']
            if isinstance(content, str) and len(content)>0:
                Suggester = JClass('com.hankcs.hanlp.suggest.Suggester')
                return {'response': suggester.suggest(content, mode)}
            else:
                return {'error': { 'content': '長度不得為零的字串'}}
    '''
    def summary(self, content, inputParams=None):
        params = {
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            sentence = []
            for v in self.HanLP.extractSummary(self._innerConvert(content, '2sc'), 3):
                sentence.append(self._innerConvert(str(v), params['convertMode']))
            return {'response': sentence}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}
    def wordDistance(self, compare, inputParams=None):
        params = {
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if not isinstance(compare, list) and len(compare) != 2:
            return {'error': { 'compare': '存放字串陣列 內含兩個要比對的字串, *必要欄位'}}

        CoreSynonymDictionary = JClass('com.hankcs.hanlp.dictionary.CoreSynonymDictionary')

        distance = CoreSynonymDictionary.distance(self._innerConvert(compare[0], '2sc'), self._innerConvert(compare[1], '2sc'))
        similarity = CoreSynonymDictionary.similarity(self._innerConvert(compare[0], '2sc'), self._innerConvert(compare[1], '2sc'))
        return {'response': {
            'compare': compare,
            'distance': distance,
            'similarity': similarity
            }
        }
    def wordOccurrence(self, content, inputParams=None):
        params = {
            'convertMode': '2tw'
        }
        if inputParams:
            params.update(inputParams)

        if isinstance(content, str) and len(content)>0:
            content = self._innerConvert(content, '2sc')
            Occurrence = JClass('com.hankcs.hanlp.corpus.occurrence.Occurrence')
            occurrence = Occurrence()
            occurrence.addAll(content)
            occurrence.compute()

            uniGramObj = {}
            uniGram = occurrence.getUniGram()
            for v in uniGram:
                key = self._innerConvert(v.getKey(), params['convertMode'])
                uniGramObj[key] = v.getValue().toString().replace(v.getKey()+'=', '')

            return {'response': uniGramObj}
        else:
            return {'error': { 'content': '長度不得為零的字串'}}


    def toTC(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.convertToTraditionalChinese(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def toSC(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.convertToSimplifiedChinese(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def tw2s(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.tw2s(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def s2tw(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.s2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def hk2s(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.hk2s(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def s2hk(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.s2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def hk2tw(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.hk2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def tw2hk(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.tw2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def t2tw(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.t2tw(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def t2hk(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.t2hk(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def tw2t(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.tw2t(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
    def hk2t(self, content):
        if isinstance(content, str) and len(content)>0:
            result = self.HanLP.hk2t(content)
            return {'response': result}
        else:
            return {'error': { 'content': '長度不得為零'}}
