import pytesseract
import cv2
import pandas as pd
import numpy as np
import time
import os
import argparse
import fitz
import re
from PyPDF2 import PdfFileReader


def process(path,down):
    Namelist = []
    FNamelist = []
    Vidlist = []
    Age = []
    Sex = []
    Name = []
    FName = []
    Vid = []
    vt = []
    vt2 = []
    vt3 = []
    vt4 = []
    Name_f1 = []
    Name_f2 = []
    Name_f3 = []
    li = ['Name','Father','Mother','Husband','Age','Photo','House','Available']
    print('\t\t\tMozilla Public License Version 2.0\n\n')
    pdf = PdfFileReader(open(path,'rb'))
    file_len = pdf.getNumPages()
    del pdf
    mat = fitz.Matrix(2.5,2.5)
    bufpath = path.split(sep = '/')[:-1]
    out = '/'.join(bufpath)
    out = out+'/temp.png'
    print(out)
    print(file_len)
    file = fitz.open(path)
    for p in range(2,file_len):
        print('Processing Page %d ....'%p)
        start = time.time()
        page = file.loadPage(p)
        pix = page.getPixmap(mat)
        pix.writePNG(out)
        img = cv2.imread(out)
        img = cv2.resize(img,(1241,1753))
        img = cv2.cvtColor(img,cv2.COLOR_BGR2XYZ)
        i1 = img[85:230]
        i2 = img[235:375]
        i3 = img[380:515]
        i4 = img[525:670]
        i5 = img[670:810]
        i6 = img[820:960]
        i7 = img[965:1105]
        i8 = img[1110:1255]
        i9 = img[1260:1400]
        i10 = img[1405:1550]
        images = []
        images.extend((i1,i2,i3,i4,i5,i6,i7,i8,i9,i10))
        images = np.array(images)
        im = []
        im2 = []
        for i in images:
            im2.append(cv2.resize(i[:,50:410],(800,350)))
            im2.append(cv2.resize(i[:,420:800],(800,350)))
            im2.append(cv2.resize(i[:,800:1170],(800,350)))
    #     for i in im:
    #         im2.append(cv2.resize(i,(880,350)))
        Vids = []
        FName = []
        Name = []
        for j in im2:
            v = 0
            n = 0
            f = 0
            ag = 0
            sx = 0
            img = j[:100,445:]
            vid = pytesseract.image_to_string(img)
            vid = vid.split(sep = '\n')
            for r in vid:
                if len(re.findall('[A-Z]',r))>1 and len(re.findall('[0-9]',r))>5:
                    Vids.append(r)
                    v+=1
            text = pytesseract.image_to_string(j,config = '--psm 11')
            text = text.split(sep = '\n')
            while '' in text:
                text.remove('')
            for z in range(len(text)):
                if 'Father' in text[z] or 'Mother' in text[z] or 'Husband' in text[z]:
                    a = text[z]
                    a = a.split(sep = 'Photo')[0]
                    a = a.split(sep = 'House')[0]
                    a = a.split(sep = 'Avail')[0]
                    try:
                        b = text[z+1]
                        b = b.split(sep = 'Photo')[0]
                        b = b.split(sep = 'House')[0]
                        b = b.split(sep = 'Avail')[0]
                    except IndexError:
                        b = ''
                    nm = []
                    nm.append(a)
                    nm.append(b)
                    f+=1
                    try:
                        FName.append((' '.join(nm)).split(sep = ':')[1:][0])
                    except IndexError:
                        FName.append(' '.join(nm))
                elif text[z].startswith('Name'):
                    a = text[z]
                    a = a.split(sep = 'Photo')[0]
                    a = a.split(sep = 'House')[0]
                    a = a.split(sep = 'Avail')[0]
                    n+=1
                    try:
                        Name.append(a.split(sep = ':')[1:][0])
                    except IndexError:
                        Name.append(a)
                elif 'Age' in text[z]:
                    Age.append(''.join(re.findall('[0-9]',text[z])))
                    ag+=1
                if re.search('Sex',text[z]):
                    Sex.append((text[z].split(sep = 'Sex')[-1]).split(sep = ':')[-1])
                    sx+=1
            if n==0:
                Name.append('deleted')
            if v==0:
                Vids.append('deleted')
            if f==0:
                FName.append('deleted')
            if ag==0:
                Age.append(0)
            if sx==0:
                Sex.append('deleted')
    #         text = pytesseract.image_to_string(j)
    #         text = text.split(sep = '\n')
    #         while '' in text:
    #             text.remove('')
    #         for z in range(len(text)):
    #             if text[z].startswith('Name'):
    #                 a = text[z]
    #                 a = a.split(sep = 'Photo')[0]
    #                 a = a.split(sep = 'House')[0]
    #                 a = a.split(sep = 'Avail')[0]
    #                 try:
    #                     Name.append(a.split(sep = ':')[1:][0])
    #                 except IndexError:
    #                     Name.append(a)
        try:
            assert len(Name)==len(FName)==len(Vids)
    #         for (g,h,k) in zip(Name,FName,Vids):
    #             Vidlist.append(k)
    #             Namelist.append(h)
    #             FNamelist.append(g)
            Namelist.extend(Name)
            FNamelist.extend(FName)
            Vidlist.extend(Vids)
        except AssertionError:        
            print('Fault on Page %d skipping page...'%p)
        print(time.time()-start)
    df = pd.DataFrame()
    df["Name"] = Namelist
    df['Relation'] = FNamelist
    df['Vid'] = Vidlist
    df['Age'] = Age
    df['Gender'] = Sex
    save = '/'.join(bufpath)
    save = save + '/outfile.csv'
    df.to_csv(os.path.join(down,'output.csv'))

