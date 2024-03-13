Supported Plot Types
===========================================

Plot Serializer currently supports the following plot types.

Line
---------------------------------

Line Plots will serialize the label of the plot, its linestyle, linewidth on top of the x-/y-data and their color. The color must be given as a string.

.. code-block:: python

    fig, ax = serializer.subplots()

    x = [1,2,3]
    y = [1,4,9]

    ax.plot(x,y,linestyle="--", lw=0.5, color="gray", label="xSquare")
    serializer.write_json_file("line_plot.json")
    plt.show()


Pie
---------------------------------
Pie Plots will serialize the color, size, radius, name and offset of each slice. The color must be given as a list of strings.

.. code-block:: python

    fig, ax = serializer.subplots()

    labels = "Frogs", "Hogs", "Dogs", "Logs"
    sizes = [15, 30, 45, 10]
    color = ["red", "green", "blue", "orange"]
    explode = [0.1, 0, 0.2, 0]

    ax.pie(sizes, labels=labels, colors=color, explode=explode)

    serializer.write_json_file("pie_plot.json")
    plt.show()

Bar
---------------------------------
Bar Plots will serialize the data and color of the bars. Color must be given as a list of strings.

.. code-block:: python

    fig, ax = serializer.subplots()

    names = ["a", "b", "c", "d", "e", "f", "g", "h"]
    heights = [10, 20, 30, 40, 50, 60, 70, 80]
    color = ["red", "green", "blue", "orange", "purple", "cyan", "blue", "blue"]

    ax.bar(names, heights, color=color)

    serializer.write_json_file("pie_plot.json")
    plt.show()

2D-Scatter
---------------------------------
2D-Scatter Plots will serialize the label of the plot and the datapoints, its sizes and colors. Thus supporting up to four dimensional data.
The colors can be passed as a string, a list of strings, a list of rgb/rgba tuples or a list of scalar values with a cmap.

.. code-block:: python

    fig, ax = serializer.subplots()

    x = [1,2,3]
    y = [1,4,9]
    sizes = [1,8,27]
    cScalar = [1, 16, 81]
    cmap = 'viridis'
    norm = 'linear'
    #c = "blue"
    #cList = ["blue", ""red", "green"]
    #cHex = ["0000ffff","ff0000ff","008000ff"]
    #cRGB = [(0.5,0.7,0.8), (0.7,0.1,0.2), (0.5,0.1,0.9)]
    #cRGBA = [(0.5,0.7,0.8,1), (0.7,0.1,0.2,1), (0.5,0.1,0.9,1)]


    ax.scatter(x, y, sizes=sizes, c=cScalar, cmap=cmap, norm=norm, label="power")

    serializer.write_json_file("pie_plot.json")
    plt.show()

3D-Scatter
---------------------------------
3D-Scatter Plots will serialize just like its 2D variant the label of the plot, the datapoints, their sizes and colors. 5D-Data can be represented.
The colors can be passed as a string, a list of strings, a list of rgb/rgba tuples or a list of scalar values with a cmap.
See 3D-Plots page in the documentation for the restrictions of creating a 3D-Axes via PlotSerializer.

.. code-block:: python

    fig, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    x = [1,2,3]
    y = [1,4,9]
    z = [1,16,81]
    sizes = [1,8,27]
    cScalar = [1, 16, 81]
    cmap = 'viridis'
    norm = 'linear'
    #c = "blue"
    #cList = ["blue", ""red", "green"]
    #cHex = ["0000ffff","ff0000ff","008000ff"]
    #cRGB = [(0.5,0.7,0.8), (0.7,0.1,0.2), (0.5,0.1,0.9)]
    #cRGBA = [(0.5,0.7,0.8,1), (0.7,0.1,0.2,1), (0.5,0.1,0.9,1)]


    ax.scatter(x, y, z, sizes=sizes, c=cScalar, cmap=cmap, norm=norm, label="power")

    serializer.write_json_file("pie_plot.json")
    plt.show()