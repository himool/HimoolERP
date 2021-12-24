export default {
  path: '/contract',
  name: 'contract',
  component: () => import('@/layouts/BaseLayout'),
  redirect: '/contract/my_contract',
  children: [
    {
      path: 'my_contract',
      meta: { title: '我的合同', permission: 'my_contract' },
      component: () => import('@/views/contract/myContract/index'),
    },
    {
      path: 'my_contract_create',
      meta: { title: '我的合同新增', permission: 'my_contract_create' },
      component: () => import('@/views/contract/myContractCreate/index'),
    },
    {
      path: 'my_contract_edit',
      meta: { title: '我的合同编辑', permission: 'my_contract_edit' },
      component: () => import('@/views/contract/myContractEdit/index'),
    },
    {
      path: 'my_contract_detail',
      meta: { title: '我的合同详情', permission: 'my_contract_detail' },
      component: () => import('@/views/contract/myContractDetail/index'),
    },
    {
      path: 'company_contract',
      meta: { title: '公司合同', permission: 'company_contract' },
      component: () => import('@/views/contract/companyContract/index'),
    },
    {
      path: 'company_contract_detail',
      meta: { title: '公司合同详情', permission: 'company_contract_detail' },
      component: () => import('@/views/contract/companyContractDetail/index'),
    },
    {
      path: 'contract_no_search',
      meta: { title: '合同号查询', permission: 'contract_no_search' },
      component: () => import('@/views/contract/contractNoSearch/index'),
    },
    {
      path: 'contract_no_search_detail',
      meta: { title: '合同号查询详情', permission: 'contract_no_search_detail' },
      component: () => import('@/views/contract/contractNoSearchDetail/index'),
    },
    {
      path: 'invoicing_approval',
      meta: { title: '开票审批', permission: 'invoicing_approval' },
      component: () => import('@/views/contract/invoicingApproval/index'),
    },
    {
      path: 'invoicing_approval_stay',
      meta: { title: '开票审批留档', permission: 'invoicing_approval_stay' },
      component: () => import('@/views/contract/invoicingApprovalStay/index'),
    },
    {
      path: 'invoicing_approval_stay_detail',
      meta: { title: '开票审批留档详情', permission: 'invoicing_approval_stay_detail' },
      component: () => import('@/views/contract/invoicingApprovalStayDetail/index'),
    },
    {
      path: 'parts_price',
      meta: { title: '部件价格表', permission: 'parts_price' },
      component: () => import('@/views/contract/partsPrice/index'),
    },
  ],
}