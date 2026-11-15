from pathlib import Path
from io import BytesIO
import shutil
from PIL import Image,ImageDraw,ImageFont
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import pypdfium2 as pdfium
out=Path('output/pdf')
text='''$ java Playfair.java
Enter key: MONARCHY

Playfair Matrix:
[M, O, N, A, R]
[C, H, Y, B, D]
[E, F, G, I, K]
[L, P, Q, S, T]
[U, V, W, X, Z]

1. Encrypt
2. Decrypt
3. Encrypt from file
4. Decrypt from file
5. Exit
Enter choice: 1
Enter text: BALLOON
Digraph Pairs: BA LX LO ON
Ciphertext: IBSUPMNA

1. Encrypt
2. Decrypt
3. Encrypt from file
4. Decrypt from file
5. Exit
Enter choice: 2
Enter text: IBSUPMNA
Digraph Pairs: IB SU PM NA
Plaintext: BALXLOON

1. Encrypt
2. Decrypt
3. Encrypt from file
4. Decrypt from file
5. Exit
Enter choice: 5
$'''
font=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',26)
small=ImageFont.truetype('/System/Library/Fonts/Menlo.ttc',22)
lines=text.splitlines()
im=Image.new('RGB',(1500,85+len(lines)*33+30),'#101b2b')
d=ImageDraw.Draw(im)
d.rectangle((0,0,1500,57),fill='#263448')
for x,color in [(28,'#ff6059'),(54,'#ffbd2e'),(80,'#28ca42')]: d.ellipse((x,20,x+14,34),fill=color)
d.text((440,17),'Playfair - Simulated example run',font=small,fill='#edf3fa')
for i,line in enumerate(lines):
 color='#a5dd9b' if line.startswith(('Ciphertext:','Plaintext:','$')) else '#e0e8f0'
 d.text((32,78+i*33),line,font=font,fill=color)
imagepath=out/'CYL57_Part_A_Q2_Simulated_Output.png'
im.save(imagepath)
old=PdfReader(out/'CYL57_All_Output_Images.pdf')
items=[]
for idx,page in enumerate(old.pages):
 heading=page.extract_text().splitlines()
 part='A' if idx<4 else 'B'
 q=([1,3,4,5][idx] if idx<4 else idx-3)
 pic=page.images[0].image.convert('RGB')
 items.append((part,q,heading[2],heading[3],pic,False))
items.insert(1,('A',2,'Playfair Cipher','Example based on the Java code in CYL57 - 2.pdf',im,True))
path=out/'CYL57_All_Output_Images.pdf'
c=canvas.Canvas(str(path),pagesize=A4)
c.setTitle('CYL57 - All Output Images')
c.setAuthor('Arush Yadav')
w,h=A4
for idx,(part,q,title,source,pic,simulated) in enumerate(items,1):
 c.setFillColorRGB(.12,.18,.27)
 c.setFont('Helvetica-Bold',11);c.drawString(36,h-37,'CYL57 | CRYPTOGRAPHY & NETWORK SECURITY LAB')
 c.setFont('Helvetica-Bold',18);c.drawString(36,h-68,f'Part {part} - Question {q}')
 c.setFont('Helvetica',14);c.drawString(36,h-91,title)
 c.setFont('Helvetica',9);c.setFillColorRGB(.35,.39,.44);c.drawString(36,h-111,source)
 if part=='B' or simulated:
  c.setFont('Helvetica-Bold',9);c.setFillColorRGB(.56,.26,.08)
  c.drawString(36,h-133,'SIMULATED EXAMPLE RUN - VERIFIED AGAINST SOURCE CODE' if simulated else 'OFFLINE MODEL OUTPUT - NOT A WIRESHARK CAPTURE')
 maxw,maxh=w-72,h-205
 scale=min(maxw/pic.width,maxh/pic.height)
 iw,ih=pic.width*scale,pic.height*scale
 c.drawImage(ImageReader(pic),(w-iw)/2,h-156-ih,width=iw,height=ih)
 c.setFillColorRGB(.4,.44,.49);c.setFont('Helvetica',8)
 c.drawString(36,32,'Simulated output image' if simulated else 'Extracted output image')
 c.drawRightString(w-36,32,f'{idx} / {len(items)}');c.showPage()
c.save()
r=PdfReader(path)
assert len(r.pages)==10
assert 'Question 2' in r.pages[1].extract_text()
doc=pdfium.PdfDocument(str(path))
doc[1].render(scale=1.5).to_pil().save('tmp/pdfs/playfair_page.png')
dest=Path('/Users/arushyadav/My Drive (emailme@arushyadav.com)/University/3rd Year/Semester 5/CYL57 - Crypto & Network Security Lab/Lab Submissions')
shutil.copy2(path,dest/path.name)
print('Updated PDF:',dest/path.name)
print('Pages:',len(r.pages))
