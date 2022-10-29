cd ..
cd adam_optimization

# bertNew3D > bert.cfg scheme3d.data
bert bert.cfg all

# find . ! -name 'dcinv.result.vtk' -type d -exec rm -r -f {} +
# find . ! -name 'dcinv.result.vtk' -type f -exec rm -f {} +
mkdir essential
mv coverage.vector essential/coverage.vector
mv dcinv.result.vtk essential/dcinv.result.vtk
mv create_scheme.py essential/create_scheme.py
mv resistivity.vector essential/resistivity.vector
mv rho2.map essential/rho2.map
mv scheme3d.data essential/scheme3d.data
mv scheme3d.ohm essential/scheme3d.ohm
mv scheme3d.shm essential/scheme3d.shm
mv build_model.sh essential/build_model.sh
mv bert.cfg essential/bert.cfg
mv invert.sh essential/invert.sh
mv vtk2csv_handler.py essential/vtk2csv_handler.py
mv optimize.sh essential/optimize.sh

mv essential ..

cd ..
rm -r adam_optimization

mv essential adam_optimization

cd adam_optimization

python3 vtk2csv_handler.py

