mkdir -p mesh
MESH=mesh/world

# start with creating a PLC
SIZE=200
polyCreateWorld -x $SIZE -y $SIZE -z $SIZE -m 1 $MESH
polyConvert -v -V -o $MESH'worldC' $MESH

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

echo "1 100 # Background" > rho.map

# calculate fem solution using BERT
dcmod -v -P -a rho.map -s scheme3d.shm $MESH
dcedit -v -B -o scheme3d.data scheme3d.ohm




