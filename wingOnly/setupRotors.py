import numpy as np
import pprint as pp


# rst fvSourceDict
def fvSourceDict(nRotors):
    R = 1.1079

    thrust_tot = 347.0897 * 3

    prop1 = np.array((2.3067, 2.2586, 2.4808))  # Wing, inboard
    prop2 = np.array((2.7209, 4.4572, 2.4808))  # Wing, middle
    prop3 = np.array((3.1364, 6.6626, 2.5908))  # Wing, tip

    y_min = prop1[1] - R
    R_max = 0.9 * prop3[2]

    # Compute Angle of Box
    dxdy = (prop3[0] - prop1[0]) / (prop3[1] - prop1[1])

    def X_Location(xIn, dY):
        xOut = xIn + dxdy * dY
        return xOut

    X_props = np.zeros((nRotors, 3))

    # Tip Propeller
    X_props[0, :] = prop3[:]

    # Inboard Propellers
    for j in range(nRotors - 1):
        X_props[j + 1, 2] = prop1[2]
        X_props[j + 1, 1] = prop3[1] - (j + 1) * (prop3[1] - y_min) / (nRotors - 0.5)
        X_props[j + 1, 0] = X_Location(prop3[0], X_props[j + 1, 1] - prop3[1])

    # Radius
    R_temp = ((prop3[1] - y_min) / (nRotors - 0.5)) / 2
    if R_temp > R_max:
        R_temp = R_max
    # Rotor Thrust
    thrust = thrust_tot / nRotors

    # Generate Dictionary
    fvSource = {}
    for i in range(nRotors):
        fvSource["disk{}".format(i + 1)] = {
            "type": "actuatorDisk",
            "source": "cylinderAnnulusSmooth",
            "center": [
                float(X_props[nRotors - i - 1, 0]),
                float(X_props[nRotors - i - 1, 1]),
                float(X_props[nRotors - i - 1, 2]),
            ],
            "direction": [1.0, 0.0, 0.0],
            "innerRadius": float(R_temp) * 0.2,
            "outerRadius": float(R_temp),
            "rotDir": "left",
            "scale": 1.0,
            "POD": 2.74,
            "eps": 0.15,
            "expM": 1.0,
            "expN": 0.5,
            "adjustThrust": 1,
            "targetThrust": thrust,
        }

    return fvSource

# rst setupRotors debug
if __name__ == "__main__":
    for i in range(5):
        print("\nFVSource Dictionary, N = {}".format(i + 1))
        pp.pprint(fvSourceDict(i + 1))
