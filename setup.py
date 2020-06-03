import re
from setuptools import setup

with open('pt/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        f.read(), re.MULTILINE).group(1)

setup(
    name='pt-py',
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
        'pt.apps.gcp',
        'pt.apps.ws',
        'pt.apps.chat',
        'pt.apps.chat.templates',
        'pt.apps.server',
        #'pt.apps.flask-app'
    ],
    package_data={
        "pt": ["apps/chat/templates/*.html"]
    },
    zip_safe=False,
    platforms='any',
    install_requires=[
        "simplejson",
        "requests",
        "flask",
        "setuptools==40.3.0",
        "google-api-python-client",
        "gunicorn"
    ],
    tests_require=[
        'coverage'
    ],
    test_suite='test_pt',
    entry_points={
        'console_scripts': [
            'pt=pt.cmd:main',
            #'pt-app=pt.apps.flask-app.server:create_app'
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
