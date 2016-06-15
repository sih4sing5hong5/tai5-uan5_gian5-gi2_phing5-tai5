from django.db.models.query_utils import Q
from django.http.response import JsonResponse


from 臺灣言語資料庫.資料模型 import 外語表
from 臺灣言語平臺.介面.Json失敗回應 import Json失敗回應


def 揣外語請教條(request):
    try:
        外語資料 = request.GET['關鍵字']
    except:
        return Json失敗回應({'錯誤': '無傳關鍵字'})
    符合資料 = []
    for 外語 in 外語表.objects\
            .filter(外語資料=外語資料)\
            .filter(
                Q(翻譯文本__文本__平臺項目__推薦用字=True) |
                Q(翻譯文本__文本__文本校對__新文本__平臺項目__推薦用字=True)
            )\
            .order_by('-pk'):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    其他建議資料 = []
    for 外語 in 外語表.objects\
            .exclude(外語資料=外語資料)\
            .filter(外語資料__contains=外語資料)\
            .order_by('-pk'):
        其他建議資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料, '其他建議': 其他建議資料})


def 揣無建議的外語(request):
    符合資料 = []
    for 外語 in 外語表.objects.filter(
        翻譯影音__isnull=True,
        翻譯文本__isnull=True
    ):
        符合資料.append({
            '外語項目編號': str(外語.平臺項目.編號()),
            '種類': 外語.種類.種類,
            '語言腔口': 外語.語言腔口.語言腔口,
            '外語語言': 外語.外語語言.語言腔口,
            '外語資料': 外語.外語資料,
        })
    return JsonResponse({'列表': 符合資料})

# def 顯示全部資料組(第幾个開始,愛幾个):
# 	資料組陣列=[]
# 	for 資料組 in 資料組表.objects.order('-pk')[第幾个開始:第幾个開始+愛幾个]:
# 		資料結果={'編號':資料組.編號()}
# 		if 資料組.外語:
# 			資料=資料組.外語
# 			資料結果['類型']='外語'
# 			資料結果['建立時間']=資料.收錄時間
# 			資料結果['語言腔口']=資料.語言腔口
# 			資料結果['種類']=資料.種類
# 			資料結果['外語語言']=資料.外語語言
# 			資料結果['外語資料']=資料.外語資料
# 		elif 資料組.影音:
# 			資料=資料組.影音
# 			資料結果['類型']='影音'
# 			資料結果['建立時間']=資料.收錄時間
# 			資料結果['語言腔口']=資料.語言腔口
# 			資料結果['種類']=資料.種類
# 			資料結果['影音網址']=資料.網頁影音資料.url
# 		else: # 資料組.文本:
# 			資料=資料組.文本
# 			資料結果['類型']='文本'
# 			資料結果['建立時間']=資料.收錄時間
# 			資料結果['語言腔口']=資料.語言腔口
# 			資料結果['種類']=資料.種類
# 			資料結果['文本資料']=資料.文本資料
# 		資料組陣列.append(資料組陣列)
