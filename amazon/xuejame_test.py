import datetime
import xlwt
from xlwt import Workbook

def xuejame_time():
    now_date = datetime.datetime.now().date()
    now_time = datetime.datetime.now().time().hour
    print(now_date)
    print(now_time)
    str_keyword = 'D:\programming\Dropbox\\amazon_keyword\key_word_'+str(now_date)+'_'+str(now_time)+'.xls'
    workbook = Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('FR-HUB')
    worksheet.write(0,0,"title")
    worksheet.write(0,1,"key_word")
    worksheet.write(0,2,"自然搜索")
    worksheet.write(0,3,"广告搜索")
    worksheet = workbook.add_sheet('UK-hub')
    worksheet.write(0,0,"title")
    worksheet.write(0,1,"key_word")
    worksheet.write(0,2,"自然搜索")
    worksheet.write(0,3,"广告搜索")
    worksheet = workbook.add_sheet('DE-hub')
    worksheet.write(0,0,"title")
    worksheet.write(0,1,"key_word")
    worksheet.write(0,2,"自然搜索")
    worksheet.write(0,3,"广告搜索")
    worksheet = workbook.add_sheet('US-CORRECTOR')
    worksheet.write(0,0,"title")
    worksheet.write(0,1,"key_word")
    worksheet.write(0,2,"自然搜索")
    worksheet.write(0,3,"广告搜索")
    worksheet = workbook.add_sheet('US-SOFOOT')
    worksheet.write(0,0,"title")
    worksheet.write(0,1,"key_word")
    worksheet.write(0,2,"自然搜索")
    worksheet.write(0,3,"广告搜索")
    worksheet = workbook.add_sheet('US-hub')
    worksheet.write(0,0,"title")
    worksheet.write(0,1,"key_word")
    worksheet.write(0,2,"自然搜索")
    worksheet.write(0,3,"广告搜索")
    worksheet = workbook.add_sheet('CA-hub')
    worksheet.write(0,0,"title")
    worksheet.write(0,1,"key_word")
    worksheet.write(0,2,"自然搜索")
    worksheet.write(0,3,"广告搜索")
    workbook.save(str_keyword)
    return str_keyword

if __name__ =="__main__":
    xuejame_time()