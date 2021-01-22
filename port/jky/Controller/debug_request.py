import pytest


class Debug_Step:
    def setup_class(self):
        self.data = None
        print('每次调试都要执行这里')

    def test_case(self):
        print('this is pass')
