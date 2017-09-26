from setuptools import setup

setup(
    name='yafblog',
    version='0.0.1',
    description='yet another flask blog',
    author='trevorxg',
    author_email='trevorxg@gmail.com',
    license='MIT',
    packages=['yafblog'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'mistune',
        'pygments',
        'pymysql',
        'gunicorn',
    ],
)
