"""
Module to save and retireve image analysis results.
Currently just to a flat json file, eventually in 
a database or something
"""

import os
import pickle

def cache_data(data):
    with open('output.pkl', 'wb') as f:
        pickle.dump(data, f)

def get_images(max_results=100, sort_field=None):
    with open('output.pkl', 'rb') as f:
        data = pickle.load(f).values()
    if sort_field:
        data.sort(key=lambda x: x.get(sort_field), reverse=True)
    return data[:max_results]        
