import re
from setuptools import setup

with open('pt/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)


setup(
    name='pt',
    version=version,
    url='https://github.com/xyz71148/pt.git',
    license='MIT',
    author='tommy',
    author_email='xyz71148@gmail.com',
    description='pt',
    long_description=__doc__,
    packages=[
        'pt',
        'pt.libs',
        'pt.libs.block_chain',
        'pt.libs.flask_httpauth',
        'pt.libs.flask_jwt',
        'pt.libs.payment',
        'pt.apps.gcp'
    ],
    zip_safe=False,
    platforms='any',
    install_requires=[],
    tests_require=[
        'coverage'
    ],
    test_suite='test_pt',
    entry_points={
        'console_scripts': [
            'pt=pt.cmd:main'
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
