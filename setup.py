# setup.py
from setuptools import setup, find_packages


setup(
    name='PyroArgs',
    version='1.1',  # ВЕРСИЯ
    description='Удобная обработка аргументов команд для Pyrogram',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='vo0ov',
    author_email='artgr123@yandex.ru',
    url='https://github.com/vo0ov/TG-UserBot',
    packages=find_packages(),
    install_requires=[
        'pyrogram>=2.0.0',
        'TgCrypto>=1.2.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
