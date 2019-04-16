from lxml import etree, html
import requests


def get_courses_list():
    coursera_link = 'https://www.coursera.org/sitemap~www~courses.xml'
    coursera_xml = requests.get(coursera_link).text.encode('utf-8')
    coursera_xml_root = etree.fromstring(coursera_xml)
    for course_url_tag in coursera_xml_root.getchildren():
        yield course_url_tag.getchildren().pop().text


def get_course_info(course_url):
    # html.parse don't work correctly
    page = requests.get(course_url).text.encode('utf-8')
    tree = html.fromstring(page)
    course_title = tree.xpath(
        './/*[@id="root"]/div[1]/div/div[1]/div[1]/div[1]/div/div/div[1]/div[2]/h1'
        )[0].text_content().encode('utf-8')
    print(course_title)
    course_language = tree.xpath(
        './/*[@id="root"]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/div[4]/div[2]/h4'
        ).pop().text_content().encode('utf-8')
    print(course_language)
    course_begin = tree.xpath(
        './/*[@id="start-date-string"]/span'
        )#.pop().text_content().encode('utf-8')
    print(course_begin)
    # return course_title, course_language, course_begin


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    for course_url in get_courses_list():
        get_course_info(course_url)
        break
