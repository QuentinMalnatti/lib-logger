from personal_logger.logger import LoggerDecorator


log_dec_for_test = LoggerDecorator("test")


class LoggerDecoratorTest(object):

    @log_dec_for_test.log_success_as_success(
        stage="test success as success (a = 1)",
        exception_to_catch=ZeroDivisionError,
        error_msg="fail test success as success",
        to_raise=True
    )
    def run_success_as_success(self):
        a = 1

    @log_dec_for_test.log_success_as_success(
        stage="test raise error success as success (a = 1/0)",
        exception_to_catch=ZeroDivisionError,
        error_msg="fail test success as success",
        to_raise=False
    )
    def run_success_as_success_ko(self):
        a = 1/0

    @log_dec_for_test.log_fail_as_success(
        stage="test fail as success (a = 1/0)",
        exception_to_catch=ZeroDivisionError,
        error_msg="fail test fail as success",
        to_raise=True
    )
    def run_fail_as_success(self):
        a = 1/0

    @log_dec_for_test.log_fail_as_success(
        stage="test raise error fail as success (a = 1)",
        exception_to_catch=TypeError,
        error_msg="fail test fail as success",
        to_raise=False
    )
    def run_fail_as_success_ko(self):
        a = 1


if __name__ == "__main__":
    test_logger_decorator = LoggerDecoratorTest()
    test_logger_decorator.run_success_as_success()
    test_logger_decorator.run_success_as_success_ko()
    test_logger_decorator.run_fail_as_success()
    test_logger_decorator.run_fail_as_success_ko()
