from setuptools import setup, find_packages

setup(
    name='yxtools',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        # 列出你的工具包依赖的其他包
        'numpy',
        'pillow',
        'SimpleITK',
        'scipy'
    ],
)