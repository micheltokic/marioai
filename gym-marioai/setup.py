from setuptools import setup, find_packages

setup(
    name="gym_marioai",
    version="0.0.1",
    author="",
    author_email="",
    description="gym environment for marioai",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'gym>=0.17.2',
        'protobuf>=3.14.0',
        'keyboard'],

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'marioai-server-cli=gym_marioai.server.cli:main',
            ]
        }

    # package_dir={
    #     'gym_marioai': 'src/gym_marioai'},
    # packages=['gym_marioai', 'gym_marioai.envs'],
)
