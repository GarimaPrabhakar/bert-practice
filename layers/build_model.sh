mkdir -p mesh
MESH=mesh/world

# start with creating a PLC
SIZE=200
polyCreateWorld -x $SIZE -y $SIZE -z $SIZE -m 1 $MESH
polyConvert -v -V -o $MESH'worldC' $MESH


# Create layer 1

polyCreateWorld -m 2 $MESH'cube2'
polyScale -x 199  -y 199 -z 100 $MESH'cube2'
polyTranslate -z -5 $MESH'cube2'

polyConvert -v -V -o $MESH'cube2PLC' $MESH'cube2'

# # Create layer 2
# polyCreateCube -m 3 $MESH'cube'
# polyScale -x $SIZE  -y $SIZE  -z $(($SIZE/3)) $MESH'cube'

# polyTranslate -z -$(($SIZE/6 + 30)) $MESH'cube'
# polyConvert -v -V -o $MESH'cubePLC' $MESH'cube'


#Merge layers and world
polyMerge -v $MESH $MESH'cube2' $MESH
# polyMerge -v $MESH $MESH'cube' $MESH

polyConvert -V -o $MESH'PLC' $MESH

# Get electrode scheme
python3 create_scheme.py
nElecs=`head -n 1 scheme3d.shm| cut -d'#' -f1`

#Add electrodes
head -n $[nElecs + 2] scheme3d.shm | tail -n $nElecs > mesh/elecs.xyz

polyAddVIP  -m -99 -f mesh/elecs.xyz $MESH

polyConvert -V -o $MESH'PLC' $MESH

polyRefineVIPS -z -0.01 $MESH

# build the mesh
tetgen -pazVACq1.2 $MESH.poly
meshconvert -v -iT -BDV -o $MESH $MESH.1
#python -c 'import pygimli as pg; m=pg.load("mesh/world.bms"); m=m.createP2(); m.save("mesh/world2.bms");'

rm -rf $MESH.1.*

echo "1 5 # Background" > rho2.map
echo "2 5 # Layer 1" >> rho2.map
# echo "3 1000 # Layer 2" >> rho.map

# calculate fem solution using BERT
dcmod -v -P -a rho2.map -s scheme3d.shm $MESH
dcedit -v -B -o scheme3d.data scheme3d.ohm




