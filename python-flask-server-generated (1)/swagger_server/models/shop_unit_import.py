# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.shop_unit_type import ShopUnitType  # noqa: F401,E501
from swagger_server import util


class ShopUnitImport(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: str=None, name: str=None, parent_id: str=None, type: ShopUnitType=None, price: int=None):  # noqa: E501
        """ShopUnitImport - a model defined in Swagger

        :param id: The id of this ShopUnitImport.  # noqa: E501
        :type id: str
        :param name: The name of this ShopUnitImport.  # noqa: E501
        :type name: str
        :param parent_id: The parent_id of this ShopUnitImport.  # noqa: E501
        :type parent_id: str
        :param type: The type of this ShopUnitImport.  # noqa: E501
        :type type: ShopUnitType
        :param price: The price of this ShopUnitImport.  # noqa: E501
        :type price: int
        """
        self.swagger_types = {
            'id': str,
            'name': str,
            'parent_id': str,
            'type': ShopUnitType,
            'price': int
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'parent_id': 'parentId',
            'type': 'type',
            'price': 'price'
        }
        self._id = id
        self._name = name
        self._parent_id = parent_id
        self._type = type
        self._price = price

    @classmethod
    def from_dict(cls, dikt) -> 'ShopUnitImport':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ShopUnitImport of this ShopUnitImport.  # noqa: E501
        :rtype: ShopUnitImport
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> str:
        """Gets the id of this ShopUnitImport.

        Уникальный идентфикатор  # noqa: E501

        :return: The id of this ShopUnitImport.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id: str):
        """Sets the id of this ShopUnitImport.

        Уникальный идентфикатор  # noqa: E501

        :param id: The id of this ShopUnitImport.
        :type id: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self) -> str:
        """Gets the name of this ShopUnitImport.

        Имя элемента.  # noqa: E501

        :return: The name of this ShopUnitImport.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this ShopUnitImport.

        Имя элемента.  # noqa: E501

        :param name: The name of this ShopUnitImport.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def parent_id(self) -> str:
        """Gets the parent_id of this ShopUnitImport.

        UUID родительской категории  # noqa: E501

        :return: The parent_id of this ShopUnitImport.
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id: str):
        """Sets the parent_id of this ShopUnitImport.

        UUID родительской категории  # noqa: E501

        :param parent_id: The parent_id of this ShopUnitImport.
        :type parent_id: str
        """

        self._parent_id = parent_id

    @property
    def type(self) -> ShopUnitType:
        """Gets the type of this ShopUnitImport.


        :return: The type of this ShopUnitImport.
        :rtype: ShopUnitType
        """
        return self._type

    @type.setter
    def type(self, type: ShopUnitType):
        """Sets the type of this ShopUnitImport.


        :param type: The type of this ShopUnitImport.
        :type type: ShopUnitType
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def price(self) -> int:
        """Gets the price of this ShopUnitImport.

        Целое число, для категорий поле должно содержать null.  # noqa: E501

        :return: The price of this ShopUnitImport.
        :rtype: int
        """
        return self._price

    @price.setter
    def price(self, price: int):
        """Sets the price of this ShopUnitImport.

        Целое число, для категорий поле должно содержать null.  # noqa: E501

        :param price: The price of this ShopUnitImport.
        :type price: int
        """

        self._price = price
