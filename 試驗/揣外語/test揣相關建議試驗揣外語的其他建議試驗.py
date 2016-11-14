# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import resolve
from django.test import TestCase
from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.資料模型 import 來源表


class 揣外語的其他建議試驗(TestCase):

    def setUp(self):
        self.鄉民 = 來源表. 加來源({"名": '鄉民', '出世年': '1950', '出世地': '臺灣', })

    def test_揣無(self):
        # 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [])

    def test_無文本當做揣無(self):
        self.資料庫加外語('水母')
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [])

    def test_文本無建議用字當做揣無(self):
        水母編號 = self.資料庫加外語('水母')
        平臺項目表.外語翻母語(水母編號, {
            '文本資料': '水母',
        })
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [])

    def test_文本有建議用字就揣會著(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [
            {
                '文本資料': '䖳',
                '音標資料': '',
            }
        ])

    def test_文本有閣校對過就揣會著(self):
        漂亮編號 = self.資料庫加外語('漂亮')
        文本 = 平臺項目表.外語翻母語(漂亮編號, {
            '文本資料': '3',
        })
        新文本 = 平臺項目表._校對母語文本(文本.編號(), {
            '文本資料': '媠',
            '屬性': {'音標': 'sui2'}
        })
        新文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '漂'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'], [{
            '文本資料': '媠',
            '音標資料': 'sui2',
        }])

    def test_文本有兩組建議用字(self):
        水母編號 = self.資料庫加外語('水母')
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        文本.設為推薦用字()
        文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '水母',
        })
        文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['其他建議']), 2)

    def test_其他建議愛有相關(self):
        水母編號 = self.資料庫加外語('水母')
        水母腦編號 = self.資料庫加外語('水母腦')
        水母國編號 = self.資料庫加外語('水母國')
        握手編號 = self.資料庫加外語('握手')
        for 編號 in [水母編號, 水母腦編號, 水母國編號, 握手編號]:
            self.外語有建議的文本(編號)
# 		前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
# 		前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(len(回應資料['其他建議']), 2)

    def test_先加入就排頭前(self):
        水母編號 = self.資料庫加外語('水母')
        䖳文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '䖳',
        })
        䖳文本.設為推薦用字()
        水母文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '水母',
        })
        水母文本.設為推薦用字()
        一九文本 = 平臺項目表.外語翻母語(水母編號, {
            '文本資料': '一九',
        })
        小刀文本 = 平臺項目表._校對母語文本(一九文本.編號(), {
            '文本資料': '小刀',
        })
        小刀文本.設為推薦用字()
#         前端輸入
        回應 = self.client.get('/平臺項目列表/揣列表', {
            '關鍵字': '水母'
        })
#         前端回傳結果
        self.assertEqual(回應.status_code, 200)
        回應資料 = 回應.json()
        self.assertEqual(回應資料['其他建議'][0]['文本資料'], '䖳')
        self.assertEqual(回應資料['其他建議'][1]['文本資料'], '一九')
        self.assertEqual(回應資料['其他建議'][2]['文本資料'], '水母')

    def 資料庫加外語(self, 外語詞):
        return 平臺項目表.加外語資料(
            {
                '外語資料': 外語詞,
            }
        ).編號()
