from typing import Type
from datetime import datetime


class LoggerDecorator(object):
    @staticmethod
    def __print_timed_message(msg: str):
        print(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | {msg}")

    @classmethod
    def __print_stage(cls, stage: str):
        log_msg = f"> Start {stage}..."
        cls.__print_timed_message(msg=log_msg)

    @classmethod
    def __print_success(cls, msg: str):
        log_msg = f"[OK] {msg}"
        cls.__print_timed_message(msg=log_msg)

    @classmethod
    def __print_fail(cls, msg: str):
        log_msg = f"[KO] {msg}"
        cls.__print_timed_message(msg=log_msg)

    @staticmethod
    def __define_error_msg(msg: str) -> str:
        return f"[ERROR] {msg}"

    @classmethod
    def __print_error(cls, msg: str):
        log_msg = cls.__define_error_msg(msg=msg)
        cls.__print_timed_message(msg=log_msg)

    @classmethod
    def __handle_fail(cls, stage: str, to_raise: bool, error_msg: str = None):
        cls.__print_fail(msg=stage)
        if error_msg:
            if to_raise:
                raise Exception(cls.__define_error_msg(msg=error_msg))
            cls.__print_error(msg=error_msg)

    @classmethod
    def log(cls, stage: str):
        def decorator(func):
            def inner(*args, **kwargs):
                cls.__print_stage(stage=stage)
                func(*args, **kwargs)
                cls.__print_success(msg=stage)

            return inner

        return decorator

    @classmethod
    def log_success_as_success(cls, stage: str, exception_to_catch: Type[Exception], error_msg: str = None, to_raise: bool = False):
        def decorator(func):
            def inner(*args, **kwargs):
                cls.__print_stage(stage=stage)
                try:
                    func(*args, **kwargs)
                    cls.__print_success(msg=stage)
                except exception_to_catch as e:
                    print(e)
                    cls.__handle_fail(stage=stage, error_msg=error_msg, to_raise=to_raise)

            return inner

        return decorator

    @classmethod
    def log_fail_as_success(cls, stage: str, exception_to_catch: Type[Exception], error_msg: str = None, to_raise: bool = False):
        def decorator(func):
            def inner(*args, **kwargs):
                cls.__print_stage(stage=stage)
                try:
                    func(*args, **kwargs)
                    cls.__handle_fail(stage=stage, error_msg=error_msg, to_raise=to_raise)
                except exception_to_catch:
                    cls.__print_success(msg=stage)

            return inner

        return decorator
