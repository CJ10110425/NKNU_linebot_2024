'''
    FIXME: 靠杯，我想用 LinebotUtility 但是它鎖在外面，因為把它包起來了，所以先讓sys位置退到根目錄～～ 我不知道要怎麼解
'''
import sys
import os
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..')))