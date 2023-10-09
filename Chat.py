from retrying import retry  # 需第三方库，需pip进行安装
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

import openai
import time


class crawler:  # 使用爬虫
    def __init__(self):
        self.Email = '3234954174@qq.com'
        self.secret = '9k8VBisKwM!7GDG'
        self.edge_options = Options()
        # self.edge_options.page_load_strategy = 'none'
        # self.edge_options.add_argument('--headless')
        self.driver = webdriver.Edge(options=self.edge_options)
        self.driver.get('https://magic.ninomae.cn/')
        time.sleep(3)

    # @retry(wait_fixed=10, stop_max_attempt_number=1)
    def find(self):
        # 登录
        self.driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(self.Email)

        self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(self.secret)

        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/form/div[3]/button').click()

        time.sleep(3)

        self.driver.find_element(By.XPATH,
                                 '//*[@id="root"]/div/div[4]/div/div[3]/div[2]/form/div/div/textarea').send_keys('你好')

        self.driver.find_element(By.XPATH,
                                 '//*[@id="root"]/div/div[4]/div/div[3]/div[2]/form/div/div/button[2]/div').click()

        target_element = self.driver.find_element(By.CSS_SELECTOR, '.markdown.prose p')

        # 提取元素的文本内容
        extracted_text = target_element.text
        time.sleep(3)

        # 打印提取的文本内容
        print(extracted_text)
        time.sleep(10900)


openai.api_key = 'your api_key'
openai.api_base = 'https://api.chatanywhere.com.cn/v1'  # 可以不需要梯子


class Chat:  # 使用apikey密钥进行连接

    @staticmethod
    def one(message):
        # 示例
        pass

    @staticmethod
    def two(messages):
        """为提供的对话消息创建新的回答 (流式传输)

            Args:
                messages (list): 完整的对话消息
                api_key (str): OpenAI API 密钥

            Returns:
                tuple: (results, error_desc)
                :param messages:
            """
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                stream=True,
            )
            completion = {'role': '', 'content': ''}
            for event in response:
                if event['choices'][0]['finish_reason'] == 'stop':
                    # print(f'收到的完成数据: {completion}')
                    return completion['content']
                for delta_k, delta_v in event['choices'][0]['delta'].items():
                    # print(f'流响应数据: {delta_k} = {delta_v}')
                    completion[delta_k] += delta_v
            messages.append(completion)  # 直接在传入参数 messages 中追加消息
            return True, ''
        except Exception as err:
            return False, f'OpenAI API 异常: {err}'

# if __name__ == '__main__':
#     # messages = [{'role': 'user', 'content': '你好'}]
#     print(Chat().two([{'role': 'user', 'content': '你好'}]))
