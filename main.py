#Reference - https://github.com/Jesse-Millwood/image-2-coe

import sys
from PIL import Image

def imageToCoeConverter(imageName1, imageName2):		
    img 	= Image.open(imageName1)	
    if img.mode != 'RGB':
        img = img.convert('RGB')	
    width 	= img.size[0]
    height	= img.size[1]
    filetype = imageName1[imageName1.find('.'):]
    filename = imageName1.replace(filetype,'.coe')
    imgcoe = open(filename,'wb')
    imgcoe.write(';	VGA Memory Map\n'.encode())
    imgcoe.write('; .COE file with hex coefficients\n'.encode())
    imgcoe.write('; Height: {0}, Width: {1}\n'.format(height,width).encode())
    imgcoe.write('memory_initialization_radix = 2;\n'.encode())
    imgcoe.write('memory_initialization_vector =\n'.encode())

    for i in range(2):
        if i ==0:
            img	= Image.open(imageName1)
        else:
            img	= Image.open(imageName2)

        if img.mode != 'RGB':
            img = img.convert('RGB')	
        width 	= img.size[0]
        height	= img.size[1]

        cnt = 0
        line_cnt = 0

        for r in range(0, height):
            for c in range(0, width):			
                cnt += 1			
                try:
                    R,G,B = img.getpixel((c,r))
                except IndexError:
                    print('Index Error Occurred At:')
                    print('c: {}, r:{}'.format(c,r))
                    sys.exit()			
                Rb = bin(R)[2:]
                Gb = bin(G)[2:]
                Bb = bin(B)[2:]

                Rb = (8-len(Rb))*"0"+Rb
                Gb = (8-len(Gb))*"0"+Gb
                Bb = (8-len(Bb))*"0"+Bb


                Outbyte = Rb+Gb+Bb					
                try:
                    imgcoe.write(Outbyte.encode())
                except ValueError:
                    print('Value Error Occurred At:')
                    print('Contents of Outbyte: {0} at r:{1} c:{2}'.format(Outbyte,r,c))
                    print('R:{0} G:{1} B{2}'.format(R,G,B))
                    print('Rb:{0} Gb:{1} Bb:{2}'.format(Rb,Gb,Bb))
                    sys.exit()	
                line_cnt+=1		
                if c==width-1 and r==height-1 and i==1:
                    imgcoe.write(';'.encode())
                else:				
                    imgcoe.write(','.encode())

    imgcoe.close()
    print('Xilinx Coefficients File:{} DONE'.format(filename))
    print('Converted from {} to .coe'.format(filetype))
    print('Size: h:{} pixels w:{} pixels'.format(height,width))
    print('COE file is 24 bits wide and {} bits deep'.format(line_cnt))
    print('Total addresses: {}'.format(2*(line_cnt)))


if __name__ == '__main__':
    imageName1 = input("Enter first image name :")
    imageName2 = input("Enter second image name :")
    imageToCoeConverter(imageName1, imageName2)