# Capstone project for Jose Portilla's Complete Python Bootcamp course at udemy.com

# Project Idea: Inverted index - An Inverted Index is a data structure used to create full text search.
# Given a set of text files, implement a program to create an inverted index. Also create a
# user interface to do a search using that inverted index which returns a list of files that
# contain the query term / terms. The search index can be in memory.

# Word-level inverted index - Features:
#   * loads text file from web into memory, scans it and builds index
#      + index stores as {'word':[(str('path/to/file'),int(pos_of__occurrence)),(...)]}
#   * combines the dictionary with main database of all scanned text files
#      + main dictionary stored locally as a sqlite file
#   * UI that allows entry of multiple words (phrases) and return of snippets from relevant text files
#      + returns results for both single words and complete phrase (ie, "love", "you", and "love you")
#      + UI in cli only, no web or widget
#   * Two tables for normalized storage
#      + table: CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT);
#      + table: CREATE TABLE words_loc(id INTEGER PRIMARY KEY AUTOINCREMENT, words_id INTEGER, url TEXT, loc INTEGER);

import urllib2
import sqlite3
import re


class FileLoad(object):

    def __init__(self,file_loc):
        '''loads file, builds index, adds to main index'''
        self.return_list = {}
        try:
            response = urllib2.urlopen(file_loc)
            html = response.read()
        except:
            html = False
            print "%s is not a valid URL."%(file_loc)
        if html != False:
            # progressively remove script, style, then all HTML tags
            clean_html = re.sub(r'<script[\s\S]+?>[\s\S]+?<\/script>','',html)
            clean_html = re.sub(r'<style[\s\S]+?>[\s\S]+?<\/style>','',clean_html)
            clean_html = re.sub(r'<[^<]+?>', '', clean_html)
            # remove all special characters except single - and single ' to help build a more clean word list
            real_clean_html = re.sub(r'^[\'-]|[\'-]$|[-]{2,}|[\']{2,}|([\'-])\W|\W([\'-])|[^a-z\'\s-]+', ' ', clean_html.lower())
            # created ordered list of unique words from file
            word_list = sorted(set(real_clean_html.split()))
            # now add to sqlite database
            try:
                conn = sqlite3.connect('capstone.db')
                self.cursor = conn.cursor()
                # find locations for each word and update database where necessary
                for w in word_list:
                    # We're only interested in words with more than one letter
                    if len(w) > 1:
                        # Check if word is already in database; if not, add it
                        w_id = self.check_for_word(w)
                        if w_id == False:
                            self.cursor.execute("insert into words(word) values(?)",(w,))
                            conn.commit()
                            w_id = self.cursor.lastrowid
                        # Get word location in document
                        for word_loc in [p.start() for p in re.finditer(r'\s%s[\s|-|\.|,]'%(w),clean_html.lower())]:
                            # First, check if this word instance is already in database
                            self.cursor.execute("select url,loc from words_loc where words_id = ?",(w_id,))
                            r = self.cursor.fetchone()
                            # If that instance of word isn't recorded already, add to the database
                            if r[1] != word_loc or r[0] != file_loc:
                                self.cursor.execute("insert into words_loc(words_id,url,loc) values(?,?,?)",(w_id,file_loc,word_loc))
                                conn.commit()
                # Close connection and print affirmative message.
                conn.close()
                print "Index successfully updated for: %s"%(file_loc)
            # Print an error if there's a problem with adding to database
            except sqlite3.Error, e:
                print "Error %s:"%(e.args[0])

    def check_for_word(self,word):
        '''Checks if a word is already recorded in database'''
        self.cursor.execute("select id from words where word = ?",(word,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return False


class FileSnip(object):

    def __init__(self,result):
        '''loads file, converts to string, and returns text within n spaces before and
         after word_position for display
         result = (file,word_position)'''
         #for word_loc in [p.start() for p in re.finditer(r'\s%s[\s|-|\.|,]'%(w),clean_html.lower())]:
         #     print loc,"Excerpt: ...",clean_html[loc-40:loc+40],"...\n"
        print result


class SearchScan(object):

    def __init__(self,word_list):
        '''scans index for occurrences of words in word_list
         scans index for phrases; phrase = words in word_list within n pos of each other
         results = [(word,file,loc),(...)]'''
        print word_list


class SearchOutput(object):

    def __init__(self,result_list):
        ''' combines and displays results to screen word, URL, and file snippet for each result'''
        print result_list


class UserInput(object):

    def __init__(self):
        pass

    def user_activity(self):
        ''' asks user to load file or search for terms and calls pertinent method'''
        while True:
            task = raw_input('Type "search" or "load" for activity: ').upper()
            if task == 'SEARCH':
                self.search_query()
                break
            elif task == 'LOAD':
                self.load_file()
                break

    def load_file(self):
        ''' takes file location from user and calls FileLoad'''
        file = raw_input("Enter full URL including http:// of page to load): ")
        # do validation here
        FileLoad(file)

    def search_query(self):
        ''' asks for search terms, calls SearchScan, and returns results as SearchOutput'''
        search = raw_input("Enter search term: ")
        word_list = search.split()
        for item in SearchScan(word_list):
            results.append([item['0'],item['1'],FileSnip([item['1'],item['2']])])
        SearchOutput(results)

    def again_or_die(self):
        ''' asks for another search query or end program'''
        while True:
            cont = raw_input("Press y to continue or any other key to quit. ").upper()
            if cont == "Y":
                return True
                break
            else:
                return False
                break


class main(object):

    def __init__(self):

        ui = UserInput()

        while True:
            #ask for input
            ui.user_activity()
            #show output
            if ui.again_or_die() == False:
                print "Goodbye!"
                break


main()
