import re

from setuptools import setup

with open("pyvk/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='pyvk',
    version=version,
    platforms='any',
    packages=['pyvk'],
    install_requires=['requests', 'lxml', 'appdirs',],
    author='Max Kuznetsov',
    author_email='maks.kuznetsov@gmail.com',
    description='VK API for Python',
    license='MIT',
    url='https://github.com/mkuznets/pyvk',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
    ],
)
