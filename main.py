print('ArknightsCheater:启动mitmproxy成功，请按帮助内操作继续。')
import mitmproxy.http
from mitmproxy import http
import json, random

entryGame = True
isInit = False
isFCM = True
userData = json.loads(open('./data.acdata', 'r', encoding='UTF-8').read())
isInit = userData['init']
isFCM = userData['fcm']
userIsMinors = False
totalChars = 0
servers = ["ak-gs-gf.hypergryph.com", "as.hypergryph.com", "ak-fs.hypergryph.com"
           "as.arknights.jp", "gs.arknights.jp", "as.arknights.global", "gs.arknights.global",
           "ak-conf.hypergryph.com", "ak-conf.arknights.jp", "ak-conf.arknights.global"]

class Cheat:

    def request(self, flow):

        if not isInit:
            if flow.request.host in servers and flow.request.path.startswith("/quest/battleStart"):

                data = flow.request.get_content()
                print('ArknightsCheater:战斗开始 >>>\n')
                j = json.loads(data)
                if not j['squad']==None:
                    j['squad']['slots']=userData['squads'][str(j['squad']['squadId'])]['slots']
                flow.request.set_content(json.dumps(j).encode())

            if flow.request.host in servers and flow.request.path.startswith("/campaign/battleStart"):

                data = flow.request.get_content()
                print('ArknightsCheater:龙门战斗开始 >>>\n')
                j = json.loads(data)
                if not j['squad']==None:
                    j['squad']['slots']=userData['squads'][str(j['squad']['squadId'])]['slots']
                flow.request.set_content(json.dumps(j).encode())

            if flow.request.host in servers and flow.request.path.startswith("/crisis/battleStart"):

                data = flow.request.get_content()
                print('ArknightsCheater:危机合同战斗开始 >>>\n')
                j = json.loads(data)
                if not j['squad']==None:
                    j['squad']['slots']=userData['squads'][str(j['squad']['squadId'])]['slots']
                flow.request.set_content(json.dumps(j).encode())

            if flow.request.host in servers and flow.request.path.startswith("/quest/squadFormation"):

                data = flow.request.get_content()
                j = json.loads(data)
                j['slots'] = userData['squads'][str(j['squadId'])]['slots']
                flow.request.set_content(json.dumps(j).encode())

            if flow.request.host not in servers:

                flow.response = http.HTTPResponse.make(404)

    def response(self, flow: mitmproxy.http.HTTPFlow):

        global entryGame,userIsMinors

        if isInit:

            if flow.request.host in servers and flow.request.path.startswith("/account/syncData"):

                j = json.loads(flow.response.get_text())
                # 区分国服外服
                if 'androidDiamond' in j['user']['status'] or 'iosDiamond' in j['user']['status']:
                    androidDiamond=j['user']['status']['androidDiamond']
                    iosDiamond=j['user']['status']['iosDiamond']
                else:
                    tdiamond=j['user']['status']['payDiamond']+j['user']['status']['freeDiamond']
                    androidDiamond=tdiamond
                    iosDiamond=tdiamond
                item=[{
                    'gold': j['user']['status']['gold'],
                    'diamondShard': j['user']['status']['diamondShard'],
                    'androidDiamond': androidDiamond,
                    'iosDiamond': iosDiamond,
                    'practiceTicket': j['user']['status']['practiceTicket'],
                    'lggShard': j['user']['status']['lggShard'],
                    'hggShard': j['user']['status']['hggShard'],
                    'gachaTicket': j['user']['status']['gachaTicket'],
                    'tenGachaTicket': j['user']['status']['tenGachaTicket']
                }]
                data=[{
                    'userIsMinors':str(userIsMinors).lower(),
                    'uid': j['user']['status']['uid'],
                    'nickName': j['user']['status']['nickName'],
                    'nickNumber': j['user']['status']['nickNumber'],
                    'level': j['user']['status']['level'],
                    'ap': j['user']['status']['ap'],
                    'maxAp': j['user']['status']['maxAp'],
                    'resume': 'Ta什么都没有留下',
                    'secretary':j['user']['status']['secretary'],
                    'secretarySkinId':j['user']['status']['secretarySkinId'],
                    'item':item[0],
                    'chars':j['user']['troop']['chars'],
                    'squads':j['user']['troop']['squads']
                }]
                f=open('.\datafromgame.acdata', 'w', encoding='UTF-8')
                f.write(str(data).replace('{\'"','{"').replace('}\'}','}}').replace('\'','"').replace('""','').replace('None','null')[1:-1])
                f.close
                print('initFinished')

        if flow.request.url.startswith("https://ak-fs.hypergryph.com/announce/Android/preannouncement.meta.json") or flow.request.url.startswith("https://ak-fs.hypergryph.com/announce/IOS/preannouncement.meta.json"):

            entryGame=True

        if flow.request.url.startswith("https://as.hypergryph.com/online/v1/ping") and isFCM:

            j=json.loads(flow.response.get_text())
            if 'timeLeft' in j:
                if not j['timeLeft']==-1:
                    userIsMinors=True
            if entryGame:
                flow.response.set_text('{"result":0,"message":"OK","interval":5400,"timeLeft":-1,"alertTime":600}')
                entryGame=False
            else:
                flow.response = http.HTTPResponse.make(404)
            print('')
            if j['message'][:6]=='您已达到本日':
                userIsMinors=True
                print('ArknightsCheater-防沉迷破解: 您已达到本日在线时长上限或不在可游戏时间范围内，破解后仍可以继续游戏，但请合理安排游戏时间。')
            else:
                s = j['timeLeft']
                h = int(s/3600)
                m = int((s-h*3600)/60)
                ss = int(s-h*3600-m*60)
                print('ArknightsCheater-防沉迷破解: 游戏剩余时间 '+str(h)+'小时'+str(m)+'分钟' + str(ss)+'秒 修改为 不限制，但请合理安排游戏时间。')
            print('')

        if flow.request.host in servers and flow.request.path.startswith("/account/syncStatus") and not isInit:

            j=json.loads(flow.response.get_text())
            j['playerDataDelta']['modified']['status']['resume']=userData['resume']
            flow.response.set_text(json.dumps(j))

        if flow.request.host in servers and flow.request.path.startswith("/account/syncData") and not isInit:

            global totalChars
            j = json.loads(flow.response.get_text())
            print('')
            print('ArknightsCheater:' + j['user']['status']['nickName'] + '#' + flow.request.headers['uid'] + ' 初始化...')
            j['user']['status']['uid']=str(userData['uid'])
            j['user']['status']['nickName']=userData['nickName']
            j['user']['status']['nickNumber']=str(userData['nickNumber'])
            j['user']['status']['level']=userData['level']
            j['user']['status']['ap']=userData['ap']
            j['user']['status']['maxAp']=userData['maxAp']
            j['user']['status']['secretary']=userData['secretary']
            j['user']['status']['secretarySkinId']=userData['secretarySkinId']
            j['user']['status']['gold']=userData['item']['gold']
            j['user']['status']['diamondShard']=userData['item']['diamondShard']

            if 'androidDiamond' in j['user']['status'] or 'iosDiamond' in j['user']['status']:
                j['user']['status']['androidDiamond']=userData['item']['androidDiamond']
                j['user']['status']['iosDiamond']=userData['item']['iosDiamond']
            else:
                j['user']['status']['payDiamond']=userData['item']['iosDiamond'] if userData['item']['androidDiamond']<=userData['item']['iosDiamond'] else userData['item']['androidDiamond']

            j['user']['status']['practiceTicket']=userData['item']['practiceTicket']
            j['user']['status']['lggShard']=userData['item']['lggShard']
            j['user']['status']['hggShard']=userData['item']['hggShard']
            j['user']['status']['gachaTicket']=userData['item']['gachaTicket']
            j['user']['status']['tenGachaTicket']=userData['item']['tenGachaTicket']
            j['user']['troop']['chars']=userData['chars']
            totalChars = len(j['user']['troop']['chars'])
            print('ArknightsCheater:载入成功，共%s个干员' % str(totalChars))
            print('')
            flow.response.set_text(json.dumps(j))

        if flow.request.host in servers and flow.request.path.startswith("/quest/squadFormation") and not isInit:

            text = flow.response.get_text()
            print('ArknightsCheater:设置编队 >>>\n')
            j = json.loads(text)
            squadId=json.loads(flow.request.get_text())['squadId']
            j['playerDataDelta']['modified']['troop']['squads'][squadId]['slots'] = userData['squads'][squadId]['slots']
            flow.response.set_text(json.dumps(j))


        if flow.request.host in servers and flow.request.path.startswith("/gacha/tenAdvancedGacha") and not isInit:

            gacha = gachaSimulation()
            flow.response = http.HTTPResponse.make(200, gacha.gachaTen(),
                                                   {"Content-Type": "application/json"})

        if flow.request.host in servers and flow.request.path.startswith("/gacha/advancedGacha") and not isInit:

            gacha = gachaSimulation()
            flow.response = http.HTTPResponse.make(200, gacha.gachaOne(),
                                                   {"Content-Type": "application/json"})

        if flow.request.host in servers:

            j = json.loads(flow.response.get_text())
            if 'error' in j and 'code'in j:
                print('error-code:'+json.dumps(j))

        if flow.request.host not in servers:

            flow.response = http.HTTPResponse.make(404)

class gachaSimulation:
    # 模拟抽卡，代码源(fu)于(zhi) LXG-Shadow/Arknights-Dolos

    def __init__(self, baodi=True):
        self.poolData = json.loads(open('./pool_table.json', 'r', encoding='UTF-8').read())
        self.rarityList = []
        self.gachaList = {}
        self.upChar = {"char_103_angel"}  # 以 上 干 员 获 得 概 率 提 升
        self.updateInfo()
        self.count = 0
        self.baodi = baodi  # 保 底

    def setUp(self,*args):
        self.upChar = set(args)
        self.updateInfo()

    def addUp(self,*args):
        for arg in args:
            self.upChar.add(arg)
        self.updateInfo()

    def updateInfo(self):
        self.rarityList = [str(x["rarityRank"]) for x in self.poolData["poolInfo"] for i in range(int(x["totalPercent"]*100))]
        random.shuffle(self.rarityList)
        self.upnormalList = {}
        for x in self.poolData["poolInfo"]:
            rarity = str(x["rarityRank"])
            self.upnormalList[rarity] = ["up" for i in range(int(x["upPercent"]*100))]+["normal" for i in range(100-int(x["upPercent"]*100))]
            self.gachaList[rarity] = {}
            self.gachaList[rarity]["normal"] = list(set(x["charIdList"]).difference(self.upChar))
            self.gachaList[rarity]["up"] = list(set(x["charIdList"]).intersection(self.upChar))
            if len(self.gachaList[rarity]["normal"]) == 0:
                self.gachaList[rarity]["normal"] = x["charIdList"]
            if len(self.gachaList[rarity]["up"]) == 0:
                self.gachaList[rarity]["up"] = x["charIdList"]

    def updateRarityList(self):
        for i in range(len(self.rarityList)):
            if self.rarityList[i] != "5":
                self.rarityList[i] = "5"
                return

    def getCharData(self,charId):
        if "chars" in userData and len(userData["chars"]) > 0:
            for instId in userData["chars"]:
                if userData["chars"][instId]["charId"] == charId:
                    return instId
        return -1

    def getOne(self):
        self.count += 1
        if self.baodi and self.count > 50:
            for i in range(2):
                self.updateRarityList()
        rarity = random.choice(self.rarityList)
        if rarity == "5":
            self.count = 0
            self.updateInfo()
        pl = random.choice(self.upnormalList[rarity])
        return (random.choice(self.gachaList[rarity][pl]), rarity)

    def getTen(self):
        return [self.getOne() for x in range(10)]

    def gachaTen(self):
        global totalChars
        respData = {"gachaResultList": [], "playerDataDelta": {"deleted": {}, "modified": {}}, "result": 0}
        print('ArknightsCheater-模拟抽卡: 十连 >>>\n')
        charlist = self.getTen()
        instIdList = []  # 避免重复
        for charId, rarity in charlist:
            gacha = {}
            gacha["isNew"] = 1
            gacha["charId"] = charId
            # 是否拥有该角色
            instId = int(self.getCharData(charId))
            if instId == -1:
                # 避免出现多个未拥有的干员
                while (instId not in instIdList):
                    instId = instId + 1
                instIdList.append(instId)
                gacha["charInstId"] = instId
                gacha["itemGet"] = {}
            else:
                gacha["isNew"] = 0
                gacha["charInstId"] = int(instId)
                if rarity == "5":
                    gacha["itemGet"] = [
                        {
                            "count": 15,
                            "id": "4004",
                            "type": "HGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_" + charId,
                            "type": "MATERIAL"
                        }
                    ]
                if rarity == "4":
                    gacha["itemGet"] = [
                        {
                            "count": 8,
                            "id": "4004",
                            "type": "HGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_" + charId,
                            "type": "MATERIAL"
                        }
                    ]
                if rarity == "3":
                    gacha["itemGet"] = [
                        {
                            "count": 30,
                            "id": "4005",
                            "type": "LGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_" + charId,
                            "type": "MATERIAL"
                        }
                    ]
                if rarity == "2":
                    gacha["itemGet"] = [
                        {
                            "count": 5,
                            "id": "4005",
                            "type": "LGG_SHD"
                        },
                        {
                            "count": 1,
                            "id": "p_" + charId,
                            "type": "MATERIAL"
                        }
                    ]
            respData["gachaResultList"].append(gacha)
        return json.dumps(respData)

    def gachaOne(self):
        global totalChars
        respData = {"charGet": {}, "playerDataDelta": {"deleted": {}, "modified": {}}, "result": 0}
        print('ArknightsCheater-模拟抽卡: 单抽 >>>\n')
        charId, rarity = self.getOne()
        gacha = {}
        gacha["isNew"] = 1
        gacha["charId"] = charId
        # 是否拥有该角色
        instId = int(self.getCharData(charId))
        if instId == -1:
            gacha["charInstId"] = totalChars + 1
            gacha["itemGet"] = {}
        else:
            gacha["isNew"] = 0
            gacha["charInstId"] = int(instId)
            if rarity == "5":
                gacha["itemGet"] = [
                    {
                        "count": 15,
                        "id": "4004",
                        "type": "HGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]
            if rarity == "4":
                gacha["itemGet"] = [
                    {
                        "count": 8,
                        "id": "4004",
                        "type": "HGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]
            if rarity == "3":
                gacha["itemGet"] = [
                    {
                        "count": 30,
                        "id": "4005",
                        "type": "LGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]
            if rarity == "2":
                gacha["itemGet"] = [
                    {
                        "count": 5,
                        "id": "4005",
                        "type": "LGG_SHD"
                    },
                    {
                        "count": 1,
                        "id": "p_" + charId,
                        "type": "MATERIAL"
                    }
                ]

        respData["charGet"] = gacha
        return json.dumps(respData)

addons = [
    Cheat()
]