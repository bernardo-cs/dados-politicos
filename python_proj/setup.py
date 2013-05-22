from distutils.core import setup

setup(
    name='eadw project',
    version='0.1.7',
    author='bernardo e guilherme',
    author_email='bersimoes@gmail.com',
    packages=['html_parser', 'sqlite_db', 'testes', 'xml_parser', 'pesquisa_whoosh', 'main','sentiment', 'graficos'],
    url='http://pypi.python.org/pypi/eadw/',
    license='README.md',
    description='projecto de eadw',
    long_description=open('README.md').read(),
)
#python setup.py sdist
#python setup.py install
