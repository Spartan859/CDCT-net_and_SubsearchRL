import setuptools

setuptools.setup(name='SEQ',        # Secondary directory
    version='0.1',
    packages=setuptools.find_packages(),
    install_requires=['gym','stable-baselines3']    # And any other dependencies foo needs
)