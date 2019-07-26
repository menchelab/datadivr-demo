import os
from utils import *

DATADIVR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd()), "DataDiVR"))
LAYOUTS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/layouts")
LINKS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/links")
LABELS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/labels")

ERRORS_TO_SHOW=10

labels_lists = [f for f in os.listdir(LABELS_DIR) if os.path.isfile(os.path.join(LABELS_DIR, f))]

for labels_list in labels_lists:
    record_errors = True
    bad_lines = []
    num_col_errors = 0
    num_xyz_errors = 0
    num_val_errors = 0

    with open(os.path.join(LABELS_DIR, labels_list)) as f:
        for i, line in enumerate(f):
            line = line.split(",")
            # Check number of columns (columns are comma-separated; commas may not be escaped in any way)
            if len(line) != 4:
                num_col_errors += 1
                if record_errors:
                    bad_lines.append(["Illegal number of columns", 4, len(line), i, ",".join(line)])
                    if len(bad_lines) == ERRORS_TO_SHOW:
                        record_errors = False
            # Validate XYZ columns
            for x in range(3):
                if x >= len(line):
                    continue
                if not validate_coordinate(line[x]):
                    num_xyz_errors += 1
                    if record_errors:
                        bad_lines.append(["illegal XYZ values", "float 0 <= f <= 1", line[x], i, ",".join(line)])
                        if len(bad_lines) == ERRORS_TO_SHOW:
                            record_errors = False
            # Check value of label
            for x in range(3,4):
                if x >= len(line):
                    continue
                if not line[x]:
                    num_val_errors += 1
                    if record_errors:
                        bad_lines.append(["Missing value to display", "any string", "", i, ",".join(line)])
                        if len(bad_lines) == ERRORS_TO_SHOW:
                            record_errors = False

    # Display any errors
    if num_col_errors or num_xyz_errors or num_val_errors:
        print("FATAL ERROR: errors in labels list %s\n" % labels_list)
        print("Hint: Each row should contain exactly 4 comma-separated fields:\n"
              "    [X, Y, Z, value]\n"
              "    X, Y, and Z are the coordinates of the location of the node and should be floats between 0 and 1,\n"
              "    Value is the value of the label that should be displayed.\n")

        asciitable(["Error type", "Count"], [list(x) for x in zip (["Invalid number of columns", "Invalid XYZ values", "Missing label"],
                                                             [str(num_col_errors), str(num_xyz_errors), str(num_val_errors)])])
        print("\nFirst %d errors:" % ERRORS_TO_SHOW)
        asciitable(["Issue", "Expected", "Got", "Line #", "Line"], bad_lines)
