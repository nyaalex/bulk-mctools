from setuptools import setup

setup(
    name='bulk_mctools',
    version='1.0.0',
    packages=['bulk_mctools'],
    url='https://github.com/nyaalex/bulk-mcstatus',
    license='',
    author='nyaalex',
    author_email='alexanderhjpettifer@gmail.com',
    description='Query Minecraft servers in bulk',
    entry_points={
              'console_scripts': [
                  'bulk-mcstatus=bulk_mctools.bulk_query:run',
              ],
    }
)
