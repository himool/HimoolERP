from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20210111 import sms_client, models
from extensions.exceptions import ServerError
from tencentcloud.common import credential
import json
from configs.django import SECRET_ID, SECRET_KEY, SMS_SDK_APP_ID, TEMPLATE_ID, SIGN_NAME, REGION


def send_phone_code(phone, code):
    """发送验证码"""

    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        cred = credential.Credential(SECRET_ID, SECRET_KEY)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = 'sms.tencentcloudapi.com'

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = sms_client.SmsClient(cred, REGION, clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.SendSmsRequest()
        params = {
            'PhoneNumberSet': [f'+86{phone}'],
            'SmsSdkAppId': SMS_SDK_APP_ID,
            'SignName': SIGN_NAME,
            'TemplateId': TEMPLATE_ID,
            'TemplateParamSet': [code],
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个SendSmsResponse的实例，与请求对象对应
        client.SendSms(req)
    except TencentCloudSDKException:
        raise ServerError('验证码发送错误')


def run(*args):
    phone = input('手机号: ')
    code = input('验证码: ')
    send_phone_code(phone, code)
