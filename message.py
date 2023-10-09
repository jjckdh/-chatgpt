from alibabacloud_aligenieiap_1_0.client import Client as AliGenieiap_1_0Client
from alibabacloud_aligenieiap_1_0.models import PushNotificationsRequestNotificationUnicastRequest, \
    PushNotificationsRequestTenantInfo, PushNotificationsRequestNotificationUnicastRequestSendTarget
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_aligenieiap_1_0 import models as ali_genieiap__1__0_models
import requests
import json
from urllib import parse
import frida
import time


class Aligenie:
    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> AliGenieiap_1_0Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'openapi.aligenie.com'
        return AliGenieiap_1_0Client(config)

    @staticmethod
    def push_message(content):
        client = Aligenie.create_client('access_key_id', 'access_key_secret')
        notificationUnicastRequest = PushNotificationsRequestNotificationUnicastRequest()
        notificationUnicastRequest.encode_key = "98223"
        notificationUnicastRequest.encode_type = "SKILL_ID"
        notificationUnicastRequest.organization_id = "1398082853812549793"
        place_holder = {'content': content}
        notificationUnicastRequest.place_holder = place_holder
        notificationUnicastRequest.message_template_id = "2DPRcMi97Qiwofsj"
        notificationUnicastRequest.is_debug = True
        requestSendTarget = PushNotificationsRequestNotificationUnicastRequestSendTarget()
        requestSendTarget.target_type = 'DEVICE_OPEN_ID'
        requestSendTarget.target_identity = 'JqyRCF91nuWRCTdk5dbOKVjRWMRBzL2jjI+xkIG3U2gLVoH5nvRw9w=='
        notificationUnicastRequest.send_target = requestSendTarget
        requestTenantInfo = PushNotificationsRequestTenantInfo()
        push_notifications_request = ali_genieiap__1__0_models.PushNotificationsRequest(notificationUnicastRequest,
                                                                                        requestTenantInfo)
        try:
            response = client.push_notifications(push_notifications_request)
            print(response)
        except Exception as err:
            print(err)


class AliGenieFrida:
    def __init__(self):
        self.last_timestamp = int(time.time())

    def get_frida_rpc_script(self):
        js = open('tmjl.js', 'r', encoding='utf-8').read()

        session = frida.get_usb_device().attach("com.alibaba.ailabs.tg")

        script = session.create_script(js)
        script.load()
        return script

    @property
    def get_data(self):
        for _ in range(2):
            try:
                # 换成抓包的data
                data = '{"limit":"10","uuid":"uuid","deviceInfo":"{' \
                       '\\"bizGroup\\":\\"X1\\",' \
                       '\\"bizType\\":\\"AILABS\\",\\"botId\\":10,' \
                       '\\"uuid\\":\\"uuid\\"}",' \
                       '"authInfo":"{\\"accessToken\\":\\"2zyAfPN+bJdMzh5dUtiWqDtLLL/KnlYJCjsMujjz' \
                       '+xYeTwqhbS2JvHGWAg7K' \
                       '+nTyip' \
                       '/vBXf83wZXe+wBdmHUWqs8OhxFYToW\\",\\"deviceIds\\":[],\\"isAuthenticated\\":false,' \
                       '\\"isNew\\":true,' \
                       '\\"isTempUser\\":false,\\"userId\\":\\"userId\\",' \
                       '\\"utdId\\":\\"ZGOM/fF/pVkDADEloBB6B5tx\\"}"}'
                api = 'mtop.alibaba.aicloud.index.listsentences'
                appKey = '23904773'

                timestamp = str(int(time.time()))
                res = json.loads(self.get_frida_rpc_script().exports.callgetsign(data, timestamp, api, appKey))
                res['timestamp'] = timestamp
                res['x-sgext'] = parse.quote(res['x-sgext'])
                res['x-mini-wua'] = parse.quote(res['x-mini-wua'])
                res['x-sign'] = parse.quote(res['x-sign'])
                res['x-t'] = parse.quote(res['timestamp'])
                requests.get("http://43.142.90.87:8610/rs?key=sign&vaule=" + json.dumps(res) + "&time_out=100")
                # print("调用frida获取", res)

                headers = {'x-sid': 'sid', 'x-uid': 'uid', 'x-nettype': 'WIFI', 'x-pv': '6.3', 'x-nq': 'WIFI',
                           'x-features': '27', 'x-app-conf-v': '0',
                           'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                           'cache-control': 'no-cache', 'x-t': res['timestamp'], 'x-bx-version': '6.5.24',
                           'f-refer': 'mtop', 'x-extdata': 'openappkey%3DDEFAULT_AUTH',
                           'x-ttid': '702008%40genieapp_android_6.0.1', 'x-app-ver': '6.0.1',
                           'x-c-traceid': 'ZGOM%2FfF%2FpVkDADEloBB6B5tx1684334633416073015885',
                           'x-umt': 'GI8Bdk5LPPgZIwKIJIE1O6HP%2F11f01e2', 'x-utdid': 'ZGOM%2FfF%2FpVkDADEloBB6B5tx',
                           'x-appkey': '23904773', 'x-devid': 'Amqv8wxkiFMLQwGHcw6DOrRUeg7B3s693f8iah0kXC6E',
                           'user-agent': 'MTOPSDK%2F3.1.1.7+%28Android%3B8.1.0%3BGoogle%3BPixel%29',
                           'Host': 'acs.m.taobao.com', 'x-sgext': res['x-sgext'], 'x-mini-wua': res['x-mini-wua'],
                           'x-sign': res['x-sign']}

                params = {
                    'data': data,
                }
                response = requests.get(
                    'https://acs.m.taobao.com/gw/mtop.alibaba.aicloud.index.listsentences/1.0/',
                    params=params,
                    headers=headers,
                ).json()

                # print(response)
                for _ in response['data']['model']:
                    if _['query'] != '' and _['cateName'] == '百科':
                        return _
                return response['data']['model'][0]
            except Exception as e:
                print(e)
