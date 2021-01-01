from django.db import connection
import pymysql

def qr_result(conv, prod_name):
    sql = """select a.prod_name, a.prod_price,b.event_cd 
                from product a, prod_event b 
                where a.prod_name LIKE %s and b.conv_type=%s
                and a.prod_id=b.prod_id"""

    sql3 = """select prod_name, prod_price from product where prod_name LIKE %s 
                        """
    cursor = connection.cursor()

    products=[]
    products2 = []
    prod_array = []
    prod_array.append(prod_name)
    for i in prod_array:
        cursor.execute(sql, (('%' + i + '%',conv,)))
        for row in cursor:
            dic = {'prod_name': row[0], 'prod_price': row[1], 'event_cd': row[2]}
            products.append(dic)

    #행사상품이아닐때
    if not products:
        for i in prod_array:
            cursor.execute(sql3, (('%' + i + '%',)))
            for row in cursor:
                dic = {'prod_name': row[0], 'prod_price': row[1]}
                dic['event_cd']='일반상품'
                products.append(dic)


    return products