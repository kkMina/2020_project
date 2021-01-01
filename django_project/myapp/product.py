#김민아 수정 2020-11-29
from django.db import connection
import pymysql
def selectTest(conv,items):
    sql = """select a.prod_name, b.event_price,b.event_cd 
                from product a, prod_event b 
                where a.prod_name LIKE %s and b.conv_type=%s
                and a.prod_id=b.prod_id"""
    sql2 = """select a.prod_name, a.prod_price,b.event_cd 
                    from product a, prod_event b 
                    where a.prod_name LIKE %s and b.conv_type=%s
                    and a.prod_id=b.prod_id or a.prod_price =%s

                   """
    sql3 = """select prod_name, prod_price from product where prod_name LIKE %s 
                            """

    cursor = connection.cursor()

    str = []
    price = []
    etc = []

    slice_list = []
    prod_string ="".join(items) #리스트 합치기
    slice_list.append(prod_string)
    slice_list = slice_list[0].split("\n")
    slice_list = list(filter(None, slice_list)) #빈칸삭제
    for i in slice_list:
        if i.isalpha():
            etc.append(i)
        #i.isalpha():
           #etc.append(i)

        # 앞글자가 숫자 마지막글자가 원일때
        #elif i[0].isdecimal() and i[-1].endswith('원'):
        #    j = i[:-1]
        #    price.append(int(j))
        # 글자가 숫자로만 이루어졌을때
        elif i.endswith('원'):
            price.append(i)
        elif i.isdecimal():
            price.append(int(i))
        else:
            str.append(i)

    print(str)
    print(price)
    products=[]

    for i in str:
        cursor.execute(sql, (('%' + i + '%', conv,)))
        for row in cursor:
            dic = {'prod_name': row[0], 'prod_price': row[1], 'event_cd': row[2]}
            products.append(dic)

        # 행사상품이아닐때
    if not products:
        for i in str:
            cursor.execute(sql3, (('%' + i + '%',)))
            for row in cursor:
                dic = {'prod_name': row[0], 'prod_price': row[1]}
                dic['event_cd'] = '일반상품'
                products.append(dic)

    # 중복값 제거
    new_products = []
    for j in products:
        if j not in new_products:
            new_products.append(j)

    new_products = sorted(products, key=lambda p: (p['event_cd']))

    return new_products
