#!/bin/bash

if [ -z "$WM_PROJECT" ]; then
  echo "OpenFOAM environment not found, forgot to source the OpenFOAM bashrc?"
  exit
fi

# =============================================================================
# Generate FFD
# =============================================================================
echo "--- Generating FFD ---"
(cd FFD && python3 generateFFD.py)

# =============================================================================
# Configure Case
# =============================================================================
echo "--- Configuring Case ---"
cp -r 0.orig 0

# =============================================================================
# Generate Mesh
# =============================================================================
echo "--- Generating Mesh ---"
if [ -d "../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic" ]; then
  mkdir -p ./constant/polyMesh
  cp ../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic/wingOnly/L3/boundary ./constant/polyMesh/
  cp ../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic/wingOnly/L3/cellZones ./constant/polyMesh/
  cp ../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic/wingOnly/L3/faces ./constant/polyMesh/
  cp ../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic/wingOnly/L3/faceZones ./constant/polyMesh/
  cp ../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic/wingOnly/L3/neighbour ./constant/polyMesh/
  cp ../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic/wingOnly/L3/owner ./constant/polyMesh/
  cp ../../inputData/DATA-MPHYS-NASATiltwing-Aerodynamic/wingOnly/L3/points ./constant/polyMesh/
else
  echo "Input Data Not Downloaded"
  exit 1;
fi
renumberMesh -overwrite &> logMeshGeneration.txt
