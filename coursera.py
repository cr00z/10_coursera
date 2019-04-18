import requests
import lxml
import json
import openpyxl
import argparse
import os
from bs4 import BeautifulSoup
from datetime import datetime
import re


def get_courses_list():
    coursera_link = 'https://www.coursera.org/sitemap~www~courses.xml'
    coursera_xml = requests.get(coursera_link).content
    coursera_xml_root = lxml.etree.fromstring(coursera_xml)
    for course_url_tag in coursera_xml_root.getchildren():
        yield course_url_tag.getchildren().pop().text


def get_full_course_info(course_url):
    course_page = requests.get(course_url)
    course_soup = BeautifulSoup(course_page.content, 'lxml')
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
    return [
        course_product['name'],
        course_course['inLanguage'],
        course_product['offers']['validFrom'],
        get_course_rating(course_product),
        get_course_duration(course_course)
    ]


def output_course_info_to_xlsx(filepath, course_info):
    if os.path.exists(filepath):
        work_book = openpyxl.load_workbook(filepath)
    else:
        work_book = openpyxl.Workbook()
    work_sheet = work_book.active
    work_sheet.append(course_info)
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


if __name__ == '__main__':
    args = get_cmdline_args()
    if not re.fullmatch(r'.*(\.xlsx|\.xlsm|\.xltx|\.xltm)$', args.xlsx_path):
        exit('Supported formats are: .xlsx,.xlsm,.xltx,.xltm')
    course_index = 1
    for course_url in get_courses_list():
        if course_index >= args.start:
            course_info = get_course_info(course_url)
            course_info = [course_index, course_url] + course_info
            if args.verbose:
                print(*course_info)
            output_course_info_to_xlsx(args.xlsx_path, course_info)
        course_index += 1
        if course_index == args.start + args.limit:
            break
