import setuptools


setuptools.setup(
    name='detection-translator',
    version='0.0.1',
    author='Maciej Lewandowicz',
    author_email='maciek.lewandowicz@gmail.com',
    description='Part of engineering thesis project. Python library responsible for translating detected boxes into '
                'MusicXML files',
    url='',
    packages=setuptools.find_namespace_packages(include=('detection_translator.*', 'detection_translator')),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8.0',
    entry_points={
        'console_scripts': [
            'detection_translator = detection_translator.main:main',
        ],
    },
)
