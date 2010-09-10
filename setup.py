from setuptools import setup, find_packages

setup(
    name = "django-chrissinchok-resume",
    version = "0.1",
    url = 'http://github.com/csinchok/django-chrissinchok-resume',
    license = 'BSD',
    description = "An app to generate a resume for Chris Sinchok",
    author = 'Chris Sinchok',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires = ['setuptools'],
)
