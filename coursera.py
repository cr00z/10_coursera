from lxml import etree
import requests


def get_courses_list():
    coursera_link = 'https://www.coursera.org/sitemap~www~courses.xml'
    coursera_xml = requests.get(coursera_link).text.encode('utf-8')
    coursera_xml_root = etree.fromstring(coursera_xml)
    for course_url_tag in coursera_xml_root.getchildren():
        yield course_url_tag.getchildren().pop().text


def get_course_info(course_slug):
#//*[@id="root"]/div[1]/div/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/h1
#<h1 class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz max-text-width-xl m-b-1s" data-reactid="207">Игрофикация</h1>
#<h1 class="H2_1pmnvep-o_O-weightNormal_s9jwp5-o_O-fontHeadline_1uu0gyz max-text-width-xl m-b-1s" data-reactid="213">FinTech Disruptive Innovation: Implications for Society</h1>
    pass


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    for course_url in get_courses_list():
        
