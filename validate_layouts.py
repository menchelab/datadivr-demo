import os
from utils import *

DATADIVR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd()), "DataDiVR"))
LAYOUTS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/layouts")
LINKS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/links")
LABELS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/labels")

ERRORS_TO_SHOW=10

# Check that each line has exactly 8 fields:
# [X, Y, Z, R, G, B, A, ?, One or more names, separated by colons]
# Of these, the first three should be floats between 0 and 1,
# the next four should be integers between 0 and 255.

print("\n!!!!!!!!!!!!!! Checking layouts files !!!!!!!!!!!!!!\n")


layouts = [f for f in os.listdir(LAYOUTS_DIR) if os.path.isfile(os.path.join(LAYOUTS_DIR, f)) and os.path.splitext(f)[1] == ".csv"]
layout_line_counts = {}
for layout in layouts:
    print("Evaluating layout ", os.path.join(LAYOUTS_DIR, layout))
    line_count = 0
    record_errors = True
    bad_lines = []
    num_col_errors = 0
    num_xyz_errors = 0
    num_rgb_errors = 0

    with open(os.path.join(LAYOUTS_DIR, layout)) as f:
        for i, line in enumerate(f):
            line_count += 1
            line = line.split(",")
            # Check number of columns (columns are comma-separated; commas may not be escaped in any way)
            if len(line) != 8:
                num_col_errors += 1
                if record_errors:
                    bad_lines.append(["Illegal number of columns", 8, len(line), i, ",".join(line)])
                    if len(bad_lines) == ERRORS_TO_SHOW:
                        record_errors = False
            for x in range(3):
                if x >= len(line):
                    continue
                if not validate_coordinate(line[x]):
                    num_xyz_errors += 1
                    if record_errors:
                        bad_lines.append(["illegal XYZ values", "float 0 <= f <= 1", line[x], i, ",".join(line)])
                        if len(bad_lines) == ERRORS_TO_SHOW:
                            record_errors = False
            for x in range(3, 7):
                if x >= len(line):
                    continue
                if not validate_color_value(line[x]):
                    num_rgb_errors += 1
                    if record_errors:
                        bad_lines.append(["illegal RGBA values", "int 0 <= i <= 255", line[x], i, ",".join(line)])
                        if len(bad_lines) == ERRORS_TO_SHOW:
                            record_errors = False

    layout_line_counts[layout] = line_count

    # Display any errors
    if num_col_errors or num_xyz_errors or num_rgb_errors:
        print("FATAL ERROR: errors in layout %s\n" % os.path.join(LAYOUTS_DIR, layout))
        print("Hint: Each row should contain exactly 8 comma-separated fields:\n"
              "    [X, Y, Z, R, G, B, A, names]\n"
              "    X, Y, and Z are the coordinates of the location of the node and should be floats between 0 and 1,\n"
              "    R, G, B, and A are color/saturation values and should be integers between 0 and 255.\n"
              "    At least one name must be given;\n"
              "        multiple names or attributes are allowed, separated by semicolons (';').\n")

        asciitable(["Error type", "Count"], [list(x) for x in zip (["Invalid number of columns", "Invalid XYZ values", "Invalid RGBA values"],
                                                             [str(num_col_errors), str(num_xyz_errors), str(num_rgb_errors)])])
        print("\nFirst %d errors:" % ERRORS_TO_SHOW)
        asciitable(["Issue", "Expected", "Got", "Line #", "Line"], bad_lines)
    else:
        print("Layout %s OK\n" % layout)

