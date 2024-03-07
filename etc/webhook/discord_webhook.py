import requests
from config import discord_webhook


def send_webhook(path, method, exc):
    data = {
        'username': 'Server Error',
        'embeds': [
            {
                'color': 15548997,
                'title': 'Uncaught Exception',
                'description': '예기치 못한 프로그램 에러가 발생하여 요청을 정상적으로 수행하지 못했습니다.',
                'fields': [
                    {
                        'name': 'Path',
                        'value': str(path),
                        'inline': True
                    },
                    {
                        'name': 'Method',
                        'value': str(method),
                        'inline': True
                    },
                    {
                        'name': 'Exception',
                        'value': str(exc)
                    }
                ]
            }
        ]
    }

    requests.post(discord_webhook.URL, json=data)
