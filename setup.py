from pip.req import parse_requirements
from setuptools import setup

setup(name='czech-working-month',
      version='0.1.0',
      description='Working month calculator for Czech environment.',
      long_description='Compute accuratly the length of arbitrary working month.'
                       'Part-timers can set their fraction of the full-time.',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
      ],
      keywords='working month planner calculator ',
      url='https://github.com/petrbel/czech-working-month',
      author='Petr Belohlavek',
      author_email='me@petrbel.cz',
      license='MIT',
      packages=['czech_working_month'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[str(ir.req) for ir in parse_requirements('requirements.txt', session='hack')],
      entry_points={
          'console_scripts': [
              'czech-working-month=czech_working_month.czech_working_month:main'
          ]
      })
