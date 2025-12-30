# Telegram Advance Security (TAS) - Setup Script
from setuptools import find_packages, setup

setup(
    name='ptb_advance_security',
    packages=find_packages(),
    version='0.1.0',
    description='Python library that incorporates standards and tools to make your Python Telegram Bot safer.',
    author='Isaaker',
    setup_requires=['python-telegram-bot>=13.7', 'requests>=2.22.0', 'cryptography>=46.0.3', 'python-gnupg>=0.5.1', 'drheader>=2.0.0'],
)