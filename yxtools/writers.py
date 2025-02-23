from ._base import print_cust, makedirs, getLocalTime
from abc import ABC, abstractmethod

import os, csv


'''
classes
'''
class base_writer(ABC):
    def __inti__(self, file:os.PathLike, mode:str='log', **kwargs):
        mode = "." + mode if mode[0] != '.' else mode

        self.flag = False

        if file is None:
            file = './' + getLocalTime(timeFormat=False, show=False) + mode

        dirname = os.path.dirname(file)
        if not os.path.exists(dirname):
            makedirs(dirname)

        self.file_name = os.path.basename(file).split('.')[0]
        if kwargs is not None:
            for i in range(len(kwargs.keys())):
                self.file_name = self.file_name + f'_{list(kwargs.keys())[i]}{list(kwargs.values())[i]}'
        self.renamed_file = self.file_name + mode
        self.file = open(os.path.join(dirname, self.renamed_file), mode='w+', encoding='utf-8')
    
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass
    
    def __del__(self):
        self.file.close()
        # 检查文件是否为空,如果为空则删除
        if os.path.getsize(os.path.join(self.dirname, self.renamed_file)) == 0 or self.flag == False:
            if self.flag == True:
                return 
            os.remove(self.renamed_file)
            print_cust(f"Deleted empty log file: {self.renamed_file}, since it's empty.", 'red')

class writer_log():
    def __init__(self, file:os.PathLike=None, **kwargs) -> None:
        
        if file is None:
            file = './' + getLocalTime(timeFormat=False, show=False) + '.log'

        self.flag = False

        self.dirname = os.path.dirname(file)
        if not os.path.exists(self.dirname):
            makedirs(self.dirname)

        self.file_name = os.path.basename(file).split('.')[0]
        if kwargs is not None:
            for i in range(len(kwargs.keys())):
                self.file_name = self.file_name + f'_{list(kwargs.keys())[i]}{list(kwargs.values())[i]}'
        self.renamed_file = self.file_name + '.log'
        
        self.file = open(os.path.join(self.dirname, self.renamed_file), mode='w+', encoding='utf-8')
        print_cust(f"Your Logger is saved at {os.path.abspath(self.renamed_file)}!", 'green')

    def __call__(self, info):
        print(info)
        self.file.write(info+'\n')
        self.file.flush()
    
    def __del__(self):
        self.file.close()
        # 检查文件是否为空,如果为空则删除
        if os.path.getsize(os.path.join(self.dirname, self.renamed_file)) == 0 or self.flag == False:
            if self.flag == True:
                return 
            os.remove(os.path.join(self.dirname, self.renamed_file))
            print_cust(f"Deleted empty log file: {self.renamed_file}, since it's empty.", 'red')

    def module_info(self, info):
        info = "-------------------------"+info+"-------------------------"
        print(info)
        self.file.write(info+'\n')
        self.file.flush()

class writer_csv():
    def __init__(self, head:list, file=None, **kwargs):
        if file is None:
            file = './' + getLocalTime(timeFormat=False, show=False) + '.csv'

        self.dirname = os.path.dirname(file)
        if not os.path.exists(self.dirname):
            makedirs(self.dirname)

        self.file_name = os.path.basename(file).split('.')[0]
        if kwargs is not None:
            for i in range(len(kwargs.keys())):
                self.file_name = self.file_name + f'_{list(kwargs.keys())[i]}{list(kwargs.values())[i]}'
        self.renamed_file = self.file_name + '.csv'
        
        self.file = open(os.path.join(self.dirname, self.renamed_file), mode='w+', encoding='utf-8')
        print_cust(f"Your csv is saved at {os.path.abspath(self.renamed_file)}!", 'green')
        self.writer = csv.writer(self.file)
        self.writer.writerow(head)
    
    def __call__(self, result:list, show=False):
        if show:
            print_cust(result)
        self.writer.writerow(result)
        self.file.flush()
    
    def __del__(self):
        self.file.close()
        # 检查文件是否为空,如果为空则删除
        if os.path.getsize(os.path.join(self.dirname, self.renamed_file)) == 0 or self.flag == False:
            if self.flag == True:
                return 
            os.remove(os.path.join(self.dirname, self.renamed_file))
            print_cust(f"Deleted empty log file: {self.renamed_file}, since it's empty.", 'red')

if __name__ == '__main__':
    pass