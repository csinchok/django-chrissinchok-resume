from setuptools import setup, find_packages

setup(
    name = "django-chrissinchok-resume",
    version = "1.0",
    url = 'https://chrissinchok.com',
    license = 'BSD',
    description = "a small app to manage my resume",
    author = 'Chris Sinchok',
    packages = find_packages('resume'),
    package_dir = {'django-chrissinchok-resume': 'resume'},
    install_requires = ['setuptools'],
)