# -*- coding: utf-8 -*-
import json

from django.test import TestCase


from 臺灣言語資料庫.資料模型 import 文本表
from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語資料庫.資料模型 import 影音表
from 臺灣言語資料庫.關係模型 import 翻譯影音表
from 臺灣言語資料庫.關係模型 import 影音文本表

from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語資料庫.關係模型 import 翻譯文本表
from 臺灣言語平臺.使用者模型 import 使用者表


class 外語新詞文本加失敗試驗(TestCase):

    def setUp(self):
        super(外語新詞文本加失敗試驗, self).setUp()
        self.鄉民 = 使用者表.加使用者(
            'sui2@pigu.tw', {"名": '鄉民', '出世年': '1950', '出世地': '臺灣', }
        )
        self.鄉民.set_password('Phoo-bun')
        self.鄉民.save()
        外語回應資料 = self.client.post(
            '/平臺項目/加外語', {
                '外語資料': '漂亮',
            }
        ).json()
        self.外語項目編號 = int(外語回應資料['平臺項目編號'])

        self.外語表資料數 = 外語表.objects.all().count()
        self.影音表資料數 = 影音表.objects.all().count()
        self.文本表資料數 = 文本表.objects.all().count()
        self.翻譯影音表資料數 = 翻譯影音表.objects.all().count()
        self.影音文本表資料數 = 影音文本表.objects.all().count()
        self.翻譯文本表資料數 = 翻譯文本表.objects.all().count()
        self.平臺項目表資料數 = 平臺項目表.objects.all().count()

    def tearDown(self):
        # 		後端資料庫檢查不增加資料
        self.assertEqual(外語表.objects.all().count(), self.外語表資料數)
        self.assertEqual(影音表.objects.all().count(), self.影音表資料數)
        self.assertEqual(翻譯影音表.objects.all().count(), self.翻譯影音表資料數)
        self.assertEqual(文本表.objects.all().count(), self.文本表資料數)
        self.assertEqual(影音文本表.objects.all().count(), self.影音文本表資料數)
        self.assertEqual(翻譯文本表.objects.all().count(), self.翻譯文本表資料數)
        self.assertEqual(平臺項目表.objects.all().count(), self.平臺項目表資料數)

    def test_編號欄位無佇資料庫(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': '2016',
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '編號號碼有問題',
        })

    def test_編號欄位毋是數字(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': 'self.外語項目編號',
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '編號欄位不是數字字串',
        })

    def test_來源無轉json字串(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '來源': {'名': '自己'},
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '來源抑是屬性無轉json字串',
        })

    def test_屬性無轉json字串(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '屬性': {'詞性': '形容詞', '字數': '1'},
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '來源抑是屬性無轉json字串',
        })

    def test_缺編號欄位(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                # 				'外語項目編號':self.外語項目編號,
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '資料欄位有缺',
        })

    def test_來源沒有名的欄位(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '來源': json.dumps({'誰': '自己'}),
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '來源沒有「名」的欄位',
        })

    def test_種類欄位不符規範(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '種類': '漢字',
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '種類和外語不一樣',
        })

    def test_無仝的種類(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '種類': '語句',  # 外語的種類是「字詞」
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '種類和外語不一樣',
        })

    def test_無仝的語言腔口(self):
        回應 = self.client.post(
            '/平臺項目/加新詞文本', {
                '外語項目編號': self.外語項目編號,
                '語言腔口': '噶哈巫語',  # 外語的語言腔口是「臺灣語言」
                '文本資料': '媠',
            }
        )
        self.assertEqual(回應.status_code, 400)
        self.assertEqual(json.loads(回應.content.decode("utf-8")), {
            '錯誤': '語言腔口和外語不一樣',
        })
