import numpy as np
import datetime as dt

"""
Function getTags takes cow_id, start_date, end_date as input and 
returns a list of tuples (tag_str, start_date, end_date) 
"""
def getTagTimes(cow_id, start_d, end_d):

    # 1. connect to database (matching table)
    # 2. extract * where cow_id=cow_id 
    # 3. find tag(s) in interval start_d - end_d
    #   if several tags -> end_date = next start_date 
    # 


"""
OUTDATED - GET A LIFE!
This script works as a reference table to match a cow + time interval to 
one or more tags. This script is currently not saving the list (TODO), should 
save to a file or something and read when __init__  the ReferenceList. 
"""
class ReferenceList:
    #Create cow list with each element representing a cow (1-numberOfCows).
    #Each element contains a list of tags, linked to the cow.
    def __init__(self, nr_of_cows):
        self.cow_list = []
        for x in range(1,nr_of_cows):
            #tag_list = []
            self.cow_list.append(TagList())

    #Add a tag to a cow
    def add_tag(self, cow_id, tag_str, start_time, end_time='current'):
        self.cow_list[cow_id-1].add_tag_dict(tag_str,start_time,end_time='current')
    
    #Notify that a tag has been removed from a cow 
    def removed_tag(self, cow_id, end_time):
        self.cow_list[cow_id-1].remove_tag(end_time)

    def get_tags(self, cow_id, start_interval, end_interval):
        queryResult = []
        for x in cow_id:
            tags_list = self.cow_list[x-1].get_tags(start_interval, end_interval)

            queryResult.append()    """ HERE """

         


class TagList:
    #Create a tag list, containing dictonaries with all tags worn by the cow.
    def __init__(self):
        self.tag_list = []

    #Add a tag to the list. The last element in the list will by default
    def add_tag_dict(self, tag_str, start_time, end_time):
        if not self.tag_list:
            self.tag_list.append([{
                'tag_id':tag_str
                'start':start_time
                'end':end_time
            }])
        else:
            self.tag_list[-1]['end'] = start_time
            self.tag_list.append([{
                'tag_id':tag_str
                'start':start_time
                'end':end_time
            }])
    #Enter the end time for the current tag (last in list)
    def remove_tag(self, time):
        if not self.tag_list:
            pass
        else:
            self.tag_list[-1]['end'] = time

    def get_tags(self, start_interval, end_interval): """ AND HERE """




