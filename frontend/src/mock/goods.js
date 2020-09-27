import Mock from 'mockjs'


const categoryList = [
  { id: 1, name: 'category1', description: 'category1 xxx xxx xxx xxx xxx', goods_quantity: 5, product_quantity: 7, order: 100 },
  { id: 2, name: 'category2', description: 'category1 xxx xxx xxx xxx xxx', goods_quantity: 5, product_quantity: 7, order: 100 },
  { id: 3, name: 'category3', description: 'category1 xxx xxx xxx xxx xxx', goods_quantity: 5, product_quantity: 7, order: 100 },
  { id: 4, name: 'category4', description: 'category1 xxx xxx xxx xxx xxx', goods_quantity: 5, product_quantity: 7, order: 100 },
  { id: 5, name: 'category5', description: 'category1 xxx xxx xxx xxx xxx', goods_quantity: 5, product_quantity: 7, order: 100 },
];


const goodsList = {
  count: 99,
  results: [
    {
      id: 1, name: 'goods1', code: 10001, suggested_retail_price: 10, retail_price: 12, order: 100, status: true,
      brand_name: 'brand1', category_name: 'category1', products: [
        { id: 1, goods: 1, spec1: 1, spec1_name: 'spec1_name', spec2: 2, spec2_name: 'spec2_name', purchase_price: 55 },
        { id: 2, goods: 1, spec1: 3, spec1_name: 'spec3_name', spec2: 4, spec2_name: 'spec4_name', purchase_price: 55 },
      ]
    },
  ],
}

Mock.mock(/\/api\/goods\//, 'get', goodsList);
Mock.mock(/\/api\/categories\//, 'get', categoryList);