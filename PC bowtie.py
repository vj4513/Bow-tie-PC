import numpy as np
import gdspy as gp

gp.current_library = gp.GdsLibrary()
lib = gp.GdsLibrary()
cell = lib.new_cell('FIRST')

tol = 1e-4   
nx = 20          #size of PC in x
ny = 20          #size of PC in y
a = 0.44            #Lattice constant
r = 0.1            #radius of holes
L = 1            #size of Cavity
dg = 0.01           #bow tie gap
ang = np.pi/4    #angle of bow tie
f = 0.005       #fillet of bow tie corners
dx = 0          #shift of holes around cavity
dr = 0           #shrink of holes around cavity

n_x = np.floor(nx/2)
n_y = np.floor(ny/2)
xs = nx%2
ys = ny%2
x = a*(np.arange(-n_x,n_x+xs,1))
y = a*np.sqrt(3)/2*(np.arange(-n_y,n_y+ys,1))     
#extra holes of PC for even are included on the left side
Ll = (n_x-1-(np.ceil(L/2)-1))+1
Lr = (n_x+1+(np.floor(L/2)))+1              
#extra cavity for even is included on the right side

county = 0
for j in y:
    countx = 0
    county+=1
    for i in x:
        countx+=1
        if county != n_y+1 or (countx >= Lr or countx <= Ll):
            if county%2 == 0:
                i+=a/2
                if county == n_y+1 and countx == Lr:
                    circle = gp.Round((i-dx,j), r-dr, tolerance = tol)
                    cell.add(circle)
                elif county == n_y+1 and countx == Ll:
                    circle = gp.Round((i+dx,j), r-dr, tolerance = tol)
                    cell.add(circle)
                else:
                    circle = gp.Round((i,j), r, tolerance = tol)
                    cell.add(circle)
            elif county == n_y+1 and countx == Lr:
                    circle = gp.Round((i-dx,j), r-dr, tolerance = tol)
                    cell.add(circle)
            elif county == n_y+1 and countx == Ll:
                    circle = gp.Round((i+dx,j), r-dr, tolerance = tol)
                    cell.add(circle)
            else:
                circle = gp.Round((i,j), r, tolerance = tol)
                cell.add(circle)
    
#adding bowtie   
if L >= 1 and dg > 0:    
    p =  a/2 if (n_y)%2 == 1 else 0  
    pie1 = gp.Round((dg/2+p, 0), r, initial_angle = -ang, 
                    final_angle = ang, tolerance = tol)
    pie1.fillet(radius = f)
    pie2 = gp.Round((-dg/2+p, 0), r, initial_angle = np.pi-ang, 
                    final_angle = np.pi+ang, tolerance = tol)
    pie2.fillet(radius = f)
    cell.add([pie1,pie2])
            
gp.LayoutViewer()
