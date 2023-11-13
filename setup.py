from distutils.core import setup
setup(
  name = 'ontoutils',         # How you named your package folder (MyLib)
  packages = ['ontoutils', "ontoutils.core"],   # Chose the same as "name"
  version = '0.8',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A collection of utility scripts mainly for translating content from Excel spreadsheets into OWL ontologies',   # Give a short description about your library
  author = 'Janna Hastings',                   # Type in your name
  author_email = 'janna.hastings@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/jannahastings/ontoutils',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jannahastings/ontoutils/archive/v_06.9.tar.gz',    # I explain this later on
  keywords = ['OWL', 'ontologies', 'Excel'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
	  'openpyxl',
	  'argparse'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8',
  ],
)
