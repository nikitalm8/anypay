import os
import codecs

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as file:

    long_description = "\n" + file.read()

VERSION = '1.1.0'
DESCRIPTION = 'Asynchronous AnyPay API wrapper'

setup(
    name="anypay",
    version=VERSION,
    author="Nikita Minaev",
    author_email="<nikita@minaev.su>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['httpx', 'pydantic'],
    keywords=['python', 'anypay', 'payments', 'anypay-api', 'async', 'asyncio'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    url='https://github.com/nikitalm8/anypay',
    project_urls={
        'Homepage': 'https://github.com/nikitalm8/anypay',
        'Bug Tracker': 'https://github.com/nikitalm8/anypay/issues',
        'API Docs': 'https://anypay.io/doc/api',
    },
)