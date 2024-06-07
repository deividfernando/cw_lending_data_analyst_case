from sqlalchemy import create_engine, MetaData, Table, func, case, and_
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import sys
import os
from .database import engine
import pandas as pd

__all__ = [
    'create_engine',
    'sessionmaker',
    'load_dotenv',
    'os',
    'engine',
    'pd',
    'MetaData',
    'Table',
    'func',
    'case',
    'and_'
    ]

root_dir = os.path.abspath(os.path.dirname(__file__))
while os.path.basename(root_dir) != "cw_lending_data_analyst_case":
    root_dir = os.path.dirname(root_dir)

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)