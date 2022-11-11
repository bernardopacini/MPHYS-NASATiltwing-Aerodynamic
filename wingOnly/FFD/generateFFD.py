import numpy as np
import sys

def writeFFDFile(fileName,nBlocks,nx,ny,nz,points):
    '''
    Take in a set of points and write the plot 3dFile
    '''

    f = open(fileName,'w')

    f.write('%d\n'%nBlocks)
    for i in range(nBlocks):
        f.write('%d %d %d '%(nx[i],ny[i],nz[i]))
    # end
    f.write('\n')
    for block in range(nBlocks):
        for k in range(nz[block]):
            for j in range(ny[block]):
                for i in range(nx[block]):
                    f.write('%f '%points[block][i,j,k,0])
                # end
            # end
        # end
        f.write('\n')

        for k in range(nz[block]):
            for j in range(ny[block]):
                for i in range(nx[block]):
                    f.write('%f '%points[block][i,j,k,1])
                # end
            # end
        # end
        f.write('\n')

        for k in range(nz[block]):
            for j in range(ny[block]):
                for i in range(nx[block]):
                    f.write('%f '%points[block][i,j,k,2])
                # end
            # end
        # end
    # end
    f.close()
    return

def returnBlockPoints(corners,nx,ny,nz):
    '''
    corners needs to be 8 x 3
    '''
    points = np.zeros([nx,ny,nz,3])

    # points 1 - 4 are the iMin face
    # points 5 - 8 are the iMax face

    for idim in range(3):
        edge1 = np.linspace(corners[0][idim],corners[4][idim],nx)
        edge2 = np.linspace(corners[1][idim],corners[5][idim],nx)
        edge3 = np.linspace(corners[2][idim],corners[6][idim],nx)
        edge4 = np.linspace(corners[3][idim],corners[7][idim],nx)

        for i in range(nx):
            edge5 = np.linspace(edge1[i],edge3[i],ny)
            edge6 = np.linspace(edge2[i],edge4[i],ny)
            for j in range(ny):
                edge7 = np.linspace(edge5[j],edge6[j],nz)
                points[i,j,:,idim] = edge7
            # end
        # end
    # end
                
    return points

################ Child FFD ##############
nBlocks = 1

nx = [10]
ny = [8]
nz = [2]

corners = np.zeros([nBlocks,8,3])

corners[0,0,:] = [2.66,-0.01,2.44]
corners[0,1,:] = [2.66,-0.01,2.74]
corners[0,2,:] = [3.96,  6.8,2.44]
corners[0,3,:] = [3.96,  6.8,2.74]
# corners[0,2,:] = [3.25,  6.8,2.44] # Expanding for propeller nodes (temporary)
# corners[0,3,:] = [3.25,  6.8,2.74]
corners[0,4,:] = [3.80,-0.01,2.44]
corners[0,5,:] = [3.80,-0.01,2.74]
corners[0,6,:] = [4.75,  6.8,2.44]
corners[0,7,:] = [4.75,  6.8,2.74]


points = []
for block in range(nBlocks):
    points.append(returnBlockPoints(corners[block],nx[block],ny[block],nz[block]))

#print points
# fileName = 'wingFFD.xyz'
fileName = 'childFFD.xyz'
writeFFDFile(fileName,nBlocks,nx,ny,nz,points)

################ Parent FFD ##############
nBlocks = 1

nx = [10]
ny = [8]
nz = [2]

corners = np.zeros([nBlocks,8,3])

# corners[0,0,:] = [2.5,-0.02,2.35]
# corners[0,1,:] = [2.5,-0.02,2.85]
# corners[0,2,:] = [2.5,  7.0,2.35]
# corners[0,3,:] = [2.5,  7.0,2.85]
# corners[0,4,:] = [5.0,-0.02,2.35]
# corners[0,5,:] = [5.0,-0.02,2.85]
# corners[0,6,:] = [5.0,  7.0,2.35]
# corners[0,7,:] = [5.0,  7.0,2.85]

corners[0,0,:] = [0.0,-0.02,0.0]
corners[0,1,:] = [0.0,-0.02,5.0]
corners[0,2,:] = [0.0,  7.0,0.0]
corners[0,3,:] = [0.0,  7.0,5.0]
corners[0,4,:] = [10.0,-0.02,0.0]
corners[0,5,:] = [10.0,-0.02,5.0]
corners[0,6,:] = [10.0,  7.0,0.0]
corners[0,7,:] = [10.0,  7.0,5.0]

points = []
for block in range(nBlocks):
    points.append(returnBlockPoints(corners[block],nx[block],ny[block],nz[block]))

#print points
# fileName = 'wingFFD.xyz'
fileName = 'parentFFD.xyz'
writeFFDFile(fileName,nBlocks,nx,ny,nz,points)