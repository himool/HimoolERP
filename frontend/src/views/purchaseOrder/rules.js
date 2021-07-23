export let rules = {
  supplier: [{ required: true, message: '请选择供应商', trigger: 'change' }],
  warehouse: [{ required: true, message: '请选择仓库', trigger: 'change' }],
  account: [{ required: true, message: '请选择账户', trigger: 'change' }],
  contacts: [{ required: true, message: '请选择联系人', trigger: 'change' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'change' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
}