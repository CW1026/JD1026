import time
import unittest
import requests
import json
from urllib import parse
from time import sleep


class GameTest(unittest.TestCase):
    def setUp(self):
        #211test环境
        self.url='http://172.16.16.211:16888'
        #233dev环境
        # self.url = 'http://172.16.16.233:9988'
        #妙啊环境
        # self.url='https://sport-live-test-api.kscyh.com'
        ##多账号任务

        headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'BundleIdentifier': 'user'
}
        login_body = 'area_code+86&username=13267192974&password=a123456'
        r_longin = requests.post(self.url+'/App/User_User/Login?', data=login_body, headers=headers)
        # print(r_longin.json())
        self.headers_token = { 'X-Token': r_longin.json()['result']['access_token'],
            'BundleIdentifier': 'user',
            'Content-Type': 'application/x-www-form-urlencoded'
                               }
        self.body=''
        self.today=time.strftime('%Y-%m-%d')


    ##获取游戏菜单
    def test_gameid(self):
        r = requests.post(self.url +'/App/App_GameMenu/GetGameMenu?id=0', data=self.body, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['result'][0]['category_name'], '体育菜单')
        sleep(0.5)
    #顶部输入框
    def test_game_input(self):
        data = {'keyword': '百家乐'}
        keyword = parse.urlencode(data).encode('utf-8')
        r = requests.post(self.url + '/App/App_GameMenu/Search', params=keyword, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['result'][0]['name'], '百家乐')

    #输入异常字符输入
    def test_gameinput_error(self):
        data = {'keyword': '%????'}
        keyword = parse.urlencode(data).encode('utf-8')
        r = requests.post(self.url + '/App/App_GameMenu/Search', params=keyword, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)

    #空字符串输入
    def test_gameinput_error(self):
        data = {'keyword': ''}
        keyword = parse.urlencode(data).encode('utf-8')
        r = requests.post(self.url + '/App/App_GameMenu/Search', params=keyword, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)

    ## 彩票菜单-一分乒乓彩
    def test_game_pingpang(self):
        r_pingpang = requests.get(self.url+'/App/Game_Game/GetTypeInfo?game_type=pingpang_1',
                                  data=self.body, headers=self.headers_token)
        result = r_pingpang.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

    # 一分乒乓彩投注
    def test_game_pingpangorder(self):
        r_pingpang = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=pingpang_1',
                                  data=self.body, headers=self.headers_token)
        qihao = r_pingpang.json()['result']['current_round']['number']

        pingpang_body = {'live_room_id': 0,
                         "game_type": "pingpang_1",
                         "game_sub": "tou3wei;",
                         "game_number": qihao,
                         "detail": "tou3wei_da:2;tou3wei_xiao:2;",
                         "multiple": 1}
        r = requests.post(self.url + '/App/Game_Order/Create', data=pingpang_body, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

     # 错误投注
    def test_game_pingpangorder_error(self):
        pingpang_body = {'live_room_id': 0,
                         "game_type": "pingpang_1",
                         "game_sub": "tou3wei;",
                         "game_number": 202111160671,
                         "detail": "tou3wei_da:2;tou3wei_xiao:2;",
                         "multiple": 1}
        r = requests.post(self.url + '/App/Game_Order/Create', data=pingpang_body, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 1)
        sleep(1)

    #投注记录
    def test_game_pingpangjl(self):
        r =requests.get(self.url+'/App/Game_Order/GetBetList?status=0&page=1&date='+str(self.today),
                        data=self.body, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #历史开奖
    def test_game_pingpangls(self):
        r = requests.get(self.url+'/App/Game_Game/HistoryDrawList?game_type=pingpang_1&page=1',
                         data=self.body, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #玩法规则
    def test_game_pingpangwf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=pingpang_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    ##百家乐
    def test_game_baijiale(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=baijiale_1',
                         data=self.body, headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    ##百家乐投注
    def test_game_1baijialeorder(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=baijiale_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        body = {'live_room_id': 0,
                "game_type": "baijiale_1",
                "game_sub": "daxiao;",
                "game_number": qh,
                "detail": "daxiao_da:2;daxiao_xiao:2;",
                "multiple": 1}
        baijialeorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = baijialeorder.json()
        self.assertNotEqual(result['code'], 2)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)
    #百家乐异常投注
    def test_game_2baijialeordererror(self):
        body = {'live_room_id': 0,
                "game_type": "baijiale_1",
                "game_sub": "daxiao;",
                "game_number": 202111160913,
                "detail": "daxiao_da:2;daxiao_xiao:2;",
                "multiple": 1}
        baijialeorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = baijialeorder.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

    # 历史开奖
    def test_game_baijialels(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=baijiale_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #玩法规则
    def test_game_baijialewf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=baijiale_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    ##一分快三
    def test_game_kuaisanle(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=kuaisan_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分快三投注
    def test_game_kuaisander(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=kuaisan_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        body = {'live_room_id': 0,
                "game_type": "kuaisan_1",
                "game_sub": "zonghe;",
                "game_number": qh,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        kuaisanorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = kuaisanorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_kuaisanerror(self):
        body = {'live_room_id': 0,
                "game_type": "kuaisan_1",
                "game_sub": "zonghe;",
                "game_number": 202111160927,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        kuaisan = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = kuaisan.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

    #历史开奖
    def test_game_kuaisanls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=kuaisan_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #玩法规则
    def test_game_kuaisanwf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=kuaisan_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    ##一分六合彩
    def test_game_liuhecai(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=liuhecai_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #六合彩投注
    def test_game_liuhecai1order(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=liuhecai_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        body = {'live_room_id': 0,
                "game_type": "liuhecai_1",
                "game_sub": "temaliangmian;",
                "game_number": qh,
                "detail": "temaliangmian_da:2;temaliangmian_xiao:2;",
                "multiple": 1}
        liuhecaiorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = liuhecaiorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_liuhecai2error(self):
        body = {'live_room_id': 0,
                "game_type": "liuhecai_1",
                "game_sub": "temaliangmian;",
                "game_number": 202111160955,
                "detail": "temaliangmian_da:2;temaliangmian_xiao:2;",
                "multiple": 1}
        liuhecai = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = liuhecai.json()
        self.assertEqual(result['code'], 1)
        sleep(1)

    #历史开奖
    def test_game_liuhecails(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=liuhecai_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #玩法规则
    def test_game_liuhecaiwf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=liuhecai_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分时时彩
    def test_game_shishicai(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=shishicai_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #投注记录
    def test_game_shishicai1order(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=shishicai_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "shishicai_1",
                "game_sub": "diyiqiuliangmian;",
                "game_number": qh,
                "detail": "diyiqiuliangmian_da:2;diyiqiuliangmian_xiao:2;",
                "multiple": 1}
        shishicaiorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = shishicaiorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        # print(shishicaiorder.json())
        sleep(1)

    #时时彩投注
    def test_game_shishicai2error(self):
        body = {'live_room_id': 0,
                "game_type": "shishicai_1",
                "game_sub": "diyiqiuliangmian;",
                "game_number": 202111161017,
                "detail": "diyiqiuliangmian_da:2;diyiqiuliangmian_xiao:2;",
                "multiple": 1}
        shishicai = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = shishicai.json()
        self.assertEqual(result['code'], 1)
        sleep(1)

    #历史开奖
    def test_game_shishicails(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=shishicai_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #玩法规则
    def test_game_shishicaiwf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=shishicai_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分赛车
    def test_game_saiche(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=saiche_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

    #一分赛车投注
    def test_game_saiche1order(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=saiche_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "saiche_1",
                "game_sub": "guanjunliangmian;",
                "game_number": qh,
                "detail": "guanjunliangmian_da:2;guanjunliangmian_xiao:2;",
                "multiple": 1}
        saicheorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = saicheorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_saiche2error(self):
        body = {'live_room_id': 0,
                "game_type": "saiche_1",
                "game_sub": "guanjunliangmian;",
                "game_number": 202111161185,
                "detail": "guanjunliangmian_da:2;guanjunliangmian_xiao:2;",
                "multiple": 1}
        saiche = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = saiche.json()
        self.assertEqual(result['code'], 1)
        sleep(1)
    #历史开奖
    def test_game_saichels(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=saiche_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #玩法规则
    def test_game_saichewf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=saiche_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

    #一分11选5
    def test_game_shiyixuanwu(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=shiyixuanwu_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 一分11选5投注
    def test_game_shiyixuanwu1order(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=shiyixuanwu_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "shiyixuanwu_1",
                "game_sub": "diyiqiuliangmian;",
                "game_number": qh,
                "detail": "diyiqiuliangmian_da:2;diyiqiuliangmian_xiao:2;",
                "multiple": 1}
        shiyixuanwuorder = requests.post(self.url + '/App/Game_Order/Create',
                                         data=body, headers=self.headers_token)
        result = shiyixuanwuorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    # 异常投注
    def test_game_shiyixuanwu2error(self):
        body = {'live_room_id': 0,
                "game_type": "shiyixuanwu_1",
                "game_sub": "diyiqiuliangmian;",
                "game_number": 202111161192,
                "detail": "diyiqiuliangmian_da:2;diyiqiuliangmian_xiao:2;",
                "multiple": 1}
        shiyixuanwu = requests.post(self.url + '/App/Game_Order/Create',
                                    data=body, headers=self.headers_token)
        result = shiyixuanwu.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

    # 历史开奖
    def test_game_shiyixuanwuls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=shiyixuanwu_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 玩法规则
    def test_game_shiyixuanwuwf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=shiyixuanwu_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分鱼虾蟹
    def test_game_yuxiaxie(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=yuxiaxie_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 一分鱼虾蟹投注
    def test_game_1yuxiaxieorder(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=yuxiaxie_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "yuxiaxie_1",
                "game_sub": "sanjun;",
                "game_number": qh,
                "detail": "sanjun_1:2;sanjun_2:2;",
                "multiple": 1}
        yuxiaxieorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = yuxiaxieorder.json()
        self.assertNotEqual(result['code'], 400)
        self.assertEqual(result['msg'], 'ok')
        sleep(2)

    #异常投注
    def test_game_2yuxiaxieerror(self):
        body = {'live_room_id': 0,
                "game_type": "yuxiaxie_1",
                "game_sub": "sanjun;",
                "game_number": 202111161201,
                "detail": "sanjun_1:2;sanjun_2:2;",
                "multiple": 1}
        yuxiaxie = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = yuxiaxie.json()
        self.assertEqual(result['code'], 1)
        sleep(2)
    # 历史开奖
    def test_game_yuxiaxiels(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=yuxiaxie_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 玩法规则
    def test_game_yuxiaxiewf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=yuxiaxie_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分骰宝
    def test_game_toubao(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=toubao_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 一分骰宝投注
    def test_game_toubao1order(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=toubao_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "toubao_1",
                "game_sub": "zonghe;",
                "game_number": qh,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        toubaoorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = toubaoorder.json()
        self.assertNotEqual(result['code'], 400)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_toubao2error(self):
        body = {'live_room_id': 0,
                "game_type": "toubao_1",
                "game_sub": "zonghe;",
                "game_number": 202111161205,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        toubao = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = toubao.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

    # 历史开奖
    def test_game_toubaols(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=toubao_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

     # 玩法规则
    def test_game_toubaowf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=toubao_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分骰宝
    def test_game_toubao(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=toubao_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 投注记录
        # 历史开奖
    def test_game_toubaols(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=toubao_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_toubaowf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=toubao_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分三球
    def test_game_sanqiu(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=sanqiu_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 一分三球投注
    def test_game_sanqiu1order(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=sanqiu_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "sanqiu_1",
                "game_sub": "zonghe;",
                "game_number": qh,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        sanqiuorder = requests.post(self.url + '/App/Game_Order/Create',
                                    data=body, headers=self.headers_token)
        result = sanqiuorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    # 异常投注
    def test_game_sanqiu2error(self):
        body = {'live_room_id': 0,
                "game_type": "sanqiu_1",
                "game_sub": "zonghe;",
                "game_number": 202111161211,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        sanqiu = requests.post(self.url + '/App/Game_Order/Create',
                               data=body, headers=self.headers_token)
        result = sanqiu.json()
        self.assertEqual(result['code'], 1)
        sleep(2)
        # 历史开奖
    def test_game_sanqiuls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=sanqiu_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

        # 玩法规则
    def test_game_sanqiuwf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=sanqiu_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

    #三分SONIC4D
    def test_game_sonic4d_3(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=sonic4d_3', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 三分SONIC4D投注
    def test_game_1sonic4dorder(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=sonic4d_3',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "sonic4d_3",
                "game_sub": "disiqiuliangmian;",
                "game_number": qh,
                "detail": "disiqiuliangmian_da:2;disiqiuliangmian_xiao:2;",
                "multiple": 1}
        sonic4d_3order = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = sonic4d_3order.json()
        self.assertNotEqual(result['code'], 2)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_2sonic4derror(self):
        body = {'live_room_id': 0,
                "game_type": "sonic4d_3",
                "game_sub": "disiqiuliangmian;",
                "game_number": 202111170207,
                "detail": "disiqiuliangmian_da:2;disiqiuliangmian_xiao:2;",
                "multiple": 1}
        sonic4d = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = sonic4d.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

        # 历史开奖
    def test_game_sonic4d_3ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=sonic4d_3&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_sonic4d_3wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=sonic4d_3', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

    #一分河内
    def test_game_henei_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=henei_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 一分河内投注
    def test_game_1heneidorder(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=henei_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "henei_1",
                "game_sub": "weishu2wei;",
                "game_number": qh,
                "detail": "weishu2wei-all@01:2;",
                "multiple": 1}
        heneiorder = requests.post(self.url + '/App/Game_Order/Create',
                                   data=body, headers=self.headers_token)
        result = heneiorder.json()
        self.assertNotEqual(result['code'], 2)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    # 异常投注
    def test_game_2heneiderror(self):
        body = {'live_room_id': 0,
                "game_type": "henei_1",
                "game_sub": "weishu2wei;",
                "game_number": 202111170625,
                "detail": "weishu2wei-all@01:2;",
                "multiple": 1}
        henei = requests.post(self.url + '/App/Game_Order/Create',
                              data=body, headers=self.headers_token)
        result = henei.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

        # 历史开奖
    def test_game_henei_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=henei_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_henei_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=henei_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

    #一分toto36
    def test_game_toto36_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=toto36_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 一分toto36投注
    def test_game_1toto36order(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=toto36_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "toto36_1",
                "game_sub": "liangmian;",
                "game_number": qh,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        toto36order = requests.post(self.url + '/App/Game_Order/Create',
                                    data=body, headers=self.headers_token)
        result = toto36order.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    # 异常投注
    def test_game_2toto36error(self):
        body = {'live_room_id': 0,
                "game_type": "toto36_1",
                "game_sub": "liangmian;",
                "game_number": 202111170635,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        toto36 = requests.post(self.url + '/App/Game_Order/Create',
                               data=body, headers=self.headers_token)
        result = toto36.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

        # 历史开奖
    def test_game_toto36_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=toto36_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

        # 玩法规则
    def test_game_toto36_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=toto36_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分M12
    def test_game_m12_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=m12_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 一分M12投注
    def test_game_1m12order(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=m12_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "m12_1",
                "game_sub": "liangmian;",
                "game_number": qh,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        m12order = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = m12order.json()
        self.assertNotEqual(result['code'], 2)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_2m12error(self):
        body = {'live_room_id': 0,
                "game_type": "m12_1",
                "game_sub": "liangmian;",
                "game_number": 202111170677,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        m12 = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = m12.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

        # 历史开奖
    def test_game_m12_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=m12_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_m12_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=m12_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #WIN24
    def test_game_w24_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=w24_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # WIN24投注
    def test_game_1w24order(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=w24_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "w24_1",
                "game_sub": "liangmian;",
                "game_number": qh,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        w24order = requests.post(self.url + '/App/Game_Order/Create',
                                 data=body, headers=self.headers_token)
        result = w24order.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    # 异常投注
    def test_game_2w24error(self):
        body = {'live_room_id': 0,
                "game_type": "w24_1",
                "game_sub": "liangmian;",
                "game_number": 202111170641,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        w24 = requests.post(self.url + '/App/Game_Order/Create',
                            data=body, headers=self.headers_token)
        result = w24.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

        # 历史开奖
    def test_game_w24_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=w24_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_w24_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=w24_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #live48
    def test_game_live48_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=live48_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # live48投注
    def test_game_1live48order(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=live48_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "live48_1",
                "game_sub": "liangmian;",
                "game_number": qh,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        live48order = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = live48order.json()
        self.assertNotEqual(result['code'], 2)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_2live48error(self):
        body = {'live_room_id': 0,
                "game_type": "live48_1",
                "game_sub": "liangmian;",
                "game_number": 202111170685,
                "detail": "liangmian_da:2;liangmian_xiao:2;",
                "multiple": 1}
        live48 = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = live48.json()
        self.assertEqual(result['code'], 1)
        sleep(2)
        # 历史开奖
    def test_game_live48_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=live48_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_live48_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=live48_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分色碟
    def test_game_sedie_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=sedie_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    # 一分色碟投注
    def test_game_1sedieorder(self):
        r = requests.get(self.url +'/App/Game_Game/GetTypeInfo?game_type=sedie_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "sedie_1",
                "game_sub": "zonghe;",
                "game_number": qh,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        sedieorder = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = sedieorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    #异常投注
    def test_game_2sedieerror(self):
        body = {'live_room_id': 0,
                "game_type": "sedie_1",
                "game_sub": "zonghe;",
                "game_number": 202111170692,
                "detail": "zonghe_da:2;zonghe_xiao:2;",
                "multiple": 1}
        sedie = requests.post(self.url + '/App/Game_Order/Create',
                                      data=body, headers=self.headers_token)
        result = sedie.json()
        self.assertEqual(result['code'], 1)
        sleep(2)
        # 历史开奖
    def test_game_sedie_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=sedie_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_sedie_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=sedie_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分红绿
    def test_game_honglv_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=honglv_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 一分红绿投注
        def test_game_1honglvorder(self):
            r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=honglv_1',
                             data=self.body, headers=self.headers_token)
            qh = r.json()['result']['current_round']['number']
            # print(qh)
            body = {'live_room_id': 0,
                    "game_type": "honglv_1",
                    "game_sub": "sebo;",
                    "game_number": qh,
                    "detail": "sebo_hong:2;sebo_lv:2;sebo_zi:2;",
                    "multiple": 1}
            honglvorder = requests.post(self.url + '/App/Game_Order/Create',
                                        data=body, headers=self.headers_token)
            result = honglvorder.json()
            self.assertEqual(result['code'], 0)
            self.assertEqual(result['msg'], 'ok')
            sleep(1)

        # 异常投注
        def test_game_2honglverror(self):
            body = {'live_room_id': 0,
                    "game_type": "honglv_1",
                    "game_sub": "sebo;",
                    "game_number": 202111170899,
                    "detail": "sebo_hong:2;sebo_lv:2;sebo_zi:2;",
                    "multiple": 1}
            honglv = requests.post(self.url + '/App/Game_Order/Create',
                                   data=body, headers=self.headers_token)
            result = honglv.json()
            self.assertEqual(result['code'], 1)
            sleep(2)
        # 历史开奖
    def test_game_honglv_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=honglv_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_honglv_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=honglv_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #一分印度红绿
    def test_game_ydhonglvparity_1(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=ydhonglvparity_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(1)

    # 一分印度红绿投注
    def test_game_1ydhonglvparityorder(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=ydhonglvparity_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "ydhonglvparity_1",
                "game_sub": "ydsebo;",
                "game_number": qh,
                "detail": "ydsebo_lv:2;ydsebo_zi:2;ydsebo_hong:2;",
                "multiple": 1}
        ydhonglvparityorder = requests.post(self.url + '/App/Game_Order/Create',
                                            data=body, headers=self.headers_token)
        result = ydhonglvparityorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

    # 异常投注
    def test_game_2ydhonglvparityerror(self):
        body = {'live_room_id': 0,
                "game_type": "ydhonglvparity_1",
                "game_sub": "ydsebo;",
                "game_number": 202111170899,
                "detail": "ydsebo_lv:2;ydsebo_zi:2;ydsebo_hong:2;",
                "multiple": 1}
        ydhonglvparity = requests.post(self.url + '/App/Game_Order/Create',
                                       data=body, headers=self.headers_token)
        result = ydhonglvparity.json()
        self.assertEqual(result['code'], 1)
        sleep(2)

    # 历史开奖
    def test_game_ydhonglvparity_1ls(self):
        r = requests.get(self.url + '/App/Game_Game/HistoryDrawList?game_type=ydhonglvparity_1&page=1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

        # 玩法规则
    def test_game_ydhonglvparity_1wf(self):
        r = requests.get(self.url + '/App/Game_Game/GetExplain?game_type=ydhonglvparity_1', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

     #一分泰国国家彩投注
    def test_game_1taiorder(self):
        r = requests.get(self.url + '/App/Game_Game/GetTypeInfo?game_type=tai_1',
                         data=self.body, headers=self.headers_token)
        qh = r.json()['result']['current_round']['number']
        # print(qh)
        body = {'live_room_id': 0,
                "game_type": "tai_1",
                "game_sub": "yidengjiang;",
                "game_number": qh,
                "detail": "yidengjiang_da:2;yidengjiang_xiao:2;",
                "multiple": 1}
        taiorder = requests.post(self.url + '/App/Game_Order/Create',
                                 data=body, headers=self.headers_token)
        result = taiorder.json()
        self.assertEqual(result['code'], 0)
        self.assertEqual(result['msg'], 'ok')
        sleep(1)

        # 异常投注

    def test_game_2taierror(self):
        body = {'live_room_id': 0,
                "game_type": "tai_1",
                "game_sub": "yidengjiang;",
                "game_number": 202111240950,
                "detail": "yidengjiang_da:2;yidengjiang_xiao:2;",
                "multiple": 1}
        tai = requests.post(self.url + '/App/Game_Order/Create',
                            data=body, headers=self.headers_token)
        result = tai.json()
        self.assertEqual(result['code'], 1)
        sleep(2)







        ###体育菜单
    #足球
    def test_game_football(self):
        r = requests.get(self.url +'/App/Sport_Matches/LeagueList?sport_type=1&match_type=1&name=', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)

    #篮球
    def test_game_basketball(self):
        r = requests.get(self.url +'/App/Sport_Matches/LeagueList?sport_type=2&match_type=1&name=', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #网球
    def test_game_tennis(self):
        r = requests.get(self.url + '/App/Sport_Matches/LeagueList?sport_type=3&match_type=1&name=', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)
    #电竞
    def test_game_dianjing(self):
        r = requests.get(self.url + '/App/Sport_Matches/LeagueList?sport_type=4&match_type=1&name=', data=self.body,
                         headers=self.headers_token)
        result = r.json()
        self.assertEqual(result['code'], 0)
        sleep(0.5)



if __name__ == '__main__':
    unittest.main()