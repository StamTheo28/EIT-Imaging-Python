from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyeit.eit.greit as greit
import pyeit.mesh as mesh
from pyeit.eit.fem import Forward
from pyeit.eit.utils import eit_scan_lines
from pyeit.mesh.shape import circle

BACKGROUND = 1.0


def create_anomaly(data: list[float]):
    """ Create an artificial anomaly based on the data

    Parameters
    ----------
    data : list
        the data to create the anomaly from

    Returns
    -------
    dict
        anomaly is a dictionary (or arrays of dictionary) contains,
        {'x': val, 'y': val, 'd': val, 'perm': val}
        all permittivity on triangles whose distance to (x,y) are less than (d)
        will be replaced with a new value, 'perm' may be a complex value.
    """
    anomaly = []
    max_value = max(data)
    min_value = min(data)

    # Calculate the electrode positions around the unit circle
    points = np.ndarray.tolist(create_16_point_circle(0, 0, 1) * np.array([1, -1]))

    # Set up each node for the anomaly
    for i in range(0, len(points), 2):
        anomaly.append({"x": points[i][0], "y": -points[i][1], "d": 0.1, "perm": BACKGROUND})

    # Determine the size of the blockage at each node
    for i in range(len(anomaly)):
        # Set up variables representing relative position of measurements
        right, left = data[4 * i + 0], data[4 * i + 1]
        far_left, far_right = data[4 * i + 2], data[4 * i + 3]
        opposite_node_index = (i + 4) % len(anomaly)

        # Logic to determine if a a blockage is present at a node
        present_at_node = (right > 1) or (left > 1)
        blockage_depth = (far_left + far_right) / 2
        blockage_width = (right + left) / 2

        # If a blockage is measured but it appears to have no width, attribute the measurement to the
        # opposite node, but only if the opposite node has a smaller measurement or hasn't been
        # evaluated yet
        if not present_at_node and anomaly[opposite_node_index]["perm"] < blockage_depth:
            anomaly[opposite_node_index]["perm"] = blockage_depth

        # If the blockage seems to be at the node being evaluated, update it's contents with the
        # relevant data. The algorithm avoids overwriting a value with a smaller one to keep the
        # output sensitive and avoid loss of data
        elif present_at_node:
            if anomaly[i]["perm"] < blockage_depth:
                anomaly[i]["perm"] = blockage_depth
            # Interpolates the width of the blockage between 0 and 0.3 and then adds a flat 0.1 to it.
            # This lets small blockages still be plotted and big blockages become more prominent on
            # the final visualisation.
            anomaly[i]["d"] = 0.1 + (blockage_width - min_value) * (0.3 / (max_value - min_value))

    return anomaly


def greit_visualisation(data: list[float], baseline_data: list[float] = None, flatten: float = None):
    """ Calculate and construct the GREIT visualiton of the data.

    Parameters
    ----------
    data : list
        the data to be processed for visualisation
    baseline_data : list, optional
        baseline data for correction, by default `None`
    flatten : float, optional
        the number of standard deviations to which data normalisation should flatten high values, will not flatten if
        `None`, by default `None`

    Returns
    -------
    fig : Figure
        output figure object of the visualisation
    """

    # Baseline correction of data if given a baseline dataset
    if baseline_data is not None:
        data = baseline_correction(data, baseline_data)

    # Clean the order of the data
    data = clean_data(data)

    # Normalise data over a better range
    data = normalise_data(data, flatten)

    # Create anomaly from data readings
    anomaly = create_anomaly(data)

    # Create mesh
    mesh_obj, el_pos = mesh.create(16, h0=0.1, fd=circle)
    mesh_new = mesh.set_perm(mesh_obj, anomaly=anomaly, background=BACKGROUND)

    # Setup EIT scan conditions
    el_dist, step = 1, 1
    ex_mat = eit_scan_lines(16, el_dist)

    # FEM forward simulations
    fwd = Forward(mesh_obj, el_pos)
    f0 = fwd.solve_eit(ex_mat, step=step, perm=mesh_obj["perm"])
    f1 = fwd.solve_eit(ex_mat, step=step, perm=mesh_new["perm"])

    # Construct using GREIT
    eit = greit.GREIT(mesh_obj, el_pos, ex_mat=ex_mat, step=step, parser="std")
    eit.setup(p=0.50, lamb=0.001)
    ds = eit.solve(f1.v, f0.v)
    x, y, ds = eit.mask_value(ds, mask_value=np.NAN)

    # Graph setup
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    fig.set_size_inches(6, 4)
    ax.axis("equal")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

    # Extra visual details
    circle2 = plt.Circle((16, 16), 16, color="black", fill=False)
    ax.add_patch(circle2)

    # Plot the position of the electrodes
    points_arr = create_16_point_circle(16, 16, 16)
    x, y = points_arr.T
    ax.plot(x, y, "ro")

    # Plot the name of the electrodes
    points_arr = points_arr + np.array([.5, .5])
    for i in range(0, len(points_arr) // 2):
        ax.annotate(str(i + 1) + "A", xy=(points_arr[2 * i][0], points_arr[2 * i][1]), color="red")
        ax.annotate(str(i + 1) + "B", xy=(points_arr[2 * i + 1][0], points_arr[2 * i + 1][1]), color="red")

    im = ax.imshow(np.real(ds), interpolation="none", cmap=plt.cm.viridis)
    fig.colorbar(im, ax=ax)

    return fig


def clean_data(data: list[float]):
    """ Clean data order by hand, to undo alphabetical sort """

    # Note: R, L, FL, FR
    data[0], data[1], data[2], data[3] = data[1], data[2], data[3], data[0]
    data[16], data[17], data[18], data[19] = data[17], data[18], data[19], data[16]
    data[20], data[21], data[22], data[23] = data[22], data[23], data[20], data[21]
    data[24], data[25], data[26], data[27] = data[26], data[27], data[24], data[25]
    data[28], data[29], data[30], data[31] = data[30], data[31], data[28], data[29]

    return data


def normalise_data(data: list[float], flatten: Optional[int] = None):
    """ Shifts all the data to a scale with lowest value 1 and optionally flattens high values to within flatten
    standard deviations """

    if flatten is not None:
        upper_outlier_boundary = np.mean(data) + (flatten * float(np.std(data)))
        for i in range(len(data)):
            if data[i] > upper_outlier_boundary:
                data[i] = upper_outlier_boundary

    min_value = min(data)

    if min_value <= 0:
        data = np.ndarray.tolist(np.array(data) + np.absolute(min_value) + 1)

    return data


def baseline_correction(data: list[float], baseline_data: list[float]):
    """ Create a new dataset by subtracting the baseline data reading from the experimental data """

    corrected_data = np.ndarray.tolist(np.array(data) - np.array(baseline_data))

    return corrected_data


def create_16_point_circle(x: int, y: int, r: int):
    """ Helper function to return array of 16 evenly spaced points around circle with center (x, y) and radius r """
    points = []
    num_points = 16

    for i in range(num_points):
        points.append(
            [
                r * np.sin((i * 2 * np.pi) / num_points),
                -r * np.cos((i * 2 * np.pi) / num_points),
            ]
        )

    points_arr = np.array(points) + np.array([x, y])

    return points_arr


# This code is only run when running this specific file for testing purposes
if __name__ == "__main__":

    FILE_PATH = "..\\data\\First_Set\\Blockage_25.xlsx"
    BASELINE_PATH = "..\\data\\First_Set\\Blockage_0.xlsx"
    FREQ = 90

    try:
        file = pd.read_excel(FILE_PATH, sheet_name=None, engine="openpyxl")
        spreadsheet = list(file.values())[0]
        data = list(spreadsheet[FREQ])
    except FileNotFoundError:
        print("Error: File at path '" + FILE_PATH + "' was not found.")
        raise

    try:
        file = pd.read_excel(BASELINE_PATH, sheet_name=None, engine="openpyxl")
        spreadsheet = list(file.values())[0]
        baseline_data = list(spreadsheet[FREQ])
    except FileNotFoundError:
        print("Error: File at path '" + BASELINE_PATH + "' was not found.")
        baseline_data = None
        raise

    fig = greit_visualisation(data, baseline_data=baseline_data, flatten=1)

    plt.show()
