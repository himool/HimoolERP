import Mock from 'mockjs'


const roleList = [
  { id: 1, name: 'role1', remark: 'remark', permissions: [] },
  { id: 2, name: 'role2', remark: 'remark', permissions: [] },
  { id: 3, name: 'role2', remark: 'remark', permissions: [] },
];

const subuserList = [
  { id: 1, username: 'role1', create_date: '2018-09-01', roles: [2], role_names: ['role1', 'role2'] },
  { id: 2, username: 'role2', create_date: '2018-09-01', roles: [], role_names: [] },
  { id: 3, username: 'role2', create_date: '2018-09-01', roles: [], role_names: [] },
];

const accountList = [
  {
    id: 1, name: 'account1', account: 'account1', holder: '11', warehouse: 1,
    warehouse_name: 'warehouse', status: true, order: 88, remark: '', type: '现金'
  },
  {
    id: 2, name: 'account2', account: 'account2', holder: '22', warehouse: 1,
    warehouse_name: 'warehouse', status: true, order: 88, remark: '', type: '现金'
  },
];

const sellerList = ['user1', 'user2'];

const bookkeepingList = {
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
      {
          "id": 2,
          "create_datetime": "2020-07-12T14:34:10.605699Z",
          "account": 2,
          "account_name": "结算账户1",
          "amount": 12.0,
          "recorder": "test",
          "remark": "33333232"
      },
      {
          "id": 1,
          "create_datetime": "2020-07-12T14:33:58.019664Z",
          "account": 1,
          "account_name": "1212",
          "amount": 12.0,
          "recorder": "11",
          "remark": "3232"
      }
  ]
};

const statisticalAccount = {
  revenue: 20,
  expenditure: 30,
}

Mock.mock(/\/api\/roles\//, 'get', roleList);
Mock.mock(/\/api\/subusers\//, 'get', subuserList);
Mock.mock(/\/api\/accounts\//, 'get', accountList);
Mock.mock(/\/api\/sellers\//, 'get', sellerList);
Mock.mock(/\/api\/bookkeeping\//, 'get', bookkeepingList);
Mock.mock(/\/api\/statistical_account\//, 'get', statisticalAccount);
Mock.mock(/\/api\/users\//, 'get', ["test", "user1", "user2"]);
