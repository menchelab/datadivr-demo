# With thanks to MattH on StackOverflow for sample code.

def asciitable(headers, rows):
  if len(rows) > 0:
    lens = []
    for i in range(len(rows[0])):
      lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
    formats = []
    hformats = []
    for i in range(len(rows[0])):
      if isinstance(rows[0][i], int):
        formats.append("%%%ds" % lens[i])
      else:
        formats.append("%%-%ds" % lens[i])
      hformats.append("%%-%ds" % lens[i])
    pattern = " | ".join(formats)
    hpattern = " | ".join(hformats)
    separator = "-+-".join(['-' * n for n in lens])
    print(hpattern % tuple(headers))
    print (separator)
    for line in rows:
        print (pattern % tuple(str(t) for t in line))
  elif len(rows) == 1:
    row = rows[0]
    hwidth = len(max(row._fields,key=lambda x: len(x)))
    for i in range(len(row)):
      print("%*s = %s" % (hwidth,row._fields[i],row[i]))


def validate_coordinate(x):
    try:
        x = float(x)
        return x >= 0 and x <= 1
    except:
        return False


def validate_color_value(x):
    try:
        x = int(x)
        return x >= 0 and x <= 255
    except:
        return False


def validate_index(x, num_points):
    try:
        x = int(x)
        return x < num_points
    except:
        return False
