import argparse
import sys

import matplotlib.pyplot as plt

from gui import VascuSensGUI
from visualisation import greit_visualisation
from filehelpers import open_file_at_frequency


def main():
    """ Main method of the Vascusense project. """

    # CLI argparse
    parser = argparse.ArgumentParser(
        description="Read in an excel spreadsheet (.xlsx) and process the data into a heatmap image.",
        exit_on_error=False)

    # Create mutually exclusive arg group for separate GUI and CLI functionality
    group = parser.add_mutually_exclusive_group()

    # Add GUI option
    group.add_argument("--gui", action="store_true", help="Whether to run the program with a gui or not")

    # Create CLI argument group
    cli_argument_group = group.add_argument_group()

    # Add CLI arguments
    cli_argument_group.add_argument("-i",
                                    "--input",
                                    type=str,
                                    help="A path string to a .xlsx file")
    cli_argument_group.add_argument("-c",
                                    "--frequency",
                                    default=100,
                                    type=int,
                                    help="The frequency to process. An integer between 20 and 100 inclusive, by defa" +
                                    "ult 100")
    cli_argument_group.add_argument("-b",
                                    "--baseline-path",
                                    default="",
                                    type=str,
                                    help="A path string to a .xlsx file to be used as a baseline")
    cli_argument_group.add_argument("-f",
                                    "--flatten",
                                    default=None,
                                    type=float,
                                    help="The number of standard deviations to which data normalisation should flatt" +
                                    "en high values, will not flatten if not passed")

    # Detect if the script was run without arguments, in which case the gui is used
    if len(sys.argv) == 1:
        # Create and run gui window loop
        program = VascuSensGUI()
        program.window.mainloop()

    # Else program is run through the CLI
    else:
        args = parser.parse_args()

        # Runs through CLI if GUI tag is missing/set to False
        if not args.gui:
            input_path = args.input
            freq = args.frequency
            baseline_path = args.baseline_path
            flatten = args.flatten

            # Open data files
            input_data, baseline_data = open_file_at_frequency(input_path, freq, baseline_path)

            # Create and show plot of the data
            fig = greit_visualisation(input_data, baseline_data=baseline_data, flatten=flatten)  # noqa: F841
            plt.show()

        else:
            # Create and run gui window loop
            program = VascuSensGUI()
            program.window.mainloop()


# Run main script in command line with:
# python main.py -i [INPUT] -c [FREQUENCY] -b [BASELINE_PATH] -f [FLATTEN]
# python main.py --gui
if __name__ == "__main__":
    main()
