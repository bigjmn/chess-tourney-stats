import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
from bs4 import BeautifulSoup
import requests

from ratingscraper import all_gamestats
from plotprepare import plotdata
from graphmaker import makegraphics

def run(uscf_id):
    data = all_gamestats(uscf_id)
    circles, bars = plotdata(data)
    makegraphics(circles, bars)
    return

run(12911474)
