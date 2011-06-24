from setuptools import setup, find_packages

setup(
    name = "django-resume",
    version = "1.0",
    url = 'https://chrissinchok.com',
    license = 'BSD',
    description = "An app to manage my resume",
    author = 'Chris Sinchok',
    packages = ['resume', 'resume.migrations'],
    package_dir = {'django-resume': 'resume'},
    install_requires = ['setuptools'],
)