# encoding: utf-8

import os
#from types import UnicodeType
from .device import BaseDevice
from .vfs import VfsDevice
try:
    from types import UnicodeType
except ImportError:
    UnicodeType = None

class MirrorDevice(BaseDevice):

    def __init__(self, name, title='', root_paths=None, options={}):
        self.name = name
        self.title = title
        self.options = options
        # 读取环境变量  VFS_xxx 做为环境变量
        root_paths = root_paths or os.environ['VFS_' + self.name.upper()]
        self.vfs_devices = []
        for index, root_path in enumerate(root_paths.split(';')):
            self.vfs_devices.append(VfsDevice(name + str(index), title + str(index), root_path=root_path))

    def os_path(self, key):
        """ 找到key在操作系统中的地址 """
        return self.vfs_devices[0].os_path(key)

    def gen_key(self, prefix='', suffix=''):
        """
        使用uuid生成一个未使用的key, 生成随机的两级目录
        :param prefix: 可选前缀
        :param suffix: 可选后缀
        :return: 设备唯一的key
        """
        return self.vfs_devices[0].gen_key(prefix, suffix)

    def exists(self, key):
        return self.vfs_devices[0].exists(key)

    def get_data(self, key, offset=0, size=-1):
        """ 根据key返回文件内容，适合小文件 """
        return self.vfs_devices[0].get_data(key, offset, size)

    def multiput_new(self, key, size=-1):
        """ 开始一个多次写入会话, 返回会话ID"""
        results = []
        for device in self.vfs_devices:
            results.append(device.multiput_new(key, size))
        return results[0]

    def multiput_offset(self, session_id):
        """ 某个文件当前上传位置 """
        return self.vfs_devices[0].multiput_offset(session_id)

    def multiput(self, session_id, data, offset=None):
        """ 从offset处写入数据 """
        results = []
        for device in self.vfs_devices:
            results.append(device.multiput(session_id, data, offset))
        return results[0]

    def multiput_save(self, session_id):
        """ 某个文件当前上传位置 """
        results = []
        for device in self.vfs_devices:
            results.append(device.multiput_save(session_id))
        return results[0]

    def multiput_delete(self, session_id):
        """ 删除一个写入会话 """
        results = []
        for device in self.vfs_devices:
            results.append(device.multiput_delete(session_id))
        return results[0]

    def put_data(self, key, data):
        """ 直接存储一个数据，适合小文件 """
        results = []
        for device in self.vfs_devices:
            results.append(device.put_data(key, data))
        return results[0]

    def put_stream(self, key, stream, size=-1):
        """ 流式上传 """
        results = []
        for device in self.vfs_devices:
            results.append(device.put_stream(key, stream, size))
        return results[0]

    def remove(self, key):
        """ 删除key文件 """
        results = []
        for device in self.vfs_devices:
            results.append(device.remove(key))
        return results[0]

    def rmdir(self, key):
        """ 删除key文件夹"""
        results = []
        for device in self.vfs_devices:
            results.append(device.rmdir(key))
        return results[0]

    def move(self, key, new_key):
        """ 升级旧的key，更换为一个新的 """
        results = []
        for device in self.vfs_devices:
            results.append(device.move(key, new_key))
        return results[0]

    def copy_data(self, from_key, to_key):
        results = []
        for device in self.vfs_devices:
            results.append(device.copy_data(from_key, to_key))
        return results[0]

    def stat(self, key):
        return self.vfs_devices[0].stat(key)

