import numpy as np
import os
import argparse

import openmdao.api as om
from mphys.multipoint import Multipoint
from dafoam.mphys import DAFoamBuilder, OptFuncs
from mphys.scenario_aerodynamic import ScenarioAerodynamic
from pygeo.mphys import OM_DVGEOCOMP

# =============================================================================
# Setup Parser
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument("--task", help="type of run to do", type=str, default="opt")
args = parser.parse_args()

if args.task == "runPrimal":
    useColoring = False
else:
    useColoring = True

# TEMPORARY PYGEO
childFFD = "./FFD/childFFD.xyz"
parentFFD = "./FFD/parentFFD.xyz"
# =============================================================================
# Flight Condition
# =============================================================================
U0 = 79.74
p0 = 69692.1456
nuTilda0 = 4.5e-5
T0 = 268.35
alpha0 = 0.0
A0 = 5.7915
rho0 = p0/287.0/T0  # density for normalizing CD and CL

CL_target = 0.67

daOptions = {
    "designSurfaces": ["wing"],
    "solverName": "DARhoSimpleFoam",
    "primalMinResTol": 1.0e-9,
    "primalMinResTolDiff": 1.0e4,
    "debug": False,
    "primalBC": {
        "U0": {"variable": "U", "patches": ["inout"], "value": [U0, 0.0, 0.0]},
        "p0": {"variable": "p", "patches": ["inout"], "value": [p0]},
        "T0": {"variable": "T", "patches": ["inout"], "value": [T0]},
        "nuTilda0": {"variable": "nuTilda", "patches": ["inout"], "value": [nuTilda0]},
        "useWallFunction": True,
    },
    # variable bounds for compressible flow conditions
    "primalVarBounds": {
        "UMax": 1000.0,
        "UMin": -1000.0,
        "pMax": 500000.0,
        "pMin": 20000.0,
        "eMax": 500000.0,
        "eMin": 100000.0,
        "rhoMax": 5.0,
        "rhoMin": 0.2,
    },
    "fvSource": {
        "disk1": {
            "type": "actuatorDisk",
            "source": "cylinderAnnulusSmooth",
            "center": [3.1364, 6.6626, 2.5908],
            "direction": [1.0, 0.0, 0.0],
            "innerRadius": 0.1,
            "outerRadius": 1.1079,
            "rotDir": "left",
            "scale": 1.0,
            "POD": 0.0,
            "eps": 0.05,
            "expM": 1.0,
            "expN": 0.5,
            "adjustThrust": 1,
            "targetThrust": 2000.0,
        },
        "disk2": {
            "type": "actuatorDisk",
            "source": "cylinderAnnulusSmooth",
            "center": [2.7209, 4.4574, 2.4808],
            "direction": [1.0, 0.0, 0.0],
            "innerRadius": 0.1,
            "outerRadius": 1.1079,
            "rotDir": "left",
            "scale": 1.0,
            "POD": 0.0,
            "eps": 0.05,
            "expM": 1.0,
            "expN": 0.5,
            "adjustThrust": 1,
            "targetThrust": 2000.0,
        },
        "disk3": {
            "type": "actuatorDisk",
            "source": "cylinderAnnulusSmooth",
            "center": [2.3067, 2.2586, 2.4808],
            "direction": [1.0, 0.0, 0.0],
            "innerRadius": 0.1,
            "outerRadius": 1.1079,
            "rotDir": "left",
            "scale": 1.0,
            "POD": 0.0,
            "eps": 0.05,
            "expM": 1.0,
            "expN": 0.5,
            "adjustThrust": 1,
            "targetThrust": 2000.0,
        },
        "disk4": {
            "type": "actuatorDisk",
            "source": "cylinderAnnulusSmooth",
            "center": [7.4511, 1.5362, 4.0060],
            "direction": [1.0, 0.0, 0.0],
            "innerRadius": 0.1,
            "outerRadius": 1.1079,
            "rotDir": "left",
            "scale": 1.0,
            "POD": 0.0,
            "eps": 0.05,
            "expM": 1.0,
            "expN": 0.5,
            "adjustThrust": 1,
            "targetThrust": 2000.0,
        },
    },
    "objFunc": {
        "CD": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["wing"],
                "directionMode": "fixedDirection",
                "direction": [1.0, 0.0, 0.0],
                "scale": 1.0 / (0.5 * rho0 * U0 * U0 * A0),
                "addToAdjoint": True,
            }
        },
        "CL": {
            "part1": {
                "type": "force",
                "source": "patchToFace",
                "patches": ["wing"],
                "directionMode": "fixedDirection",
                "direction": [0.0, 0.0, 1.0],
                "scale": 1.0 / (0.5 * rho0 * U0 * U0 * A0),
                "addToAdjoint": True,
            }
        },
    },
    "useAD": {"mode": "reverse"},
    "adjUseColoring": useColoring,
    "adjStateOrdering": "cell",
    "adjEqnOption": {"gmresRelTol": 1.0e-10, "pcFillLevel": 1, "jacMatReOrdering": "natural", "gmresMaxIters": 5000, "gmresRestart": 2000},
    "normalizeStates": {"U": U0, "p": p0, "nuTilda": nuTilda0 * 10.0, "phi": 1.0, "T": T0},
    "adjPartDerivFDStep": {"State": 1e-6, "FFD": 1e-3},
    "adjPCLag": 100,
    "designVar": {
        "twist": {"designVarType": "FFD"},
        "shape": {"designVarType": "FFD"},
        # "actuator_disk1": {"designVarType": "ACTD", "actuatorName": "disk1"},
        # "actuator_disk2": {"designVarType": "ACTD", "actuatorName": "disk2"},
    },
    "checkMeshThreshold": {
        "maxNonOrth": 90.0,
    },
}

class Top(Multipoint):
    def setup(self):
        # =====================================================================
        # DAFoam Setup
        # =====================================================================
        meshOptions = {
            "gridFile": os.getcwd(),
            "fileType": "OpenFOAM",
            "useRotations": False,
            "symmetryPlanes": [[[0.0, 0.0, 0.0], [0.0, 1.0, 0.0]]],
        }

        # Initialize DAFoam Builder
        dafoam_builder = DAFoamBuilder(daOptions, meshOptions, scenario="aerodynamic")
        dafoam_builder.initialize(self.comm)

        # =====================================================================
        # MPHY Setup
        # =====================================================================
        # Add Independent Variable Component for Design Variables
        self.add_subsystem("dvs", om.IndepVarComp(), promotes=["*"])

        # Create Mesh and Cruise Scenario
        self.add_subsystem("mesh", dafoam_builder.get_mesh_coordinate_subsystem())

        # Add Geometry Component
        self.add_subsystem("geometry", OM_DVGEOCOMP(file=parentFFD, type="ffd"))

        # Add Scenario
        self.mphys_add_scenario("cruise", ScenarioAerodynamic(aero_builder=dafoam_builder))

        # Connect Components
        self.connect("mesh.x_aero0", "geometry.x_aero_in")
        self.connect("geometry.x_aero0", "cruise.x_aero")

    def configure(self):
        # Add Functions to MPHYS
        self.cruise.aero_post.mphys_add_funcs()

        # Geometry DV Setup
        points = self.mesh.mphys_get_surface_mesh()

        # Add Pointset
        self.geometry.nom_add_discipline_coords("aero", points)

        # Constraint DV Setup
        tri_points = self.mesh.mphys_get_triangulated_surface()
        self.geometry.nom_setConstraintSurface(tri_points)

        # Create Reference Axis
        self.geometry.nom_addChild(ffd_file=childFFD)
        nRefAxPts = self.geometry.nom_addRefAxis(name="wingAxis", xFraction=0.25, alignIndex="j", childIdx=0)

        # Define Twist Design Variable
        def twist(val, geo):
            for i in range(0, nRefAxPts):
                geo.rot_y["wingAxis"].coef[i] = val[i]

        # Add DVs
        self.geometry.nom_addGlobalDV(dvName="twist", value=np.array([0] * (nRefAxPts)), func=twist, childIdx=0)
        nShapes = self.geometry.nom_addLocalDV(dvName="shape", axis="z", childIdx=0)
        
        # Set up constraints
        leList = [[2.72, 0.01, 2.59], [3.96, 6.61, 2.59]]
        teList = [[3.71, 0.01, 2.59], [4.65, 6.61, 2.59]]
        self.geometry.nom_addThicknessConstraints2D("thickcon", leList, teList, nSpan=16, nChord=20)
        self.geometry.nom_addVolumeConstraint("volcon", leList, teList, nSpan=16, nChord=20)
        self.geometry.nom_add_LETEConstraint("lecon", 0, "iLow", childIdx=0)
        self.geometry.nom_add_LETEConstraint("tecon", 0, "iHigh", childIdx=0)

        # Add and Connect DVs on the Indepent Variable Component
        self.dvs.add_output("twist", val=np.array([alpha0] * (nRefAxPts)))
        self.dvs.add_output("shape", val=np.array([0] * nShapes))
        self.connect("twist", "geometry.twist")
        self.connect("shape", "geometry.shape")

        # Define Design Variables
        self.add_design_var("twist", lower=-10.0, upper=10.0, scaler=1.0)
        self.add_design_var("shape", lower=-1.0, upper=1.0, scaler=10.0)

        # Define Constraints
        self.add_constraint("cruise.aero_post.CL", equals=0.67, scaler=10.0)
        self.add_constraint("geometry.thickcon", lower=0.5, upper=3.0, scaler=1.0)
        self.add_constraint("geometry.volcon", lower=1.0, upper=3.0, scaler=1.0)
        self.add_constraint("geometry.tecon", equals=0.0, scaler=1.0, linear=True)
        self.add_constraint("geometry.lecon", equals=0.0, scaler=1.0, linear=True)

        # Define Objective
        self.add_objective("cruise.aero_post.CD", scaler=100.0)


# =============================================================================
# OpenMDAO setup
# =============================================================================
prob = om.Problem()
prob.model = Top()

# Define Optimizer
prob.driver = om.pyOptSparseDriver()
prob.driver.options["optimizer"] = "SNOPT"
prob.driver.opt_settings = {
    "Major feasibility tolerance": 1.0e-4,
    "Major optimality tolerance": 1.0e-4,
    "Minor feasibility tolerance": 1.0e-4,
    "Verify level": -1,
    "Function precision": 1.0e-8,
    "Major iterations limit": 500,
    "Nonderivative linesearch": None,
    "Print file": "opt_SNOPT_print.txt",
    "Summary file": "opt_SNOPT_summary.txt",
}
prob.driver.options["debug_print"] = ["nl_cons", "desvars", "objs"]

# Setup Problem
prob.setup(mode="rev")
om.n2(prob, show_browser=False, outfile="mphys_aero.html")

# ----------------------------- Run Optimization ---------------------------- #
if args.task == "opt":
    prob.run_driver()

# -------------------------------- Run Primal ------------------------------- #
elif args.task == "runPrimal":
    prob.run_model()

# ------------------------------- Check Totals ------------------------------ #
elif args.task == "check_totals":
    prob.run_model()
    prob.check_totals(method="fd", step=1e-3)

# --------------------------------- No Task --------------------------------- #
else:
    print("Task not found!")
    exit(0)
