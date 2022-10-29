bertNew3D > bert.cfg scheme3d.data

sed -i 's/#MAXITER=20/MAXITER=5/' bert.cfg
sed -i 's/#PARA3DQUALITY=1.5/PARA3DQUALITY=1.5' bert.cfg
sed -i 's/#LAMBDA=20/LAMBDA=1/' bert.cfg
sed -i 's/#ZWEIGHT=0.1/ZWEIGHT=0.05/' bert.cfg

cat bert.cfg
