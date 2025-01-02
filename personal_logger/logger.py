from typing import Type
from datetime import datetime


class LoggerBase(object):
    @staticmethod
    def print_timed_message(msg: str):
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {msg}")

    @classmethod
    def print_stage(cls, stage: str):
        log_msg = f"> Start {stage}..."
        cls.print_timed_message(msg=log_msg)

    @classmethod
    def print_success(cls, msg: str):
        log_msg = f"[SUCCESS] {msg}"
        cls.print_timed_message(msg=log_msg)

    @classmethod
    def print_fail(cls, msg: str):
        log_msg = f"[FAIL] {msg}"
        cls.print_timed_message(msg=log_msg)

    @staticmethod
    def define_error_msg(msg: str) -> str:
        return f"[ERROR] {msg}"

    @classmethod
    def print_error(cls, msg: str):
        log_msg = cls.define_error_msg(msg=msg)
        cls.print_timed_message(msg=log_msg)

    @classmethod
    def handle_fail(cls, stage: str, to_raise: bool, error_msg: str = None):
        cls.print_fail(msg=stage)
        if error_msg:
            if to_raise:
                raise Exception(cls.define_error_msg(msg=error_msg))
            cls.print_error(msg=error_msg)


class LoggerDecorator(object):
    @classmethod
    def log(cls, stage: str):
        def decorator(func):
            def inner(*args, **kwargs):
                LoggerBase.print_stage(stage=stage)
                func(*args, **kwargs)
                LoggerBase.print_success(msg=stage)

            return inner

        return decorator

    @classmethod
    def log_success_as_success(cls, stage: str, exception_to_catch: Type[Exception], error_msg: str = None, to_raise: bool = False):
        def decorator(func):
            def inner(*args, **kwargs):
                LoggerBase.print_stage(stage=stage)
                try:
                    func(*args, **kwargs)
                    LoggerBase.print_success(msg=stage)
                except exception_to_catch as e:
                    print(e)
                    LoggerBase.handle_fail(stage=stage, error_msg=error_msg, to_raise=to_raise)

            return inner

        return decorator

    @classmethod
    def log_fail_as_success(cls, stage: str, exception_to_catch: Type[Exception], error_msg: str = None, to_raise: bool = False):
        def decorator(func):
            def inner(*args, **kwargs):
                LoggerBase.print_stage(stage=stage)
                try:
                    func(*args, **kwargs)
                    LoggerBase.handle_fail(stage=stage, error_msg=error_msg, to_raise=to_raise)
                except exception_to_catch:
                    LoggerBase.print_success(msg=stage)

            return inner

        return decorator
