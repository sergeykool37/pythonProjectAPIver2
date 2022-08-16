from django.db import connection


def delete_all_views(cursor):
    query = 'DROP VIEW IF EXISTS top_customer;'
    cursor.execute(query)

    query = 'DROP VIEW IF EXISTS items;'
    cursor.execute(query)


def create_view_top_customer(cursor):
    query = '''
        CREATE VIEW IF NOT EXISTS top_customer AS
        SELECT customer, sum(total) as sum_total
        FROM proc_deals_deal d
        GROUP BY customer
        ORDER BY SUM(total) DESC
        LIMIT 5
        '''
    cursor.execute(query)


def create_view_items(cursor):
    query = '''
        CREATE VIEW IF NOT EXISTS items AS
        SELECT  d.item, count(distinct  t.customer), t.customer
      FROM proc_deals_deal d
      INNER JOIN top_customer as t ON d.customer = t.customer
      GROUP BY d.item
      HAVING count(distinct  t.customer) > 1
        '''
    cursor.execute(query)


def  select_top_customets_with_items(cursor):

    delete_all_views(cursor)

    create_view_top_customer(cursor)

    create_view_items(cursor)

    query = '''
        SELECT  distinct d.item, d.customer, c.sum_total
        FROM proc_deals_deal  as d
        JOIN top_customer c on d.customer = c.customer
        WHERE item in (SELECT item FROM items)
        '''

    result = cursor.execute(query)

    return result

def return_top_customer_with_items():


    cursor = connection.cursor()

    result_query = select_top_customets_with_items(cursor)

    ans = []
    record= {'customer':'',
             'items':'',
             'total_sum':0}
    for row in result_query.fetchall():
        if record['customer'] == row[1]:
            record['items'] = record['items']+', '+ row[0]
        else:
            if record['customer'] != '':
                ans.append(record)
                record = {'customer': '',
                          'items': [],
                          'total_sum': 0}
            record['customer'] = row[1]
            record['items'] = row[0]
            record['total_sum'] = row[2]
    if record['customer'] != '':
        ans.append(record)
    return ans

