import PyPDF2
import os
import re
#os.getcwd()

print('Input file name including extention.')
file_name = input()

#opens the file in binary
file = open(file_name,'rb')

#reads the PDF's binary
reader = PyPDF2.PdfFileReader(file)

#sets reader to first page
page = reader.getPage(0)

#extract text from file
file_txt = page.extractText()

#a search parameters; b what to search
#uses search parameters to search document
def loc_finder(a,b):
    search = re.search(a,b)
    try:
        loc = search.span()
        return loc
    except:
        return False

#finds 'TO:' in the senders symbol block
ssb_loc = loc_finder('TO[:\s][:\s]', file_txt)

#finds 'From:' location
frm_loc = loc_finder('From[:]', file_txt)

#finds 'To:' location
to_loc = loc_finder('To[:]', file_txt)

#finds 'Subj:' location
subj_loc = loc_finder('Subj[:]', file_txt)

#finds 'Ref:' location
ref_loc = loc_finder('Ref[:]', file_txt)

#finds 'Encl:' location
encl_loc = loc_finder('Encl[:]', file_txt)

#finds the start of the body using '1.'
start_loc = loc_finder('1[.]', file_txt)

'''
These find the text of each of the lines that will be used by using the location where
the line starts and stops its seach at the beginning of the field that should follow it
'''
#Finds the SSIC and the sender, then separates them into individual variables
def ssb_line():
    if ssb_loc == False:
        return None
    else:
        return file_txt[ssb_loc[1]:frm_loc[0]]
ssb = ssb_line()
ssb_items = ssb.split()
ssic = ssb_items[0]
sender = ssb_items[1]
print(ssic)
print(sender)

#Establishes entire 'From:' line
def frm_line():
    if frm_loc == False:
        return None
    else:
        return file_txt[frm_loc[1]:to_loc[0]]
frm = frm_line()
print(frm)

#Establishes entire 'To:' line
def to_line():
    if frm_loc == False or to_loc == False:
        return None
    else:
        return file_txt[to_loc[1]:subj_loc[0]]
to = to_line()
print(to)

#Establishes 'Subj:' line
def subj_line():
    if ref_loc != False:
        return file_txt[subj_loc[1]:ref_loc[0]]
    elif encl_loc != False:
        return file_txt[subj_loc[1]:encl_loc[0]]
    else:
        return file_txt[subj_loc[1]:start_loc[0]]
subj = subj_line()
print(subj)

#Establishes 'Ref:' line
def ref_line():
    if ref_loc == False:
        return 'N/A'
    elif ref_loc != False and encl_loc != False:
        return file_txt[ref_loc[1]:encl_loc[0]]
    elif ref_loc != False and encl_loc == False:
        return file_txt[ref_loc[1]:start_loc[0]]
ref = ref_line()
print(ref)

#def to_loc():
#    pattern1 = re.compile(r'\w\w[:]')
#    matches1 = pattern1.finditer(file1)
#    return(match.span())
#to_loc()