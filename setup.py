import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-cache-page-per-user',
    version='0.1.0',
    author='Boris',
    author_email='@gmail.com',
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
    url='',
    download_url='',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    test_suite='runtests.runtests',
)
