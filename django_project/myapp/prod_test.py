from django.db import connection
import pymysql

def selectTest(array):
    sql = """select a.prod_name, a.prod_price,b.event_cd 
                from product a, prod_event b 
                where a.prod_name LIKE %s and b.conv_type=%s
                and a.prod_id=b.prod_id"""

    sql3 = """select prod_name, prod_price from product where prod_name LIKE %s 
                        """
    cursor = connection.cursor()

    conv = "GS"
    items = ["아이스브레이커메론","멘토스"]
    #list1 = ["오츠카)데미소다\n피치250ml\n3개 2,400원\n1,200원\n데미소다\nDemiSoda\nDemisoda l\n데미소다\n"]
    list1 = ["킬리만자로"]
    list2 = list1[0].split("\n")
    #items = ["치약"]
    #items = ["한라봉에이드"]

    products=[]
    products2 = []
    str = []
    etc = []
    price = []
    for i in array:
        if i.isalpha():
            etc.append(i)
        #i[0].isdecimal() and i[1]=='개':
            #etc.append(i)
        # 앞글자가 숫자 마지막글자가 원일때
        #elif i[0].isdecimal() and i[-1].endswith('원'):
        #    j = i[:-1]
        #    price.append(int(j))
        # 글자가 숫자로만 이루어졌을때
        elif i.endswith('원'):
            price.append(i)
        elif i.isdecimal():
            price.append(i)
        else:
            str.append(i)

    for i in str:
        cursor.execute(sql, (('%' + i + '%',conv,)))
        for row in cursor:
            dic = {'prod_name': row[0], 'prod_price': row[1], 'event_cd': row[2]}
            products.append(dic)

    #행사상품이아닐때
    if not products:
        for i in str:
            cursor.execute(sql3, (('%' + i + '%',)))
            for row in cursor:
                dic = {'prod_name': row[0], 'prod_price': row[1]}
                dic['event_cd']='일반상품'
                products.append(dic)
    #중복값 제거
    new_products = []
    for j in products:
        if j not in new_products:
            new_products.append(j)

    return new_products

