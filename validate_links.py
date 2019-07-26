import os
from utils import *

DATADIVR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd()), "DataDiVR"))
LAYOUTS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/layouts")
LINKS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/links")
LABELS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/labels")

ERRORS_TO_SHOW=10

layouts = [f for f in os.listdir(LAYOUTS_DIR) if os.path.isfile(os.path.join(LAYOUTS_DIR, f)) and os.path.splitext(f)[1] == ".csv"]
layout_line_counts = {}
for layout in layouts:
    with open(os.path.join(LAYOUTS_DIR, layout)) as f:
        for i, l in enumerate(f):
            pass
    layout_line_counts[layout] = i+1


links_lists = [f for f in os.listdir(LINKS_DIR) if os.path.isfile(os.path.join(LINKS_DIR, f))]
for links_list in links_lists:
    record_errors = True
    bad_lines = []
    num_col_errors = 0
    num_idx_errors = 0
    matching_layouts = [layout for layout in layout_line_counts if links_list.startswith(os.path.splitext(layout)[0])]
    if not matching_layouts:
        print("ERROR: Links list without matching layout detected: %s." % links_list)
        continue
    shortest_matching_layout_length = min([layout_line_counts[layout] for layout in matching_layouts])

    with open(os.path.join(LINKS_DIR, links_list)) as f:
        for i, line in enumerate(f):
            line = line.split(",")
            # Validate number of columns
            if len(line) != 2:
                num_col_errors += 1
                if record_errors:
                    bad_lines.append(["Illegal number of columns", 6, len(line), i, ",".join(line)])
                    if len(bad_lines) == ERRORS_TO_SHOW:
                        record_errors = False
            # Validate references to nodes
            for x in range(2):
                if x >= len(line):
                    continue
                if not validate_index(line[x], shortest_matching_layout_length):
                    num_idx_errors += 1
                    if record_errors:
                        bad_lines.append(["Illegal node reference (out of range)", "int 0 <= i < %s" % line_count, line[x], i, ",".join(line)])
                        if len(bad_lines) == ERRORS_TO_SHOW:
                            record_errors = False

    if num_col_errors or num_idx_errors:
        print("FATAL ERROR: errors in file %s\n" % links_list)
        print("Note: Each row should contain exactly two comma-separated fields:\n"
              "    [N1, N2] \n"
              "    N1 and N2 are the 0-indexed IDs (line numbers) of the nodes in the corresponding layout.\n")

        asciitable(["Error type", "Count"], [list(x) for x in zip (["Invalid number of columns", "Invalid index values", "Invalid RGB values"],
                                                             [str(num_col_errors), str(num_idx_errors), str(num_rgb_errors)])])
        print("\nFirst %d errors:" % ERRORS_TO_SHOW)
        asciitable(["Issue", "Expected", "Got", "Line #", "Line"], bad_lines)
    else:
        print("All tests passed for %s!"% links_list)
