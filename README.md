*Tagesschau Wordcloud Generator

**Welcome to the Tagesschau Wordcloud Generator!

This fun little python project pulls data from the Tagesschau API[link], saves it to
a json file and (optionally) displays a wordcloud from that data.

By default, the whole server reply is saved to the json. Relevant columns for further
work with the data are "topline", "title", and "firstSentence". If you're interested 
in doing ML-type things, the data does come with the tags supplied by Tagesschau. But
beware, they're only saved to a single pandas Dataframe column as a dict in the 
"tag":<tag> format, so you'll have to de-clutter it a little bit.

The average time duration captured by the data in the files is about 6 days. If you 
want to do a longitudal study, remember to get new data frequently.

Once you downloaded the files, you'll be free to do whatever you want whith them. Fork
as much as you please but please keep in mind the Tagesschau API rate limit of max
1 query every minute.

**Installation:

***Dependencies:
    Python:             3.11.9
    Pip:                23.0.1
    (python3.11-venv)   3.11.2-6

***Install:

    1. Download the files from github
    Ideally, you download the files to their own directory
    $ wget <link>
    or
    $ git clone <link> . #to install it to current directory
    or
    $ git clone <link> <directory> #to install to directory <directory>

    2. Set up the local environment
    $ cd <path/to/directory>            #navigate to directory
    $ python3 -m venv <name-of-venv>    #make a virtual environment
    $ source <venv>/bin/activate        #activate venv
    $ pip install requirements.txt      #download required packages

    You're set up !

    Either from your favourite IDE or from the command line, you can now interact
    with the Tagesschau Reader.

