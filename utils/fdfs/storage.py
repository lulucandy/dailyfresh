from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client

class FDFSStorage(Storage):
    def __init__(self, client_conf=None, base_url=None):
        '''初始化'''
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url 

    def _open(self,name,mode='rb'):
        pass
    def _save(self,name,content):
        #创建对象
        client = Fdfs_client(self.client_conf)
        #上传文件
        res = client.upload_by_buffer(content.read())
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fast dfs失败')

        # 获取返回的文件ID
        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):
        '''Django判断文件名是否可用'''
        return False

    def url(self, name):
        '''返回访问文件的url路径'''
        return self.base_url+name
    