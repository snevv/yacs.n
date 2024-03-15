#Ok so this file should take in some inputs (what though) and output a dictionary.
#This dictionary has all of the courses' course code as the keys and the value as the relevant information
#See fetch_catalog_course_info.py for the source of a lot of the code
#It's just that I will be rewriting it so that it is (hopefully) more understandable and better documented
import requests as req
import threading #https://docs.python.org/3/library/threading.html
import unicodedata
import re
import regex #https://www.dataquest.io/blog/regex-cheatsheet/
import json 
from datetime import date
from time import time
from threading import Lock
from io import StringIO
from bs4 import BeautifulSoup, SoupStrainer #https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from lxml import etree
import pdb

COURSE_DETAIL_TIMEOUT = 120.00 # seconds

allow_for_extension_regex = re.compile("(<catalog.*?>)|(<\/catalog>)|(<\?xml.*?\?>)")
prolog_and_root_ele_regex = re.compile("^(?P<prolog><\?xml.*?\?>)?\s*(?P<root><catalog.*?>)")

#Though we probably will not need everything here
class PrereqParse:
    def __init__(self, api_key):
        self.key = api_key
        self.search_endpoint = "http://rpi.apis.acalog.com/v2/search/courses?"
        self.course_detail_endpoint = "http://rpi.apis.acalog.com/v2/content?options[full]=1&method=getItems&type=courses"
        self.catalogIdEndpoint = "http://rpi.apis.acalog.com/v2/content?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&method=getCatalogs"
        self.resFormat = "xml"
        self.catalogId = 0
        self._lock = Lock()
        self._courseDetailsXMLStr = []
        self._xmlProlog = ""
        self._catalogRoot = ""
        self.chunkSize = 100
        self.courses = dict()
        
    def _all_threads_joined(self, threads):
        for thread in threads:
            thread.join(COURSE_DETAIL_TIMEOUT)
            if (thread.is_alive()):
                return False
        return True
        
    #Returns the current catalog id for the specified year
    def getCataId(self, year : int):
        res = req.get(self.catalogIdEndpoint)
        tree = etree.parse(StringIO(res.content.decode()))
        root = tree.getroot()
        try:
            key = "Rensselaer Catalog " + str(year) + "-" + str(year + 1)
            #https://stackoverflow.com/questions/53459703/type-lxml-etree-elementunicoderesult-cannot-be-serialized  
            for path in root.xpath("//text()"):
                if ''.join(str(s) for s in path) == key: #Could also use path.__str__() == key
                    return re.search("(?P<id>\d+)$", path.getparent().getparent().attrib['id']).group('id')
        except Exception as exception:
            print("Failed to get the catalog id")
        
    #Return the endpoint of the course ids
    def getCourseIds(self):
        # pdb.set_trace()
        #http://rpi.apis.acalog.com/v2/search/courses?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&method=listing&catalog=26&options[limit]=0
        xmlLink = (f"{self.search_endpoint}key={self.key}&format={self.resFormat}&method=listing&catalog={self.catalogId}&options[limit]=0")
        idXML = req.get(xmlLink).content.decode("utf8") #The xml is returned as bytes, so we need to turn it into a string
        only_ids = SoupStrainer("id")
        id_tags = BeautifulSoup(idXML, "xml", parse_only=only_ids).find_all("id")
        return [f"ids[]={id_xml.text}" for id_xml in id_tags]
    
    # Adds all course details in xml format to courseDetailsXMLStr class attribute 
    def getAllCourseDetails(self, ids_chunk):
        return 0
        
    def getCoursesXMLStr(self, ids):
        course_count = len(ids)
        id_chunks = [ids[i:i+self.chunkSize] for i in range(0, course_count, self.chunkSize)]
        chunk_count = len(id_chunks)
        courses_xml = ""
        
        # thread_jobs = []
        # for id_chunk in id_chunks:
        #     query_param_chunk = "&".join(id_chunk)
        #     fetch_course_details_job = threading.Thread(target=self.getCourseDetails, args=[query_param_chunk], daemon=False)
        #     thread_jobs.append(fetch_course_details_job)
        #     fetch_course_details_job.start()
        # # Wait until all jobs are finished
        # while True:
        #     if self._all_threads_joined(thread_jobs):
        #         break
        # courses_xml = self._xmlProlog + self._catalogRoot + "".join(self._courseDetailsXMLStr) + "</catalog>"
        return courses_xml
        
    #Return a dictionary of every course in the catalog
    def getAllCourses(self, ids):
        course_catalog = dict()
        self.getCoursesXMLStr()
        
        return 0
    
    #Return the details of a single course
    def getCourseDetails(self, id_params):
        course_details_xml_str = req.get(f"{self.course_detail_endpoint}&key={self.key}&format={self.resFormat}&catalog=21&{id_params}").content.decode("utf8")
        with self._lock:
            # https://stackoverflow.com/questions/39119165/xml-what-does-that-question-mark-mean
            # Can only have one prolog per XML document in order for it to be well-formed.
            # Can also only have one root.
            match = prolog_and_root_ele_regex.match(course_details_xml_str)
            if (match is None):
                raise Exception("XML document is missing prolog and root. Invalid.")
            # For some reason, the response is sometimes missing the XML prolog. Not sure how it's possible, but give default in that case.
            self._xmlProlog = match.group("prolog") if match.group("prolog") is not None else '<?xml version="1.0"?>'
            if match.group("root") is None:
                raise Exception("XML document is missing root element. Invalid.")
            self._catalogRoot = match.group("root")
            self._courseDetailsXMLStr.append(allow_for_extension_regex.sub("", course_details_xml_str))
            
    #Runs the program
    def run(self, year):
        #Maybe make some feature to get the catalog for every year?
        self.catalogId = self.getCataId(year)
        ids = self.getCourseIds()
        print(ids)
        #courses = self.getAllCourses(ids)
        #self.getAllCourseDetails(ids)

def main():
    parser = PrereqParse("3eef8a28f26fb2bcc514e6f1938929a1f9317628")
    parser.run(2023)

if __name__ == "__main__":
    main()