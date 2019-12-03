import pyautogui
import subprocess
import time
import os
from api_handlers import SmsServiceHandler # заменить на фабрику


class Telegram():

    def __init__(self, path: str):
        self.process = subprocess.Popen(path)
        time.sleep(2)
        self._await_resource('start_messaging', 8)
        self.click_button_by_resource('start_messaging')
        time.sleep(0.5)

    def set_proxy(self, proxy):
        pass

    def click_button_by_resource(self, resource):
        pass

    def set_name(self):
        pass

    def _await_resource(self, resource, time_limitation):
        pass

    def set_phone(self, phone):
        pass

    def check_phone(self):
        pass

    def check_proxy(self):
        pass

    def set_code(self):
        pass

    def check_code(self, code):
        pass

    def kill(self):
        pass


class Reger():
    def __init__(self, sms_service: SmsServiceHandler, proxy: str):
        self.sms_service = sms_service
        self.proxy = proxy

    def register_acc(self):
        telegram = Telegram('tg_path')
        telegram.set_proxy(self.proxy)
        telegram.check_proxy()

        if self.sms_service.check_reg_possibility():
            operation_id, phone = self.sms_service.get_number()
            telegram.set_phone(phone)
            telegram.check_phone()

            code = self.sms_service.get_activation_code(operation_id)
            telegram.check_code(code)

            telegram.set_name()
            telegram.kill()

    def after_reg(self):
        # move tdata
        pass
