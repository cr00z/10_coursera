import requests
import lxml
import json
import openpyxl
import argparse
import os
from bs4 import BeautifulSoup
from datetime import datetime
import re


COURSERA_LINK = 'https://www.coursera.org/sitemap~www~courses.xml'


def get_url_content(url):
    return requests.get(url).content


def get_courses_list_from_xml(coursera_xml_content):
    coursera_xml_root = lxml.etree.fromstring(coursera_xml_content)
    for course_url_tag in coursera_xml_root.getchildren():
        yield course_url_tag.getchildren().pop().text


def get_full_course_info(course_content):
    course_soup = BeautifulSoup(course_content, 'lxml')
    try:
        course_json_str = course_soup.find(
            'script',
            attrs={'type': 'application/ld+json'}
        ).string
    except AttributeError:
        return None
    return json.loads(course_json_str)


def get_course_duration(course):
    days_in_week = 7
    week_correction = 1
    try:
        start_date = datetime.strptime(
            course['hasCourseInstance']['startDate'],
            '%Y-%m-%d'
        )
        end_date = datetime.strptime(
            course['hasCourseInstance']['endDate'],
            '%Y-%m-%d'
        )
        return (end_date - start_date).days // 7 - week_correction
    except KeyError:
        return None


def get_course_rating(course):
    try:
        return course['aggregateRating']['ratingValue']
    except KeyError:
        return None


def get_course_info(course_url):
    course_info = get_full_course_info(course_url)
    if not course_info:
        return []
    for course_elem in course_info['@graph']:
        if course_elem['@type'] == 'Product':
            course_product = course_elem
        if course_elem['@type'] == 'Course':
            course_course = course_elem
    return {
        'name': course_product['name'],
        'language': course_course['inLanguage'],
        'start': course_product['offers']['validFrom'],
        'rating': get_course_rating(course_product),
        'duration': get_course_duration(course_course)
    }


def output_courses_info_to_xlsx(filepath, courses_info):
    if os.path.exists(filepath):
        work_book = openpyxl.load_workbook(filepath)
    else:
        work_book = openpyxl.Workbook()
    work_sheet = work_book.active
    for course_info in courses_info:
        work_sheet.append(convert_course_info_to_list(course_info))
    work_book.save(filepath)


def get_cmdline_args():
    parser = argparse.ArgumentParser(
        description='courses list grabber from Coursera.org'
    )
    parser.add_argument('xlsx_path', help='path for result excel file')
    parser.add_argument(
        '--limit',
        type=int,
        default=20,
        help='number of courses'
    )
    parser.add_argument(
        '--start',
        type=int,
        default=1,
        help='course to start'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='show results in console'
    )
    return parser.parse_args()


def convert_course_info_to_list(course_info):
    return [
        course_info['index'],
        course_info['url'],
        course_info['name'],
        course_info['language'],
        course_info['start'],
        course_info['rating'],
        course_info['duration']
    ]

    
if __name__ == '__main__':
    args = get_cmdline_args()
    if not re.fullmatch(r'.*(\.xlsx|\.xlsm|\.xltx|\.xltm)$', args.xlsx_path):
        exit('Supported formats are: .xlsx,.xlsm,.xltx,.xltm')
    courses_info = []
    course_index = 1
    for course_url in get_courses_list_from_xml(get_url_content(COURSERA_LINK)):
        if course_index >= args.start:
            course_info = get_course_info(get_url_content(course_url))
            course_info['index'] = course_index
            course_info['url'] = course_url
            if args.verbose:
                print(*convert_course_info_to_list(course_info))
            courses_info.append(course_info)
            course_index += 1
        if course_index == args.start + args.limit:
            break
    output_courses_info_to_xlsx(args.xlsx_path, courses_info)
