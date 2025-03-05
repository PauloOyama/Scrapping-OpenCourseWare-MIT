import re 

# example = "2a5a21775717ad45b02b6cea8ed3a872_MIT21M_380S11_lec14.pdf"
example = './tmp/Lecture_1__What_Make****s_Healthcare_Unique?.txt'

ls = re.sub('[^A-Za-z0-9_/.]+', '', example)

print(ls)