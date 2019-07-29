# datadivr-demo
This is the supporting code for the demo version of the DataDiVR, a virtual reality-based network visualization application, maintained by Sebastian Pirch, Felix Müller, Jen Iofinova, and others at the [Jörg Menche Lab](http://www.menchelab.com) at the [Center for Molecular Medicine](http://www.cemm.oeaw.ac.at) of the Austrian Academy of Sciences, based in Vienna, Austria.

The visualization software itself can be downloaded using the script download_software.py. Note that for now this is not publicly available and the download is password-protected. Please contact us or file a support request in this github project if you would like to partner with us to apply the DataDiVR to your project.

## Instructions for using the DataDiVR

The DataDiVR comes pre-loaded with several networks already included, and so is ready to use as soon as it is installed. Additionally, it is easy to load your own networks into the DataDiVR.

*Note: this repository provides tools to assist in creating files for consumption by the DataDiVR. The use of these tools to produce and/or validate inputs is **strongly recommended**, as no errors or warnings will be raised by the DataDiVR itself.*

### File Structure
Each 3-dimensional "scene" viewable in the DataDiVR consists of a set of nodes. The full list of nodes, along with their names, any additional annotations, colors and (fixed) positions, is called a **layout**. Optionally, these nodes may be connected by undirected **links**. In addition, **labels**, which are text annotations not connected to any specific nodes, may be added to annotate groups of nodes. Finally, sets of particularly interesting nodes may be saved as a **selection**.

Each of these objects - layouts, links, labels, and selections - are written as .csv files. These files can be found in the directories below relative to the home directory of the DataDiVR:

- viveNet/Content/data/layouts
- viveNet/Content/data/links
- viveNet/Content/data/labels
-  viveNet/Content/data/Selections

Any .csv files found in those directories (but not in any subfolders) will be read by the DataDiVR, and will be discoverable from inside the VR. The naming conventions enforced by the software are as follows:

 - Links are always paired to exactly one layout, though a layout may have multiple sets of links, or no links at all. To signal the association, **the name of the links file must start with the name of the layout to which it is associated**. For example, if a layout is called "awesome_1.csv", its associated links list(s) may be called "awesome_1.csv" (not a conflict since layouts and links are in separate folders), or "awesome_1_sometext.csv". 
 - At most one labels file may be associated with a layout. The names must match exactly.
 - If the name of the layout ends with "_geo", the default view presented in the DataDiVR will feature a globe.

*You can check your file structure by running the **validate_file_structure.py** script.*

### File contents

#### Layouts
The layout files must be in csv format, with no header. The separator must be a comma, and no escaping separators is allowed. The columns are as follows:

 1. x-coordinate, a floating-point decimal between 0 and 1
 1. y-coordinate, a floating-point decimal between 0 and 1
 1. z-coordinate, a floating-point decimal between 0 and 1
 1. R (red) value of the RBG color of the node, an integer between 0 and 255 (inclusive)
1. G (green) value of the RGBA color of the node, an integer between 0 and 255 (inclusive)
2. B (blue) value of the RGBA color of the node, an integer between 0 and 255 (inclusive)
3. A (transparency) value of the RGBA color of the node, an integer between 0 and 255 (inclusive)
4. The name and any other annotation strings for the node, separated by semicolons (;). At least one name is required. **Please note that names and other annotations may not contain commas.**

*You can check your layouts by running the **validate_layouts.py** script.*

#### Links
The links files are likewise in .csv format with no header the following format:
1. Node 1 ID, an integer between 0 and num(nodes) - 1. The ID is simply the 0-indexed number of the line in the corresponding layout in which the node is described.
2. Node 2 ID, same as above.

Note that there is no need to list the edge twice - the edge (N1, N2) is equivalent to the edge (N2, N1).

*You can check your layouts by running the **validate_links.py** script.*

#### Labels
The labels .csv file should have the following columns:
 1. x-coordinate, a floating-point decimal between 0 and 1
 2. y-coordinate, a floating-point decimal between 0 and 1
 3. z-coordinate, a floating-point decimal between 0 and 1
 4. The text of the label. **Please note that the name of the label may not contain commas.**

*You can check your labels by running the **validate_labels.py** script.*

#### Selections
A selection file is simply a list of nodes, one node per line. As with links, the node IDs are the 0-indexed line numbers on which the node appears.

Example notebooks are provided to demonstrate the creation of DataDiVR inputs from other formats, for example from a NetworkX graph.
