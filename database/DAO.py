from database.DB_connect import DBConnect
from model.arco import Arco
from model.category import Category
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select * 
                    from categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(Category(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getProductsByCategory(category):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from products p
                    where p.category_id = %s"""

        cursor.execute(query, (category.category_id,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(category, d1, d2, idMapP):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select p1.product_id as id1, p2.product_id as id2, p1.n as n1, p2.n as n2, p1.n+p2.n as peso
                    from (select p.product_id, count(*) as n
                    from products p, order_items oi, orders o
                    where p.product_id = oi.product_id and oi.order_id = o.order_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s
                    group by p.product_id ) p1,
                    (select p.product_id, count(*) as n
                    from products p, order_items oi, orders o
                    where p.product_id = oi.product_id and oi.order_id = o.order_id 
                    and o.order_date between %s and %s
                    and p.category_id = %s 
                    group by p.product_id ) p2
                    where p1.product_id <> p2.product_id
                    and p1.n >= p2.n
                    order by peso asc"""

        cursor.execute(query, (d1,d2,category.category_id,d1,d2,category.category_id,))

        for row in cursor:
            results.append(Arco(idMapP[row["id1"]],idMapP[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results
