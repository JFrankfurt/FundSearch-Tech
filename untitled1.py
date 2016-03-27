# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 20:51:36 2016

@author: Jordan
"""

# Get a dictionary
myList = [{'age': x} for x in range(1, 20, 2)]

# Enumerate ages
for i, age in enumerate(d['age'] for d in myList):
    print(i, age)


def asdf():
    info = dict()
    info["firm"] = "hi"
    info["count"] = 1
    info["cumulative"] = .2
    print(info)

asdf()
