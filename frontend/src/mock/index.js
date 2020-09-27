import Mock from 'mockjs'


require('./user');
require('./account');
require('./goods');
require('./warehouse');
require('./purchase');
require('./sales');
require('./report');


Mock.setup({
  timeout: 500,
});
