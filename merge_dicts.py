# dict_merge.py
# merge dictionary files with menu options for ease
# uses code from sort.py and relabel_clean.py
# February 3, 2014

# from relabel_clean.py:
# This script will take a dictionary and several other dictionaries
# and merge all with the first.

# TODO:

# imports

import csv
import glob
import codecs
import re
from sys import exit
from shutil import move
from os import makedirs
from os.path import exists
from subprocess import call

# functions

# eliminates duplicates, taken from get_german_dict.py code
def no_copies(data):
        """Eliminates identical entries in a list."""
        data_new = []; prev = None
        for line in data:
                if prev is not None and not line == prev:
                        data_new.append(prev)
                prev = line
        return data_new

# on same line as each word, add its pronunciation
# change special chars to utf-8 encode
def add_pronunciation(words):

        new_words = []

        for item in words:
                list_string = list(item)
                for character in list_string:
                        new_char = character.encode('unicode_escape')
                        
                        if '\\' in new_char:
                                new_char = new_char.replace('\\', "")
                        
                        item = item + " " + new_char
                new_words.append(item)

        return new_words

# create list of words from old dictionary file
def list_from_old_dict(dictname):
        tmpList = []
        old_dict_list = []
                
        # if it does, extract the first word on each line
        if exists(dictname):
                
                with codecs.open(dictname, 'r', 'utf-8') as f:
                        tmpList = f.readlines()                        
                        
                f.close()
                        
                for item in tmpList:
                        item = item.split()[0]
                        old_dict_list.append(item)
                        
        return old_dict_list

# create list of words from lab files in file directory
def list_of_words(filedir):
        # updated list of files
        lab_list = glob.glob(filedir+"*")

        dictionary_list = []

        # for each file, get words from file and 
        for file in lab_list:
                if ".lab" in file:
                
                        #extract each word in file, put into dictionary list
                        dictionary_list = extract_word(file, dictionary_list)
                        
        return dictionary_list

# create dictionary from list of words
def create_dict(dictionary_list):
        # sort list
        sorted_words = sorted(dictionary_list)
                
        # remove duplicates
        unique_words = no_copies(sorted_words)

        # make pronunciations
        words_pronounced = add_pronunciation(unique_words)
                
        # put list into a dictionary text file        
        dictionary_file = codecs.open(filedir + "/dictionary.txt", 'w', 'utf-8')

        for word in words_pronounced:
                dictionary_file.write(word)
                dictionary_file.write("\n")

        dictionary_file.close()
        
        return dictionary_file

# user form

menu = True

while menu == True:

    print"""
===== MENU =====
1. merge dictionaries
2. quit
    
Please enter the number for the option you would like to select
"""
    value = raw_input("> ")
    
    if value == "1":

        # run dictionary merge script
        print"""
What is the file directory?
You can drag and drop the files into the Terminal window to fill out this space
WARNING: No individual directory should have a space character
If so, please go back and replace any spaces with underscores
        """
        filedir = raw_input("> ")
        if filedir[-1] == ' ':
                filedir = filedir.replace(" ", '')
        if filedir[-1] != '/':
                filedir = filedir + '/'
        
        # allow the user to enter several dictionaries, all of which are added to a new dictionary list
        moreDicts = True
        other_dict_list = []
        while (moreDicts == True):
            print"""
If there is a dictionary in another directory you would like to merge with the dictionary you are creating, 
input the file name (must include the directory)
If not, just hit enter.
You can drag and drop the files into the Terminal window to fill out this space
WARNING: No individual directory should have a space character
If so, please go back and replace any spaces with underscores
            """
            dictdir = raw_input("> ")
            if dictdir == '':
                    print(" ")
                    moreDicts = False
            else:
                    if dictdir[-1] == ' ':
                            dictdir = dictdir.replace(" ", '')
                    other_dict_list_temp = list_from_old_dict(dictdir)
                    other_dict_list += other_dict_list_temp
                    
        # check if dictionary already exists
        dictname = filedir + "/dictionary.txt"                                
        old_dict_list = list_from_old_dict(dictname)
        
        dictionary_list = old_dict_list + other_dict_list
        
        if not dictionary_list:
                print("The dictionary is empty.")
        else:                
                dictionary_file = create_dict(dictionary_list)
                print("merged dictionaries")
        
        
        
    elif value == "2":
        # quit
        print("quit")
        menu = False
        
    else: 
        print("Incorrect input. Try again.")