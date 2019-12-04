import requests
import abc


class HandlerException(Exception):
    pass


class SmsServiceHandler(metaclass=abc.ABCMeta):
    url = ''
    errors = set()

    def __init__(self, api_key: str, service: str, country_code: int = None):
        self.api_key = api_key
        self.service = service
        self.country_code = country_code

    def send_request(self, payload: dict, parse_json: bool):
        payload['api_key': self.api_key]
        response = requests.get(self.url, params=payload)
        if response.status_code != 200:
            # log request error
            print('request_error ' + response.text)
            raise HandlerException
        if response.text in self.errors:
            # log api method error
            print(payload.get('action') + response.text)
            raise HandlerException
        if parse_json:
            return response.json()
        return response.text

    @abc.abstractmethod
    def get_numbers_count(self) -> int:
        pass

    @abc.abstractmethod
    def get_balance(self) -> float:
        pass

    @abc.abstractmethod
    def get_number(self) -> str:
        pass

    @abc.abstractmethod
    def _get_status(self, operation_id: int) -> str:
        pass

    @abc.abstractmethod
    def _set_status(self, operation_id: int, status: int) -> str:
        pass

    @abc.abstractmethod
    def get_activation_code(self, operation_id: int) -> str:
        pass

    @abc.abstractmethod
    def get_number_price(self) -> float:
        pass

    def check_reg_possibility(self) -> bool:
        return self.get_balance >= self.get_number_price and self.get_numbers_count


class SmsActivateHandler(SmsServiceHandler):
    url = "http://sms-activate.ru/stubs/handler_api.php"
    errors = set('NO_ACTIVATION', 'ERROR_SQL', 'NO_NUMBERS', 'NO_BALANCE', 
                 'BAD_SERVICE', 'BAD_KEY', 'BAD_STATUS', 'BAD_ACTION', 'BANNED')

    def get_numbers_count(self) -> int:
        payload = {
            'action': 'getNumbersStatus'
        }
        if self.country_code is not None:
            payload['country'] = self.country_code
        response = self.send_request(payload, True)
        return response.get(self.service + '_0')

    def get_balance(self):
        payload = {
            'action': 'getBalance'
        }
        response = self.send_request(payload, False)
        return float(response.replace('ACCESS_BALANCE:', ''))

    def get_number(self):
        payload = {
            'action': 'getNumber',
            'service': self.service
        }
        if self.country_code is not None:
            payload['country'] = self.country_code
        response = self.send_request(payload, False).split(':')
        return response[1:]

    def _get_status(self, operation_id):
        payload = {
            'action': 'getStatus',
            'id': operation_id
        }
        return self.send_request(payload, False)
    
    def _set_status(self, operation_id, status):
        payload = {
            'action': 'setStatus',
            'id': operation_id,
            'status': status
        }
        return self.send_request(payload, False)

    def get_number_price(self):
        payload = {
            'service': self.service
        }
        if self.country_code:
            payload['country'] = self.country_code
        response = self.send_request(payload, True)
        if self.country_code:
            response = response.get(str(self.country_code))
        return float(response.get(self.service))

    def get_activation_code(self, operation_id):
        # тут изичная комбинация получения кода из гет статуса
        # и изменения статуса, если код битый, если не уложились
        # в таймаут, но нужно вызвать метод get_number, чтобы узнать начальный статус
        # и посмотреть работу комбинаций get_status set_status на практике, а с чужим апи кеем
        # я не решился это делать
        pass



        
            


    
        
