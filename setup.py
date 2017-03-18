from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="Si7021",
    version="0.1.1",
    description="Driver for the Si7021 humidity and temperature sensor",
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Embedded Systems',
    ],
    url="https://github.com/herm/Si7021",
    author="Hermann Kraus",
    author_email="hermann.kraus@gmail.com",
    license="MIT",
    packages=["si7021"],
    zip_safe=True
)