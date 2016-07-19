# Capstone project for Jose Portilla's Complete Python Bootcamp course at udemy.com

# Inverted index - An Inverted Index is a data structure used to create full text search.
# Given a set of text files, implement a program to create an inverted index. Also create a
# user interface to do a search using that inverted index which returns a list of files that
# contain the query term / terms. The search index can be in memory.

# Word-level inverted index - Features:
#   * loads text file from web into memory, scans it and builds index
#      + index stores as {'word':[(str('path/to/file'),int(pos_of__occurrence)),(...)]}
#   * combines the dictionary with main dictionary of all scanned text files
#      + main dictionary stored locally as a sqlite file
#   * UI that allows entry of multiple words (phrases) and return of snippets from relevant text files
#      + returns results for both single words and complete phrase (ie, "love", "you", and "love you")
#      + UI in cli only, no web or widget

import urllib
import sqlite3
import re

class FileLoad(object):

    def __init__(self,file):
        # loads file, builds index, adds to main index
        pass


class FileSnip(object):

    def __init__(self,result):
        #result = (file,word_position)
        #opens file and returns text within n spaces before and after word_position for display


class SearchScan(object):

    def __init__(self,word_list):
        # scans index for occurrences of words in word_list
        # scans index for phrases; phrase = words in word_list within n pos of each other
        # returns abridged index of results
        pass


class SearchOutput(object):

    def __init__(self,result_list):
        # combines and displays results to screen
        # word, URL, and file snippet for each result
        pass


class UserInput(object):

    def __init__(self):
        pass

    def user_activity(self):
        # asks user to load file or search for terms
        # returns "load" or "search"
        task = raw_input('Type "search" or "load" for activity: ').upper()
        if task == 'SEARCH':
            self.search_scan()
        elif UserInput.user_activity() == 'LOAD':
            self.load_file()

    def load_file(self):
        # takes file location from user and calls FileLoad
        file = raw_input("Enter full URL to file: ")
        # do validation here
        FileLoad(file)

    def search_query(self):
        # asks for search terms and returns them as SearchOutput
        search = raw_input("Enter search term: ")
        word_list = search.split()
        SearchScan(word_list)

    def again_or_die(self):
        # asks for another search query or end program
        cont = raw_input("Contine? Enter y or n: ").upper()
        if cont == "Y"
            return True
        else:
            return False


class main(object):

    def __init__(self):
        while True:
            #ask for input
            UserInput.user_activity()
            #show output
            if UserInput.again_or_die() == False:
                break
