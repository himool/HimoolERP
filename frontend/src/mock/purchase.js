import Mock from 'mockjs'


const supplierList = [
  {
    id: 1, name: 'supplier1', manager: 'manager1', phone: '110', bank_account_name: 'bank_account_name',
    bank_account: 'bank_account', remark: 'remark', bank_name: 'bank_name', address: 'address', status: true, order: 88,
    url: 'url', default_discount: 80, update_date: '2019-09-09',
  },
  {
    id: 2, name: 'supplier2', manager: 'manager2', phone: '112', bank_account_name: 'bank_account_name',
    bank_account: 'bank_account', remark: 'remark', bank_name: 'bank_name', address: 'address', status: true, order: 88,
    url: 'url', default_discount: 80, update_date: '2019-09-09',
  },
];

const purchaseOrderList = {
    "count": 12,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 2,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 3,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 4,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 5,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 6,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 1.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 7,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 2.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 8,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 12.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 9,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-05",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 12.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 10,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-06",
            "remark": "",
            "products": [],
            "is_draft": false
        },
        {
            "id": 11,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-06",
            "remark": "",
            "products": [
                {
                    "name": "goods2",
                    "code": "1002",
                    "spec1": "spec3",
                    "spec2": null,
                    "quantity": 21.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": false
        },
        {
            "id": 12,
            "supplier": 1,
            "supplier_name": "23212312",
            "warehouse": 1,
            "account": 2,
            "amount": 0.0,
            "date": "2020-07-06",
            "remark": "",
            "products": [
                {
                    "name": "goods1",
                    "code": "1001",
                    "spec1": "spec1",
                    "spec2": "spec3",
                    "quantity": 2.0,
                    "purchase_price": 0.0,
                    "discount": 100.0,
                    "discount_price": 0.0,
                    "amount": 0.0,
                    "discount_amount": 0.0
                }
            ],
            "is_draft": true
        }
    ]
};

const changeRecordList = {
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 3,
            "goods_name": "goods2",
            "spec1": "spec5",
            "spec2": "spec4",
            "change_method": "手动修改",
            "before_change": 0.0,
            "after_change": 33.0,
            "operator": "test",
            "relation_order": null
        },
        {
            "id": 2,
            "goods_name": "goods2",
            "spec1": "spec5",
            "spec2": "spec3",
            "change_method": "手动修改",
            "before_change": 12.0,
            "after_change": 33.0,
            "operator": "test",
            "relation_order": null
        },
        {
            "id": 1,
            "goods_name": "goods1",
            "spec1": "spec1",
            "spec2": "spec3",
            "change_method": "手动修改",
            "before_change": 0.0,
            "after_change": 1.0,
            "operator": "test",
            "relation_order": null
        }
    ]
};

const purchaseOrderRetrieve = {
    "id": "PC200720104306239619",
    "supplier": 1,
    "supplier_name": "23212312",
    "warehouse": 2,
    "warehouse_name": "warehouse2",
    "account": 3,
    "account_name": "21312",
    "amount": 0.0,
    "date": "2020-07-19T16:00:00Z",
    "remark": "",
    "products": [
        {
            "product_id": "e9f1996e-c105-11ea-b73e-87e5a1fdee64",
            "name": "goods3",
            "code": "1003",
            "spec1": "spec4",
            "spec2": "spec1",
            "quantity": 1.0,
            "purchase_price": 11.0,
            "discount": 100.0,
            "discount_price": 11.0,
            "amount": 11.0,
            "discount_amount": 11.0
        }
    ],
    "is_draft": false
};

Mock.mock(/\/api\/supplier\//, 'get', supplierList);
Mock.mock(/\/api\/purchase_order\/.+\//, 'get', purchaseOrderRetrieve);
Mock.mock(/\/api\/purchase_order\//, 'get', purchaseOrderList);
Mock.mock(/\/api\/change_records\//, 'get', changeRecordList);
