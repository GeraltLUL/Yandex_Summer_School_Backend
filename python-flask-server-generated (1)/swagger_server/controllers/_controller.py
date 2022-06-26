import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.shop_unit import ShopUnit  # noqa: E501
from swagger_server.models.shop_unit_import_request import ShopUnitImportRequest  # noqa: E501
from swagger_server.models.shop_unit_statistic_response import ShopUnitStatisticResponse  # noqa: E501
from swagger_server import util

import dateutil.parser as dp
import uuid
from datetime import datetime
from bson import json_util
from flask import Flask, request, json, make_response
from pymongo import MongoClient

# MongoDB config
client = MongoClient('localhost', 27017)
db = client['YandexSummerSchool']
colItems = db['items']
colQueries = db['queries']


#
class Item:
    id = ''
    name = ''
    type = ''
    parentId = ''
    date = ''  # ISO 8601 : YYYY-MM-DDThh:mm:ss	 2005-08-09T18:31:42
    price = 0
    children = []

    def __init__(self, id, name, type, parentId, date, price, children):
        self.id = id
        self.name = name.encode('utf8')
        self.type = type
        self.parentId = parentId
        self.date = date
        self.price = price
        self.children = children

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parentId": self.parentId,
            "date": self.date,
            "price": self.price,
            "children": self.children
        }


class Queri:
    uid = ''
    id = ''
    name = ''
    type = ''
    parentId = ''
    date = ''
    price = 0
    children = []

    def __init__(self, uid, id, name, type, parentId, date, price, children):
        self.uid = uid
        self.id = id
        self.name = name.encode('utf8')
        self.type = type
        self.parentId = parentId
        self.date = date
        self.price = price
        self.children = children


def find_statistic(id, dateStart, dateEnd):
    items = []
    curdb = colQueries.find({'id': id})

    startInSec = dp.parse(dateStart).timestamp() if dateStart is not None else None
    endInSec = dp.parse(dateEnd).timestamp() if dateEnd is not None else None

    for item in curdb:
        itemDateInSec = dp.parse(item['date']).timestamp()
        del (item['_id'])

        if dateStart is not None and dateEnd is not None:
            if endInSec >= itemDateInSec >= startInSec:
                items.append(item)
        else:
            items.append(item)

    return {'items': items}


def calcPrice(node, k):
    if 'children' in node.keys() and node['children'] is None or 'children' not in node.keys():
        # k+=1
        print(1, k + 1)
        return node['price'] / k if node['price'] > 0 else 0

    price = 0
    if 'children' in node.keys():
        for x in node['children']:
            price += calcPrice(x, k + 1)

    print(2, k + 1)
    return price / k


def create_record(curItem):
    # colItems.find_one_and_update()
    if 'price' not in curItem.keys():
        curItem['price'] = None
        requestPrice = None
    else:
        requestPrice = curItem['price']

    if 'children' not in curItem.keys():
        curItem['children'] = None
        requestChildren = None
    else:
        requestChildren = curItem['children']

    requestType = curItem['type']
    requestId = curItem['id']
    requestDate = str(datetime.now()).replace(' ', 'T').split('.')[0] + '.000Z'

    colItems.find_one_and_replace(filter={'id': requestId},
                                  replacement={'id': requestId,
                                               'name': curItem['name'],
                                               'type': requestType,
                                               'parentId': curItem['parentId'],
                                               'date': requestDate,
                                               'price': requestPrice,
                                               'children': requestChildren
                                               },
                                  upsert=True)

    colQueries.insert_one({
        'uid': str(uuid.uuid4()),
        'id': requestId,
        'name': curItem['name'],
        'type': requestType,
        'parentId': curItem['parentId'],
        'date': requestDate,
        'price': requestPrice,
        'children': requestChildren
    })



def delete_record(id):
    colQueries.find_one_and_delete({'id': id})
    return colItems.find_one_and_delete({'id': id})


def get_record(id):
    curRecord = colItems.find_one({'id': id})

    if curRecord is not None:
        return Item(
            id=curRecord['id'],
            name=curRecord['name'],
            type=curRecord['type'],
            parentId=curRecord['parentId'],
            date=curRecord['date'],
            price=curRecord['price'],
            children=curRecord['children']
        )
    else:
        return None


def find_24h(startTime):
    startInSec = dp.parse(startTime).timestamp()
    endInSec = startInSec + 86400
    fulldb = colItems.find()

    items = []
    for item in fulldb:
        itemDateInSec = dp.parse(item['date']).timestamp()

        if endInSec >= itemDateInSec >= startInSec:
            del (item['_id'])
            items.append(item)

    return {'items': items}


#


def delete_id_delete(id_):  # noqa: E501
    id = id_

    if id is None or id == '':
        responseCode = 400
        responseMessage = 'Validation Failed'
    elif delete_record(id=id) is None:
        responseCode = 404
        responseMessage = 'Item not found'
    else:
        responseCode = 200
        responseMessage = 'Validation Successes'

    # for record in colQueries:
    #     if record

    return make_response({
        'code': responseCode,
        'message': responseMessage
    }, responseCode)


def imports_post(body=None):  # noqa: E501
    for item in request.json['items']:
        if item['type'] == "OFFER" and item['price'] is None:
                return make_response({
                    'code': 400,
                    'message': 'Validation Failed'
                }, 400)

    for item in request.json['items']:
        create_record(curItem=item)

    return make_response({
        'code': 200,
        'message': 'Validation Successes'
    }, 200)


def node_id_statistic_get(id_, date_start=None, date_end=None):  # noqa: E501
    id = id_
    dateStart = date_start
    dateEnd = date_end

    if id is None:
        return make_response({
            'code': 400,
            'message': 'Validation Failed'
        }, 400)

    curRecords = find_statistic(id, dateStart, dateEnd)

    if curRecords is None:
        return make_response({
            'code': 404,
            'message': 'Item not found'
        }, 404)

    return make_response(json.loads(json_util.dumps(curRecords)), 200)


def nodes_id_get(id_):  # noqa: E501
    id = id_
    curRecord = get_record(id=id)

    if id is None or id == '':
        return make_response({
            'code': 400,
            'message': 'Validation Failed'
        }, 400)
    elif curRecord is None:
        return make_response({
            'code': 404,
            'message': 'Item not found'
        }, 404)

    return make_response(curRecord.to_json(), 200)


def sales_get(date):  # noqa: E501
    dateStart = date

    if 'Z' not in dateStart or dateStart is None:
        return make_response({
            'code': 400,
            'message': 'Validation Failed'
        }, 400)

    curRecords = find_24h(dateStart)
    return make_response(json.loads(json_util.dumps(curRecords)), 200)
