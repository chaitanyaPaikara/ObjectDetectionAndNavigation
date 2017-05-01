# -*- coding: utf-8 -*-
import numpy as np
import sys
import cv2

class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items==[]

    def enque(self,item):
        self.items.insert(0,item)

    def deque(self):
        return self.items.pop()

    def qsize(self):
        return len(self.items)
    
    def isInside(self, item):
      return (item in self.items)

class SLIC:
    def __init__(self, img, step, nc):
        self.img = img
        self.height, self.width = img.shape[:2]
        self._convertToLAB()
        self.step = step
        self.nc = nc
        self.ns = step
        self.FLT_MAX = 1000000
        self.ITERATIONS = 10

    def _convertToLAB(self):
       
          self.labimg = np.copy(self.img)
          for i in xrange(self.labimg.shape[0]):
              for j in xrange(self.labimg.shape[1]):
                  rgb = self.labimg[i, j]
                  self.labimg[i, j] = self._rgb2lab(tuple(reversed(rgb)))

    def _rgb2lab ( self, inputColor ) :

       num = 0
       RGB = [0, 0, 0]

       for value in inputColor :
           value = float(value) / 255

           if value > 0.04045 :
               value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
           else :
               value = value / 12.92

           RGB[num] = value * 100
           num = num + 1

       XYZ = [0, 0, 0,]

       X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
       Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
       Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
       XYZ[ 0 ] = round( X, 4 )
       XYZ[ 1 ] = round( Y, 4 )
       XYZ[ 2 ] = round( Z, 4 )

       XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
       XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
       XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

       num = 0
       for value in XYZ :

           if value > 0.008856 :
               value = value ** ( 0.3333333333333333 )
           else :
               value = ( 7.787 * value ) + ( 16 / 116 )

           XYZ[num] = value
           num = num + 1

       Lab = [0, 0, 0]

       L = ( 116 * XYZ[ 1 ] ) - 16
       a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
       b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

       Lab [ 0 ] = round( L, 4 )
       Lab [ 1 ] = round( a, 4 )
       Lab [ 2 ] = round( b, 4 )

       return Lab

    def generateSuperPixels(self):
        self._initData()
        indnp = np.mgrid[0:self.height,0:self.width].swapaxes(0,2).swapaxes(0,1)
        for i in range(self.ITERATIONS):
            self.distances = self.FLT_MAX * np.ones(self.img.shape[:2])
            for j in xrange(self.centers.shape[0]):
                xlow, xhigh = int(self.centers[j][3] - self.step), int(self.centers[j][3] + self.step)
                ylow, yhigh = int(self.centers[j][4] - self.step), int(self.centers[j][4] + self.step)

                if xlow <= 0:
                    xlow = 0
                if xhigh > self.width:
                    xhigh = self.width
                if ylow <=0:
                    ylow = 0
                if yhigh > self.height:
                    yhigh = self.height

                cropimg = self.labimg[ylow : yhigh , xlow : xhigh]
                colordiff = cropimg - self.labimg[self.centers[j][4], self.centers[j][3]]
                colorDist = np.sqrt(np.sum(np.square(colordiff), axis=2))

                yy, xx = np.ogrid[ylow : yhigh, xlow : xhigh]
                pixdist = ((yy-self.centers[j][4])**2 + (xx-self.centers[j][3])**2)**0.5
                dist = ((colorDist/self.nc)**2 + (pixdist/self.ns)**2)**0.5

                distanceCrop = self.distances[ylow : yhigh, xlow : xhigh]
                idx = dist < distanceCrop
                distanceCrop[idx] = dist[idx]
                self.distances[ylow : yhigh, xlow : xhigh] = distanceCrop
                self.clusters[ylow : yhigh, xlow : xhigh][idx] = j

            for k in xrange(len(self.centers)):
                idx = (self.clusters == k)
                colornp = self.labimg[idx]
                distnp = indnp[idx]
                self.centers[k][0:3] = np.sum(colornp, axis=0)
                sumy, sumx = np.sum(distnp, axis=0)
                self.centers[k][3:] = sumx, sumy
                self.centers[k] /= np.sum(idx)

    def _initData(self):
        self.clusters = -1 * np.ones(self.img.shape[:2])
        self.distances = self.FLT_MAX * np.ones(self.img.shape[:2])

        centers = []
        for i in xrange(self.step, self.width - self.step/2, self.step):
            for j in xrange(self.step, self.height - self.step/2, self.step):
                
                nc = self._findLocalMinimum(center=(i, j))
                color = self.labimg[nc[1], nc[0]]
                center = [int(color[0]), int(color[1]), int(color[2]), int(nc[0]), int(nc[1])]   
                centers.append(center)
        self.center_counts = np.zeros(len(centers))
        self.centers = np.array(centers)

    def createConnectivity(self):
        label = 0
        adjlabel = 0
        lims = self.width * self.height / self.centers.shape[0]
        dx4 = [-1, 0, 1, 0]
        dy4 = [0, -1, 0, 1]
        new_clusters = -1 * np.ones(self.img.shape[:2]).astype(np.int64)
        elements = []
        for i in xrange(self.width):
            for j in xrange(self.height):
                if new_clusters[j, i] == -1:
                    elements = []
                    elements.append((j, i))
                    for dx, dy in zip(dx4, dy4):
                        x = elements[0][1] + dx
                        y = elements[0][0] + dy
                        if (x>=0 and x < self.width and 
                            y>=0 and y < self.height and 
                            new_clusters[y, x] >=0):
                            adjlabel = new_clusters[y, x]
                count = 1
                c = 0
                while c < count:
                    for dx, dy in zip(dx4, dy4):
                        x = elements[c][1] + dx
                        y = elements[c][0] + dy

                        if (x>=0 and x<self.width and y>=0 and y<self.height):
                            if new_clusters[y, x] == -1 and self.clusters[j, i] == self.clusters[y, x]:
                                elements.append((y, x))
                                new_clusters[y, x] = label
                                count+=1
                    c+=1
                if (count <= lims >> 2):
                    for c in range(count):
                        new_clusters[elements[c]] = adjlabel
                    label-=1
                label+=1
        self.new_clusters = new_clusters

    def displayContours(self, color):
        dx8 = [-1, -1, 0, 1, 1, 1, 0, -1]
        dy8 = [0, -1, -1, -1, 0, 1, 1, 1]

        isTaken = np.zeros(self.img.shape[:2], np.bool)
        contours = []

        for i in xrange(self.width):
            for j in xrange(self.height):
                nr_p = 0
                for dx, dy in zip(dx8, dy8):
                    x = i + dx
                    y = j + dy
                    if x>=0 and x < self.width and y>=0 and y < self.height:
                        if isTaken[y, x] == False and self.clusters[j, i] != self.clusters[y, x]:
                            nr_p += 1

                if nr_p >= 2:
                    isTaken[j, i] = True
                    contours.append([j, i])

        for i in xrange(len(contours)):
            self.img[contours[i][0], contours[i][1]] = color

    def _findLocalMinimum(self, center):
        min_grad = self.FLT_MAX
        loc_min = center
        for i in xrange(center[0] - 1, center[0] + 2):
            for j in xrange(center[1] - 1, center[1] + 2):
                c1 = self.labimg[j+1, i]
                c2 = self.labimg[j, i+1]
                c3 = self.labimg[j, i]
                if ((c1[0] - c3[0])**2)**0.5 + ((c2[0] - c3[0])**2)**0.5 < min_grad:
                    min_grad = abs(c1[0] - c3[0]) + abs(c2[0] - c3[0])
                    loc_min = [i, j]
        return loc_min

img = cv2.imread(sys.argv[1])
nr_superpixels = int(400)
nc = int(37)

step = int((img.shape[0]*img.shape[1]/nr_superpixels)**0.5)

slic = SLIC(img, step, nc)
slic.generateSuperPixels()
slic.createConnectivity()
slic.displayContours([0, 0, 255])
cv2.imshow("superpixels", slic.img)
#cv2.waitKey(0)
cv2.imwrite("SLICimg.jpg", slic.img)

su=np.zeros(len(slic.centers)+1)

#print(slic.centers)#(l,a,b,x,y) of each superpixel center`

print(len(su))
print(img.shape)
for i in range(img.shape[0]):
  for j in range(img.shape[1]):   
    su[slic.new_clusters[i][j]]+=1

print(slic.new_clusters.shape)

dic={}
dimension=[]
for i in range(len(slic.centers)):
  
  t=slic.new_clusters[int(slic.centers[i][4]),int(slic.centers[i][3])]
  li1,li2=np.where(slic.new_clusters== t)
  
  
  l=[]
  
  for j in range(len(li2)):   
    if li1[j]==int(slic.centers[i][4]) :
      l.append(li2[j])
  width=max(l)-min(l)
  li=[]
  for j in range(len(li1)):   
    if li2[j]==int(slic.centers[i][3]) :
      li.append(li1[j])
  height=max(li)-min(li)
  li3=[]
  for j in range(len(li1)):
    if li1[j]-int(slic.centers[i][4])==li2[j]-int(slic.centers[i][3]):
      li3.append(li1[j]-int(slic.centers[i][4]))
  diag=max(li3)-min(li3)
  dic[t]=(width,height,diag,int(slic.centers[i][3]),int(slic.centers[i][4]),slic.centers[i][0],slic.centers[i][1],slic.centers[i][2],int(su[t]))
  dimension.append(tuple((width,height,diag)))



# cv2.imshow('centers',img)
# cv2.imwrite("img.jpg", img)  
##area of each superpixel is equivalent to total number of pixels in each superpixel   
#print(su)
##height width and diaginal of each superpixel
#print(dimension)
#print(dic)

'''
print(sum(su))   

for (i, segVal) in enumerate(np.unique(slic.new_clusters)):
  # construct a mask for the segment
  print "[x] inspecting segment %d" % (i)
  mask = np.zeros(img.shape[:2], dtype = "uint8")
  mask[slic.new_clusters == segVal] = 255   
  
  # show the masked region
  cv2.imshow("Mask", mask)
  cv2.imshow("Applied",cv2.bitwise_and(img, img, mask = mask))
  cv2.waitKey(0)
'''

image = np.zeros((480,640,3), np.uint8)
pts = np.array([[160,480],[230,385],[405,385],[480,480]], np.int32)
pts = pts.reshape((-1,1,2))
cv2.fillPoly(image,[pts],[255,255,255],4,0)
#cv2.imshow("Applied",image)
#cv2.waitKey(0)


con=set([])

for i in range(168,480):
  for j in range(385, 480):
    #print(image[i][j])
    if  (image[i][j]==[255,255,255]).all: 
      con.add(dic[slic.new_clusters[j,i]])
      
means=[sum(x)/len(con) for x in zip(*con)]
print("means = ", means) 

# cv2.imshow("superpixels", slic.img)
# # cv2.waitKey(0)
# cv2.imwrite("SLICimg13.jpg", slic.img)
# print(step)
# src = slic.img
# # building training set from safe zone
# for key in dic.keys():
#   #print(tuple(np.subtract(dic[key],tuple(means))))
  
#   (a,b,c,d,e,f,g,h,i)=tuple(np.subtract(dic[key],tuple(means)))
#   #print(d+means[3],e+means[4])
#   ssd=((a/(step))**2+(b/(step))**2+(c**2)/(step**2)/2+f**2+g**2+h**2+(i/step**2)**2)
#   if ssd<600:
#     final=[]
#     final=zip(*np.where(slic.new_clusters== key)) 
#     for (x_,y_) in final:
#       src[x_][y_]=(255,255,255)


src = slic.img
space=[]  
for i in range(11):
  new=[]
  for j in range(15):
    new.append(0)
  space.append(new)
                                    

space=[[0]*15]*11  
cv2.imwrite('final.jpg',src)
for i in range(len(slic.centers)):
  cv2.circle(src,(int(slic.centers[i][3]),int(slic.centers[i][4])), 6, (0,0,255), -1)
print(space) 
for i in range(len(slic.centers)) :
  r=i//11
  c=i%11
  # print(r,c)
  # print(slic.centers[i][4],slic.centers[i][3],slic.new_clusters[int(slic.centers[i][4])][int(slic.centers[i][3])])
  # space[c][r]=dic[slic.new_clusters[slic.centers[i][4]][slic.centers[i][3]]]
  # print(c,r,space[r][c])
  # print(dic[slic.new_clusters[int(slic.centers[i][3])][int(slic.centers[i][4])]])
  # cv2.circle(src,(int(i[3]),int(i[4])), 6, (0,0,255), -1)
print(len(slic.centers)) 
# np.reshape(slic.centers, (11, 15,5)) 
print(slic.centers.shape)
print(slic.centers)

# cv2.imshow('floor',src)
# cv2.waitKey(0)

# print("space = ", space)
# print("space shape = ", np.array(space).shape)

# print(slic.new_clusters.shape)

def regiongrow(image,epsilon,start_point):
    print(image.shape)
    Q = Queue()
    s = set([])    
    x = start_point[0]
    y = start_point[1]
    while not Q.isEmpty():

        t = Q.deque()
        x = t[0]
        y = t[1]
    
   
    Q.enque((x,y))
    while not Q.isEmpty():

        t = Q.deque()
        x = t[0]
        y = t[1]
        
        if x < image.shape[0]-1:
            (a,b,c,d,e,f,g,h,i)=tuple(np.subtract(space[x+1][y],tuple(means)))
            ssd=((a/(step))**2+(b/(step))**2+(c**2)/(step**2)/2+f**2+g**2+h**2+(i/step**2)**2)
            if ssd<= epsilon and not Q.isInside( (x + 1 , y) ) and not (x + 1 , y) in s:
                Q.enque( (x + 1 , y) )
        
                
        if x > 0 :
            (a,b,c,d,e,f,g,h,i)=tuple(np.subtract(space[x-1][y],tuple(means)))
            ssd=((a/(step))**2+(b/(step))**2+(c**2)/(step**2)/2+f**2+g**2+h**2+(i/step**2)**2)
            if ssd<= epsilon and  not Q.isInside( (x - 1 , y) ) and not (x - 1 , y) in s:
                Q.enque( (x - 1 , y) )
        
                     
        if y < (image.shape[1] - 1):
            (a,b,c,d,e,f,g,h,i)=tuple(np.subtract(space[x][y+1],tuple(means)))
            ssd=((a/(step))**2+(b/(step))**2+(c**2)/(step**2)/2+f**2+g**2+h**2+(i/step**2)**2)
            if ssd<= epsilon and not Q.isInside( (x, y + 1) ) and not (x , y + 1) in s:
                Q.enque( (x , y + 1) )

                    
        if y > 0:
            (a,b,c,d,e,f,g,h,i)=tuple(np.subtract(space[x][y-1],tuple(means)))
            ssd=((a/(step))**2+(b/(step))**2+(c**2)/(step**2)/2+f**2+g**2+h**2+(i/step**2)**2)
            if ssd<= epsilon and not Q.isInside( (x , y - 1) ) and not (x , y - 1) in s:
                Q.enque( (x , y - 1) )


        if t not in s:                              
            s.add( t )
            #print("yes")
            #print(space[t[0]][t[1]][3],space[t[0]][t[1]][4])
        # for (x,y) in s:
        #     cv2.circle(src,(int(space[x][y][3]),int(space[x][y][4])), 6, (0,0,255), -1)    
        #     print(space[x][y][3],space[x][y][4])
    print("s is")
    print(s)
     
    for i in s:
      final=[]
      final=zip(np.where(slic.new_clusters== slic.new_clusters[space[i[0]][i[1]][4],space[i[0]][i[1]][3]]))
      for (x_,y_) in final:
       src[x_][y_]=(255,255,255)
      #cv2.circle(src,(int(space[i[0]][i[1]][3]),int(space[i[0]][i[1]][4])), 6, (0,0,255), -1)
      # cv2.circle(src,int(space[i[0]][i[1]][3]),int(space[i[0]][i[1]][4]), 6, (0,0,255), -1)

print(space[0][0])

# regiongrow(np.array(space),500,(8,9))
# cv2.imwrite("bfs13.jpg",src)
# cv2.imshow("sdfsdf",src)
# cv2.waitKey(0)
