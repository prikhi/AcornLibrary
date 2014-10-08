from django.core.management.base import BaseCommand, CommandError
from books.models import Category
import requests
from lxml import html, etree, objectify
import urllib
import json

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class Command(BaseCommand):

    def handle(self, *args, **options):
        while Category.objects.count():
            ids = Category.objects.values_list('pk', flat=True)[:100]
            Category.objects.filter(pk__in = ids).delete()
    
        page = requests.get('http://en.wikipedia.org/wiki/List_of_Dewey_Decimal_classes')
        tree = html.fromstring(page.text)        
        
        top_level = ['Generalities',
                     'Philosophy and Psychology',
                     'Religion',
                     'Social Sciences',
                     'Language',
                     'Science',
                     'Technology',
                     'Arts and Recreation',
                     'Literature',
                     'History and Geography']
        
        for level_one_index in range (0, 10):
            level_one_object = Category.objects.create(number=''.join([str(level_one_index), '00']), title=top_level[level_one_index], link_number=level_one_index)
            for level_two_index in range(1, 11):
                raw = tree.xpath(''.join(['//*[@id="mw-content-text"]/ul[', str(level_one_index+1), ']/li[', str(level_two_index), ']/b']))[0].text_content()
                l2_number = raw[:3]
                l2_title = raw[4:]
                level_two_object = Category.objects.create(number=l2_number, title=l2_title, parent=level_one_object, link_number=l2_number[:2])
                for level_three_index in range(1 ,12):                    
                    if tree.xpath(''.join(['//*[@id="mw-content-text"]/ul[', str(level_one_index+1), ']/li[', str(level_two_index), ']/ul/li[', str(level_three_index), ']'])):
                        raw = tree.xpath(''.join(['//*[@id="mw-content-text"]/ul[', str(level_one_index+1), ']/li[', str(level_two_index), ']/ul/li[', str(level_three_index), ']']))[0].text_content()
                        l3_number = raw[:3]
                        l3_title = raw[4:]
                        Category.objects.create(number=l3_number, title=l3_title, parent=level_two_object, is_leaf=True, link_number=l3_number)
                        if level_three_index==1 and l3_number[2]!=0:
                            Category.objects.create(number=l2_number, title=l2_title, parent=level_two_object, is_leaf=True, link_number=l2_number)
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
