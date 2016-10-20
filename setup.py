from setuptools import setup

setup(
    name='pyvk',
    version='0.0.1',
    platforms='any',
    packages=['pyvk'],

    install_requires=[
        'requests',
        'lxml',
        'appdirs',
    ],

    tests_require=[
        'mock',
        'pytest',
        'pytest-cov',
    ],

    author='Max Kuznetsov',
    author_email='maks.kuznetsov@gmail.com',
    description='VK API for Python',
    license='MIT',
    url='https://github.com/mkuznets/PyVK',

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
