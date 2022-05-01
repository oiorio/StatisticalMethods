## Welcome to the Stat Methods page!

Follow the basic instructions on the necessary steps to install conda, minuit, etc. 

## 1) Installing conda

Install anaconda for your platform:

https://docs.anaconda.com/anaconda/install/index.html


By default (installation procedure should ask you) it will create a folder /home/username/miniconda2

It can ask to automatically setup the Conda , meaning your path will be extended with

    PATH=$PATH:/home/username/anaconda3/bin

    //Note: the version of python might be different depending on which OS and conda version you install - conda 3 should be the latest.

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

    PYTHONPATH=$PYTHONPATH:/home/username/anaconda3/lib/pythonX.Y/site-package

Note that X.Y is your local python version.

For the anaconda navigator you may have to install extra graphics libraries. For example, for linux:

    apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

## 2) installing jupyter

You should be able to launch the command for the anaconda navigator:

    anaconda-navigator

From there, you should be able to follow the jupyter icon and either install it or update it.

It can be launched from command line as well:

    jupyter-notebook

## 3) Installing iminuit

To install iminuit:

    conda install iminuit -c conda-forge

you can also install it on your machine by first deactivating the environment

## 4) Installing root

To install root:

    conda install root -c conda-forge

you can also install it on your machine by first deactivating the environment, but it's not recommended with conda,

## 5) Installing mathplotlib

To install root:

    conda install mathplotlib -c conda-forge

Used by some tools, including minuit, for plotting routines.

