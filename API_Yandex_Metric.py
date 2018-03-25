# Домашнее задание к лекции 3.4 «Работа с классами на примере API Yandex Метрика»
# Создайте страничку с помощью GitHub Pages.
# Установите счётчик.
# Реализуйте класс доступа к API Яндекс.Метрика, который принимает токен и предоставляет информацию о визитах,
# просмотрах и посетителях.

import requests

# APP_ID = '5c1cd4f979aa4b288d0f4e152170bc57'
# AUTH_URL = 'https://oauth.yandex.ru/authorize'
#
# auth_data = {
#     'response_type': 'token',
#     'client_id': APP_ID
# }
#
# print('?'.join((AUTH_URL, urlencode(auth_data))))


TOKEN = 'AQAAAAAkeuXLAATpCMvoJYmYgkU1idtl-XKEfaU'

params = {
    'oauth_token': TOKEN,
    'pretty': 1
}
# reponse = requests.get('https://api-metrika.yandex.ru/management/v1/counters', params)
# counter_id = reponse.json()['counters'][0]['id']
# print(counter_id)


class YAMetrica:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_counters(self):
        headers = self.get_headers()
        reponse = requests.get('https://api-metrika.yandex.ru/management/v1/counters', params, headers=headers)
        return [c['id'] for c in reponse.json()['counters']]

    def get_metric(self, counter_id, metric):
        params = {
            'id': counter_id,
            'metrics': metric
        }
        headers = self.get_headers()
        reponse = requests.get('https://api-metrika.yandex.ru/stat/v1/data', params, headers=headers)
        try:
            return reponse.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e

    @property
    def get_stat(self):
        counters = self.get_counters()
        for counter in counters:
            print('Метрика :', counter)
            print('Суммарное количество визитов :', self.get_metric(counter, 'ym:s:visits'))
            print('Число просмотров страниц на сайте за отчетный период :', self.get_metric(counter, 'ym:s:pageviews'))
            print('Количество уникальных посетителей. :', self.get_metric(counter, 'ym:s:users'))
            print('-------------------------------------------------------')
            return 0


A = YAMetrica(TOKEN)
A.get_stat
