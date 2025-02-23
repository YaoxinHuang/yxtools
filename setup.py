from setuptools import setup, find_packages

setup(
    name='yaoxin_tools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # 列出你的工具包依赖的其他包
        'numpy==1.24.0',
        'pillow',
        'SimpleITK'
    ],
)