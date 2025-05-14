#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from alibabacloud_dysmsapi20170525 import models as dysmsapi_models
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models

from config import *


def send_sms(phone_number, code):
    # 配置客户端
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    config.endpoint = 'dysmsapi.aliyuncs.com'
    client = Dysmsapi20170525Client(config)

    # 构造请求
    send_request = dysmsapi_models.SendSmsRequest(
        phone_numbers=phone_number,
        sign_name=sign_name,
        template_code=template_code,
        template_param=f'{{"code":"{code}"}}'
    )

    try:
        # 发送请求
        response = client.send_sms(send_request)
        if response.body.code == 'OK':
            print("短信发送成功")
            return True
        else:
            print(f"短信发送失败: {response.body.message}")
    except Exception as e:
        print(f"发送短信时出错: {e}")


if __name__ == '__main__':
    # 使用示例
    send_sms('13800138000', '123456')  # 手机号和验证码
