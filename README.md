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

    //Note: the version of python might be different depending on which one you are using.

Once you installed conda, suggest to log in again to make the .bashrc launch again, or just make 

    source .bashrc

1.1) Creating the environment: with conda it's often useful to create a working environment that will help you setup all your codes.

    conda create -n rootenv -c conda-forge

    //"rootenv" can be any name you want.

After you create it, activate it with:

    conda activate rootenv

You can install programs in the global environment, but it's not suggested:

    conda deactivate

and proceed. In that case, you will have to manually link the pythonpath:

    PYTHONPATH=$PYTHONPATH:/home/username/miniconda2/lib/pythonX.Y/site-package

Note that X.Y is your local python version.

## 2) Installing iminuit

To install iminuit:

    conda install iminuit -c conda-forge

you can also install it on your machine by first deactivating the environment

## 3) Installing root

To install root:

    conda install minuit -c conda-forge

you can also install it on your machine by first deactivating the environment, but it's not recommended with conda,

## 4) Installing mathplotlib

To install root:

    conda install minuit -c mathplotlib

Used by some tools, including minuit, for plotting routines.


