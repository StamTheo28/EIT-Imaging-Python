import pandas as pd


def open_file_at_frequency(input_path: str, freq: int, baseline_path: str = ""):
    """ Open data file(s) at a given frequency

    Parameters
    ----------
    input_path : str
        path string of the input data
    freq : int
        frequency for which to extract data
    baseline_path : str, optional
        path string of the baseline data, by default ""

    Returns
    -------
    tuple[list, list | None]
        tuple of the input data and the optional baseline data at the given frequency
    """

    # Raise ValueError if frequency is out of range
    if freq not in range(20, 101):
        raise ValueError("Please enter a whole number frequency between 20 and 100 inclusive")

    # Open data file
    try:
        file = pd.read_excel(input_path, sheet_name=None, engine="openpyxl")
    except FileNotFoundError:
        raise FileNotFoundError("Input file at path '" + input_path + "' was not found.\n")
    except ValueError:
        raise ValueError("Invalid file path. Input a valid file path string with \'-i [INPUT_PATH]\' and try again.\n")

    # Extract input data at the frequency provided
    spreadsheet = list(file.values())[0]
    input_data = list(spreadsheet[freq])

    # Open baseline data file if provided
    if baseline_path != "":
        try:
            file = pd.read_excel(baseline_path, sheet_name=None, engine="openpyxl")
        except FileNotFoundError:
            raise FileNotFoundError("Baseline file at path '" + baseline_path + "' was not found.")
        except ValueError:
            raise ValueError("Invalid file path. Input a valid file path string with \'-b [BASELINE_PATH]\' and try " +
                             "again.\n")

        # Extract data or set it as None if no data was provided
        spreadsheet = list(file.values())[0]
        baseline_data = list(spreadsheet[freq])
    else:
        baseline_data = None

    return input_data, baseline_data
