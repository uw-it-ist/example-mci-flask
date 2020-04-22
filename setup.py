from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='my-flask-app',
    version='1.0',
    long_description=readme(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'gunicorn', 'flask-caching', 'redis', 'whitenoise', 'psycopg2-binary', 'requests'],
    setup_requires=('pytest-runner'),
    tests_require=('pytest', 'pytest-flake8', 'pytest-cov', 'pytest-flask'),
)
