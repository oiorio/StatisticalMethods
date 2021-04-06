## Welcome to the Stat Methods page!

Follow the basic instructions on the necessary steps to install conda, minuit, etc. 

## 1) Installing conda

Download miniconda installer your platform:

https://docs.conda.io/en/latest/miniconda.html

And proceed with the instructions

https://conda.io/projects/conda/en/latest/user-guide/install/index.html

By default (installation procedure should ask you) it will create a folder /home/username/miniconda2

It will ask to automatically setup the Miniconda , meaning your path will be extended with

PATH=$PATH:/home/username/miniconda2/bin

If you have a $PYTHONPATH setup, you should add this to the path in a similar way:

PYTHONPATH=$PYTHONPATH:/home/username/miniconda2/lib/python2.7/site-packages

Note: the version of python might be different depending on which one you are using.

Once you installed conda, suggest to log in again to make the .bashrc launch again, or just make source .bashrc

## 2) Installing iminuit

To install minuit:

conda install -f iminuit -c conda-forge

## 3) Installing root

To install root:

3.1 conda install -f iminuit -c conda-forge

3.2 Or you can create an enviornment following this guide

https://iscinumpy.gitlab.io/post/root-conda/

But I would suggest to use the first one for the purposes of this exercise.

