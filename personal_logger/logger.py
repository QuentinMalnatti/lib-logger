from typing import Type
from datetime import datetime


class LoggerBase(object):

    def __init__(self, component):
        self.__component = component

    def print_timed_message(self, msg: str):
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {self.__component} | {msg}")

    def print_stage(self, stage: str):
        log_msg = f"> Start {stage}..."
        self.print_timed_message(msg=log_msg)

    def print_success(self, msg: str):
        log_msg = f"[SUCCESS] {msg}"
        self.print_timed_message(msg=log_msg)

    def print_fail(self, msg: str):
        log_msg = f"[FAIL] {msg}"
        self.print_timed_message(msg=log_msg)

    @staticmethod
    def define_error_msg(msg: str) -> str:
        return f"[ERROR] {msg}"

    def print_error(self, msg: str):
        log_msg = self.define_error_msg(msg=msg)
        self.print_timed_message(msg=log_msg)

    def handle_fail(self, stage: str, to_raise: bool, error_msg: str = None):
        self.print_fail(msg=stage)
        if error_msg:
            if to_raise:
                raise Exception(self.define_error_msg(msg=error_msg))
            self.print_error(msg=error_msg)


class LoggerDecorator(object):

    def __init__(self, component):
        self.__logger_base = LoggerBase(component=component)

    def get_logger_base(self):
        return self.__logger_base

    def log(self, stage: str):
        def decorator(func):
            def inner(*args, **kwargs):
                self.__logger_base.print_stage(stage=stage)
                func(*args, **kwargs)
                self.__logger_base.print_success(msg=stage)

            return inner

        return decorator

    def log_success_as_success(self, stage: str, exception_to_catch: Type[Exception], error_msg: str = None, to_raise: bool = False):
        def decorator(func):
            def inner(*args, **kwargs):
                self.__logger_base.print_stage(stage=stage)
                try:
                    func(*args, **kwargs)
                    self.__logger_base.print_success(msg=stage)
                except exception_to_catch as e:
                    print(e)
                    self.__logger_base.handle_fail(stage=stage, error_msg=error_msg, to_raise=to_raise)

            return inner

        return decorator

    def log_fail_as_success(self, stage: str, exception_to_catch: Type[Exception], error_msg: str = None, to_raise: bool = False):
        def decorator(func):
            def inner(*args, **kwargs):
                self.__logger_base.print_stage(stage=stage)
                try:
                    func(*args, **kwargs)
                    self.__logger_base.handle_fail(stage=stage, error_msg=error_msg, to_raise=to_raise)
                except exception_to_catch:
                    self.__logger_base.print_success(msg=stage)

            return inner

        return decorator
