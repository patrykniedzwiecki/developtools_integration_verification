import sys
import typing
import os
import glob
from pathlib import Path
from typing import *

def unit_adaptive(size: int) -> str:
    unit_list = ["Byte", "KB", "MB", "GB"]
    index = 0
    while index < len(unit_list) and size >= 1024:
        size /= 1024
        index += 1
    if index == len(unit_list):
        index = len(unit_list)-1
        size *= 1024
    return str(round(size,2))+unit_list[index]

class BasicTool:
    @classmethod
    def find_all_files(cls, folder: str, real_path: bool = True, apply_abs: bool = True, de_duplicate: bool = True,
                       p_filter: typing.Callable = lambda x: True) -> list:
        filepath_list = set()
        for root, _, file_names in os.walk(folder):
            filepath_list.update(
                [os.path.abspath(os.path.realpath(
                    os.path.join(root, f) if real_path else os.path.join(root, f))) if apply_abs else os.path.relpath(
                    os.path.realpath(os.path.join(root, f) if real_path else os.path.join(root, f))) for f in file_names
                 if p_filter(os.path.join(root, f))])
        if de_duplicate:
            filepath_list = set(filepath_list)
        filepath_list = sorted(filepath_list, key=str.lower)
        return filepath_list

    @classmethod
    def get_abs_path(cls, path: str) -> str:
        return os.path.abspath(os.path.expanduser(path))
    
    @classmethod
    def execute(cls, cmd: str, post_processor: Callable[[Text], Text] = lambda x:x) -> Any:
        """
        封装popen，返回标准输出的列表
        :param post_processor: 对执行结果进行处理
        :param cmd: 待执行的命令
        :return: 经处理过后的字符串列表

        """
        output = os.popen(cmd).read()
        output = post_processor(output)
        return output


if __name__ == '__main__':
    for i in BasicTool.find_all_files(".", apply_abs=False):
        print(i)