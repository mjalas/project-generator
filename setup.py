from setuptools import setup, find_packages


VERSION = '0.0.1'

setup(
    name='project-generator',
    version=VERSION,
    description='Generates project structure.',
    url='https://github.com/mjalas/project-generator',
    author='Mats Jalas',
    author_email='mats.jalas@gmail.com',
    license='GNU GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=[]),
    install_requires=[
        'PyYAML==4.2b4',
        'Click==7.0',
        'Jinja2==2.10.1'
    ],
    setup_requires=[
        'PyYAML==4.2b4',
        'Click==7.0'
    ],
    test_suite='nose.collector',
    tests_require=[
        'pytest==3.9.3',
        'pytest-cov==2.6.0',
        'PyYAML==4.2b4',
        'python-coveralls==2.9.1',
        'coverage==4.4'
    ],
    entry_points={
        'console_scripts': [
            'project=project_generator.cli.app:main'
        ]
    },
)
