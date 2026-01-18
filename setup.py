"""Setup configuration for Spiralverse-AetherMoore"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='spiralverse-aethermoore',
    version='0.1.0',
    author='Isaac Davis',
    author_email='issdandavis@github.com',
    description='Quantum-Resistant Cryptographic Framework with Harmonic Scaling Law',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/issdandavis/Spiralverse-AetherMoore',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Security :: Cryptography',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.9',
    install_requires=[
        'pycryptodome>=3.19.0',
        'numpy>=1.24.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'mypy>=1.0.0',
            'black>=23.0.0',
            'isort>=5.12.0',
        ],
        'pqc': [
            'pqcrypto>=0.1.3',
            'liboqs-python>=0.8.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'spiralverse=spiralverse.cli:main',
        ],
    },
    keywords='cryptography pqc quantum kyber dilithium harmonic encryption',
    project_urls={
        'Bug Reports': 'https://github.com/issdandavis/Spiralverse-AetherMoore/issues',
        'Source': 'https://github.com/issdandavis/Spiralverse-AetherMoore',
        'Documentation': 'https://github.com/issdandavis/Spiralverse-AetherMoore/docs',
    },
)
