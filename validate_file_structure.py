import os
from utils import asciitable

DATADIVR_PATH = os.path.realpath(os.path.join(os.path.dirname(os.getcwd()), "DataDiVR"))
LAYOUTS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/layouts")
LINKS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/links")
LABELS_DIR = os.path.join(DATADIVR_PATH, "viveNet/Content/data/labels")

layouts = [f for f in os.listdir(LAYOUTS_DIR) if os.path.isfile(os.path.join(LAYOUTS_DIR, f))]
links_lists = [f for f in os.listdir(LINKS_DIR) if os.path.isfile(os.path.join(LINKS_DIR, f))]
labels_lists = [f for f in os.listdir(LABELS_DIR) if os.path.isfile(os.path.join(LABELS_DIR, f))]

# We pair a links list to a layout if the name of the layout
# is a prefix (or an exact match to) the name of a links list.

layouts_with_links = [[layout, links_list, labels_list]
                      for layout in layouts
                      for links_list in links_lists
                      for labels_list in labels_lists
                      if labels_list.startswith(layout)]

layout_to_links = {}
for layout in layouts:
    layout_to_links[layout] = [l for l in links_lists if l.startswith(os.path.splitext(layout)[0])]
layout_to_labels = {}
for layout in layouts:
    layout_to_labels[layout] = [l for l in labels_lists if l.startswith(os.path.splitext(layout)[0])]
layouts.sort()

print("\n!!!!!!!!!!!!!! Checking file structure !!!!!!!!!!!!!!\n")

print("The following layouts with corresponding links/label lists were detected:")
asciitable(["layout", "links lists", "labels lists"],
           [[l, ", ".join(layout_to_links[l]) if layout_to_links[l] else '-',
             ", ".join(layout_to_labels[l]) if layout_to_labels[l] else '-'] for l in layouts])

mismatched_links_lists = [ll for ll in links_lists if not any(ll.startswith(l[:-4]) for l in layouts)]
if mismatched_links_lists:
    print("\n\nFATAL ERROR: The following links lists did not match any layout:\n",
          mismatched_links_lists,
          "\n(hint: the name of the links list must start with the full name of the layout to which it belongs.)")

mismatched_labels_lists = [ll for ll in labels_lists if not any(ll == l for l in layouts)]
if mismatched_labels_lists:
    print("\n\nERROR: The following labels lists did not match any layout:\n",
          mismatched_labels_lists,
          "\n(hint: the name of the labels list must start with the full name of the layout to which it belongs.)")

else:
    print("File structure tests passed!")
