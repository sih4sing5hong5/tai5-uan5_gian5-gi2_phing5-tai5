from django.http.response import JsonResponse
from 臺灣言語平臺.項目模型 import 平臺項目表

列表一頁幾筆 = 15

def 外語請教條列表(request):
	try:
		第幾頁 = int(request.GET['第幾頁'])
	except:
		第幾頁 = 1
	列表 = []
	for 平臺項目 in 平臺項目表.objects\
			.exclude(外語__isnull=True)\
			.filter(是資料源頭=True)\
			.order_by('-pk')\
			[列表一頁幾筆 * (第幾頁 - 1):列表一頁幾筆 * 第幾頁]:
		列表.append({
				'外語請教條項目編號':str(平臺項目.編號()),
				'種類':平臺項目.外語.種類.種類,
				'語言腔口':平臺項目.外語.語言腔口.語言腔口,
				'外語語言':平臺項目.外語.外語語言.語言腔口,
				'外語資料':平臺項目.外語.外語資料,
			})
	return JsonResponse({'列表':列表})


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

			
