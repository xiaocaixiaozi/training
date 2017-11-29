#!/usr/bin/env python
# coding=utf-8
# Author: bloke
# 修改ERM文件

from xml.etree import ElementTree as ET

old_file = ''
new_file = 'transport.new.xml'
new_servicegroup = [str(x) for x in range(10)]
old_servicegroup = []

tree = ET.parse(old_file)
servicegroups = tree.getiterator('ServiceGroups')[0]
streamlinks = tree.getiterator('StreamLinks')[0]

for i in servicegroups:
    old_servicegroup.append(i.get('id'))

diff = set(new_servicegroup).difference(set(old_servicegroup))
for servicegroup_id in diff:
    ET.SubElement(servicegroups, 'Group', attrib={"id":str(servicegroup_id), "type":"", "desc":""})

#tree.write(new_file, encoding='utf-8', xml_declaration=True)

