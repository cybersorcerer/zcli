from setuptools import setup
setup(
    name='zosapi',
    version='0.0.1',
    description='Wrapper for the z/OSMF REST API',
    author='Ronny Funk',
    author_email='ronny@cybersorcerer.de',
    license='MIT',
    url='https://codehub.sva.de/zosapi',
    packages=['zosapi'],
    install_requires=[
        'setuptools==75.6.0',
        'requests==2.32.3',
        'click==8.1.7',
        'click-help-colors==0.9.4',
        'urllib3==2.2.3',
    ],
)