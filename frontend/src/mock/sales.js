import Mock from 'mockjs'

const salesOrderList = {
    "count": 21,
    "next": "http://127.0.0.1:8000/api/sales_order/?page=2",
    "previous": null,
    "results": [
        {
            "id": "SA200721134052536062",
            "date": "2020-07-20T16:00:00Z",
            "seller": "111",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 12.6,
            "zero_amount": 0.5,
            "change_amount": -35.0,
            "client_phone": "333",
            "client_name": "333",
            "client_address": "",
            "remark": "",
            "discount": 90.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "unit_price": 14.0,
                    "amount": 0.8,
                    "remark": null
                }
            ],
            "amount_receivable": 0.72
        },
        {
            "id": "SA200721134608159509",
            "date": "2020-07-20T16:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 20.0,
            "zero_amount": 0.0,
            "change_amount": 25.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "unit_price": 14.0,
                    "amount": 0.8,
                    "remark": null
                }
            ],
            "amount_receivable": 0.8
        },
        {
            "id": "12",
            "date": "2020-07-15T16:00:00Z",
            "seller": "111",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": -14.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [],
            "amount_receivable": 0.0
        },
        {
            "id": "13",
            "date": "2020-07-15T16:00:00Z",
            "seller": "111",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": -14.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [],
            "amount_receivable": 0.0
        },
        {
            "id": "14",
            "date": "2020-07-15T16:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": -14.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [],
            "amount_receivable": 0.0
        },
        {
            "id": "15",
            "date": "2020-07-15T16:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": -14.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [],
            "amount_receivable": 0.0
        },
        {
            "id": "16",
            "date": "2020-07-15T16:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": -14.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [],
            "amount_receivable": 0.0
        },
        {
            "id": "17",
            "date": "2020-07-15T16:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": -14.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [],
            "amount_receivable": 0.0
        },
        {
            "id": "18",
            "date": "2020-07-15T16:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": -14.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "unit_price": 14.0,
                    "amount": 14.0,
                    "remark": null
                }
            ],
            "amount_receivable": 0.0
        },
        {
            "id": "19",
            "date": "2020-07-15T16:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": 0.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "3f81f392-c34a-11ea-b4ce-25e2e5a8f494",
                    "name": "goods2",
                    "code": "1002",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "unit_price": 0.0,
                    "amount": 0.0,
                    "remark": null
                },
                {
                    "product_id": "3f81f393-c34a-11ea-b4ce-25e2e5a8f494",
                    "name": "goods2",
                    "code": "1002",
                    "spec1": "spec1",
                    "spec2": "spec4",
                    "quantity": 1.0,
                    "unit_price": 0.0,
                    "amount": 0.0,
                    "remark": null
                },
                {
                    "product_id": "3f81f394-c34a-11ea-b4ce-25e2e5a8f494",
                    "name": "goods2",
                    "code": "1002",
                    "spec1": "spec5",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "unit_price": 0.0,
                    "amount": 0.0,
                    "remark": null
                }
            ],
            "amount_receivable": 0.0
        },
        {
            "id": "10",
            "date": "2020-07-12T00:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": 2.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 2.0,
                    "unit_price": 14.0,
                    "amount": 28.0,
                    "remark": null
                }
            ],
            "amount_receivable": 0.0
        },
        {
            "id": "9",
            "date": "2020-07-11T00:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": 1.0,
            "client_phone": "",
            "client_name": "",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "unit_price": 14.0,
                    "amount": 14.0,
                    "remark": null
                }
            ],
            "amount_receivable": 0.0
        },
        {
            "id": "7",
            "date": "2020-07-08T00:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 3,
            "account_name": "21312",
            "amount_received": 0.0,
            "zero_amount": 0.0,
            "change_amount": 32.0,
            "client_phone": "222",
            "client_name": "33",
            "client_address": "",
            "remark": "",
            "discount": 100.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 12.0,
                    "unit_price": 14.0,
                    "amount": 0.0,
                    "remark": "12312"
                }
            ],
            "amount_receivable": 0.0
        },
        {
            "id": "8",
            "date": "2020-07-08T00:00:00Z",
            "seller": "11",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "account": 2,
            "account_name": "结算账户1",
            "amount_received": 0.0,
            "zero_amount": 2.0,
            "change_amount": 2.0,
            "client_phone": "333",
            "client_name": "333",
            "client_address": "",
            "remark": "",
            "discount": 90.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "e9f1996e-c105-11ea-b73e-87e5a1fdee64",
                    "name": "goods3",
                    "code": "1003",
                    "spec1": "spec4",
                    "spec2": "spec1",
                    "quantity": 10.0,
                    "unit_price": 12.0,
                    "amount": 108.0,
                    "remark": null
                }
            ],
            "amount_receivable": 0.0
        },
        {
            "id": "6",
            "date": "2020-07-08T00:00:00Z",
            "seller": "11",
            "warehouse": 2,
            "warehouse_name": "warehouse2",
            "account": 3,
            "account_name": "21312",
            "amount_received": 0.0,
            "zero_amount": 0.5,
            "change_amount": 2.5,
            "client_phone": "1111111",
            "client_name": "czw",
            "client_address": "qwe",
            "remark": "wqe",
            "discount": 100.0,
            "is_undo": false,
            "products": [
                {
                    "product_id": "0d50aba4-bc4a-11ea-8e20-0b942bb21c98",
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 2.0,
                    "unit_price": 14.0,
                    "amount": 0.0,
                    "remark": null
                }
            ],
            "amount_receivable": 0.0
        }
    ]
};

const salesTaskList = {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "goods": 1,
            "goods_name": "goods1",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "quantity": 10.0,
            "start_date": "2020-07-06",
            "end_date": "2020-07-21",
            "create_date": "2020-07-12",
            "completed_quantity": 21.0
        },
        {
            "id": 1,
            "goods": 1,
            "goods_name": "goods1",
            "warehouse": 1,
            "warehouse_name": "warehouse1",
            "quantity": 10.0,
            "start_date": "2020-07-12",
            "end_date": "2020-07-21",
            "create_date": "2020-07-12",
            "completed_quantity": 2.0
        }
    ]
};

const salesProfitList = {
    "total_profit": 240.1984534506999,
    "results": [
        {
            "id": 6,
            "date": "2020-07-08T00:00:00Z",
            "warehouse_name": "warehouse2",
            "products": [
                {
                    "id": 5,
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 2.0,
                    "purchase_price": 0.0,
                    "unit_price": 14.0,
                    "remark": null,
                    "goods_name": "goods1"
                }
            ],
            "extra_profits": []
        },
        {
            "id": 7,
            "date": "2020-07-08T00:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [
                {
                    "id": 6,
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 12.0,
                    "purchase_price": 0.0,
                    "unit_price": 14.0,
                    "remark": "12312",
                    "goods_name": "goods1"
                }
            ],
            "extra_profits": []
        },
        {
            "id": 8,
            "date": "2020-07-08T00:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [
                {
                    "id": 7,
                    "spec1": "spec4",
                    "spec2": "spec1",
                    "quantity": 10.0,
                    "purchase_price": 0.0,
                    "unit_price": 12.0,
                    "remark": null,
                    "goods_name": "goods3"
                }
            ],
            "extra_profits": []
        },
        {
            "id": 9,
            "date": "2020-07-11T00:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [
                {
                    "id": 8,
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "unit_price": 14.0,
                    "remark": null,
                    "goods_name": "goods1"
                }
            ],
            "extra_profits": []
        },
        {
            "id": 10,
            "date": "2020-07-12T00:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [
                {
                    "id": 9,
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 2.0,
                    "purchase_price": 0.0,
                    "unit_price": 14.0,
                    "remark": null,
                    "goods_name": "goods1"
                }
            ],
            "extra_profits": []
        },
        {
            "id": 11,
            "date": "2020-06-30T16:00:00Z",
            "warehouse_name": "warehouse2",
            "products": [
                {
                    "id": 10,
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "unit_price": 14.0,
                    "remark": null,
                    "goods_name": "goods1"
                }
            ],
            "extra_profits": []
        },
        {
            "id": 12,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [],
            "extra_profits": []
        },
        {
            "id": 13,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [],
            "extra_profits": []
        },
        {
            "id": 14,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [],
            "extra_profits": []
        },
        {
            "id": 15,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [],
            "extra_profits": []
        },
        {
            "id": 16,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [],
            "extra_profits": []
        },
        {
            "id": 17,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [],
            "extra_profits": []
        },
        {
            "id": 18,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [
                {
                    "id": 11,
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.8015465493000795,
                    "unit_price": 14.0,
                    "remark": null,
                    "goods_name": "goods1"
                }
            ],
            "extra_profits": []
        },
        {
            "id": 19,
            "date": "2020-07-15T16:00:00Z",
            "warehouse_name": "warehouse1",
            "products": [
                {
                    "id": 12,
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "unit_price": 0.0,
                    "remark": null,
                    "goods_name": "goods2"
                },
                {
                    "id": 13,
                    "spec1": "spec1",
                    "spec2": "spec4",
                    "quantity": 1.0,
                    "purchase_price": 112.0,
                    "unit_price": 0.0,
                    "remark": null,
                    "goods_name": "goods2"
                },
                {
                    "id": 14,
                    "spec1": "spec5",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 33.0,
                    "unit_price": 0.0,
                    "remark": null,
                    "goods_name": "goods2"
                }
            ],
            "extra_profits": []
        }
    ],
    "count": 14
};

const salesValueList = {
    "results": [
        {
            "date": "2020-07-08",
            "warehouse_name": "warehouse1",
            "amount": 274.0
        },
        {
            "date": "2020-07-11",
            "warehouse_name": "warehouse1",
            "amount": 14.0
        },
        {
            "date": "2020-07-12",
            "warehouse_name": "warehouse1",
            "amount": 28.0
        },
        {
            "date": "2020-07-15",
            "warehouse_name": "warehouse1",
            "amount": 98.0
        },
        {
            "date": "2020-07-08",
            "warehouse_name": "warehouse2",
            "amount": 27.5
        },
        {
            "date": "2020-06-30",
            "warehouse_name": "warehouse2",
            "amount": 14.0
        }
    ],
    "warehouse_list": [
        "warehouse1",
        "warehouse2",
        "333"
    ]
};

const salesOrderRetrieve = {
    "id": "19",
    "date": "2020-07-15T16:00:00Z",
    "seller": "11",
    "warehouse": 1,
    "warehouse_name": "warehouse1",
    "account": 2,
    "account_name": "结算账户1",
    "amount_received": 0.0,
    "zero_amount": 0.0,
    "change_amount": 0.0,
    "client_phone": "",
    "client_name": "",
    "client_address": "",
    "remark": "",
    "discount": 100.0,
    "is_undo": false,
    "products": [
        {
            "product_id": "3f81f392-c34a-11ea-b4ce-25e2e5a8f494",
            "name": "goods2",
            "code": "1002",
            "spec1": "spec1",
            "spec2": "spec3",
            "quantity": 1.0,
            "unit_price": 0.0,
            "amount": 0.0,
            "remark": null
        },
        {
            "product_id": "3f81f393-c34a-11ea-b4ce-25e2e5a8f494",
            "name": "goods2",
            "code": "1002",
            "spec1": "spec1",
            "spec2": "spec4",
            "quantity": 1.0,
            "unit_price": 0.0,
            "amount": 0.0,
            "remark": null
        },
        {
            "product_id": "3f81f394-c34a-11ea-b4ce-25e2e5a8f494",
            "name": "goods2",
            "code": "1002",
            "spec1": "spec5",
            "spec2": "spec3",
            "quantity": 1.0,
            "unit_price": 0.0,
            "amount": 0.0,
            "remark": null
        }
    ]
};

const clientList = {
    count: 99,
    results: [
      { id: 1, name: 'client1', create_date: '2018-09-01', phone: '110' },
      { id: 2, name: 'client2', create_date: '2018-09-01', phone: '110' },
      { id: 3, name: 'client3', create_date: '2018-09-01', phone: '110' },
    ]
  };
  

Mock.mock(/^\/api\/sales_order\/$/, 'get', salesOrderList);
Mock.mock(/\/api\/sales_order\//, 'get', salesOrderRetrieve);
Mock.mock(/\/api\/sales_tasks\//, 'get', salesTaskList);
Mock.mock(/\/api\/sales_profits\//, 'get', salesProfitList);
Mock.mock(/\/api\/sales_values\//, 'get', salesValueList);
Mock.mock(/\/api\/clients\//, 'get', clientList);
