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

ACALOG_COURSE_FIELDS = {
    "department": "acalog-field-508",
    "level": "acalog-field-510",
    "full_name": "acalog-field-512",
    "description": "acalog-field-493",
    "raw_precoreqs": "acalog-field-495",
    "offer_frequency": "acalog-field-497",
    "cross_listed": "acalog-field-500",
    "graded": "acalog-field-502",
    "credit_hours": "acalog-field-504",
    "contact_lecture_lab_hours": "acalog-field-506",
}

USED_FIELDS = {
    "id": False, # custom
    "department": True,
    "level": True,
    "full_name": True,
    "short_name": True, # custom, requires department and level to be true. Use this to join with SIS data.
    "description": True,
    "prerequisites": True, # custom
    "corequisites": True, # custom
    "raw_precoreqs": True, # If either prereq or coreq is true, then this must be true cause the client needs to look at this field to understand the other two
    "offer_frequency": True,
    "cross_listed": False,
    "graded": False,
    "credit_hours": False,
    "contact_lecture_lab_hours": False,
}

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
    
    # https://stackoverflow.com/a/34669482/8088388
    def _clean_utf(self, string):
        # Format the unicode string into its normalized combined version
        return unicodedata.normalize("NFKC", string)
    
    def _is_actual_course(self, course_xml_element):
        # A valid course should have a name and description (can be empty, just not missing).
        # For some reason, the <course> tag is used in some places where there isn't an actual course.
        # If you remove this check in _get_all_courses, the returned course count is 1939 when using
        # catalog id 20. But if you count the course ids from the API it's 1933.
        # This check correctly returns the 1933 courses.
        desc_xml = course_xml_element.xpath(f"*[local-name() = 'field'][@type='{ACALOG_COURSE_FIELDS['description']}']")
        name_xml = course_xml_element.xpath(f"*[local-name() = 'name']")
        return desc_xml and name_xml
        
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
    
    #Return the details of a single course in XML format
    def getCourseDetailsXML(self, id_params):
        course_details_xml_str = req.get(f"{self.course_detail_endpoint}&key={self.key}&format={self.resFormat}&catalog=21&{id_params}").content.decode("utf8")
        with self._lock:
            # https://stackoverflow.com/questions/39119165/xml-what-does-that-question-mark-mean
            # Can only have one prolog per XML document in order for it to be well-formed.
            # Can also only have one root.
            match = prolog_and_root_ele_regex.match(course_details_xml_str)
            if (match is None):
                raise Exception("XML document is missing prolog and root. Invalid.")
            # For some reason, the response is sometimes missing the XML prolog. Not sure how it's possible, but give default in that case.
            self._xml_prolog = match.group("prolog") if match.group("prolog") is not None else '<?xml version="1.0"?>'
            if match.group("root") is None:
                raise Exception("XML document is missing root element. Invalid.")
            self._catalog_root = match.group("root")
            self._courseDetailsXMLStr.append(allow_for_extension_regex.sub("", course_details_xml_str))
        
    def getCoursesXMLStr(self, ids):
        course_count = len(ids)
        id_chunks = [ids[i:i+self.chunkSize] for i in range(0, course_count, self.chunkSize)]
        chunk_count = len(id_chunks)
        courses_xml = ""
        thread_jobs = []
        for id_chunk in id_chunks:
            query_param_chunk = "&".join(id_chunk)
            fetch_course_details_job = threading.Thread(target=self.getCourseDetailsXML, args=[query_param_chunk], daemon=False)
            thread_jobs.append(fetch_course_details_job)
            fetch_course_details_job.start()
        # Wait until all jobs are finished
        while True:
            if self._all_threads_joined(thread_jobs):
                break
        courses_xml = self._xmlProlog + self._catalogRoot + "".join(self._courseDetailsXMLStr) + "</catalog>"
        return courses_xml
        
    #Return a dictionary of every course in the catalog
    def getAllCourses(self, ids):
        courses_xml_str = self.getCoursesXMLStr(ids)
        parser = etree.XMLParser(encoding="utf-8")
        # tree = etree.parse(StringIO(courses_xml_str), parser=parser)
        # # https://stackoverflow.com/a/4256011/8088388
        # course_content_xml = tree.getroot().xpath("//*[local-name() = 'course']/*[local-name() = 'content']")
        # courses = []
        # for raw_course in course_content_xml:
        #     if (self._is_actual_course(raw_course)):
        #         field_values = {}
        #         used_standard_fields = filter(lambda key: key in ACALOG_COURSE_FIELDS and USED_FIELDS[key], USED_FIELDS)
        #         used_custom_fields = filter(lambda key: key not in ACALOG_COURSE_FIELDS and USED_FIELDS[key], USED_FIELDS)
        #         for field_name in used_standard_fields:
        #             # A <field>, like description, can have multiple children tags, so get all text nodes.
        #             # One example of this is ARCH 4870 - Sonics Research Lab 1, catalog 20, courseid 38592
        #             value = ("".join(raw_course.xpath(f"*[local-name() = 'field'][@type='{ACALOG_COURSE_FIELDS[field_name]}']//text()"))).replace("\n", "").replace("\r","").strip()
        #             if field_name == 'description':
        #                 field_values['description'] = self._clean_utf(value).encode("utf8").decode("utf8")
        #             else:
        #                 field_values[field_name] = self._clean_utf(value)
        #         if (len(field_values) > 0):
        #             courses.append(field_values)
        # return 0
    
    # Adds all course details in xml format to courseDetailsXMLStr class attribute 
    def getAllCourseDetails(self):
        return 0
            
    #Runs the program
    def run(self, year):
        self.catalogId = self.getCataId(year)
        ids = self.getCourseIds()
        courses = self.getAllCourses(ids)
        #self.getAllCourseDetails(ids)

def main():
    parser = PrereqParse("3eef8a28f26fb2bcc514e6f1938929a1f9317628")
    parser.run(2023)

if __name__ == "__main__":
    main()