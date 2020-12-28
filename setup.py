import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-cache-page-per-user',
    version='0.1.0',
    author='Boris Trubin',
    author_email='mgbit3214@gmail.com',
    keywords=[
        'Django',
        'Django Cache',
        'cache_page',
        'Django Cache Page Per User',
        'Django Cache Page Per Language',
        'Django Cache View Per User',
    ],
    description='decorator for view caching per user and per language',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/chessmaster04/django-cache-page-per-user',
    download_url='',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    test_suite='runtests.runtests',
)
