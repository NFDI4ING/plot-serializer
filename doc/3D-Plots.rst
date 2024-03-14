Serializing 3D-Plots
===========================================

PlotSerializer only supports the initiazation of the figure and axes via the subplots method.
The following two step initialisation to draw a 3D plot is not supported:

.. code-block:: python

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x = [1,2,3]
    y = [3,2,4]
    z = [4,4,4]

    ax.scatter(x,y,z)
    plt.show()

Instead you have to add the projection attribute into the subplots method:

.. code-block:: python

    from plot_serializer.matplotlib.serializer import MatplotlibSerializer

    fig, ax = serializer.subplots(subplot_kw={"projection": "3d"})

    x = [1,2,3]
    y = [3,2,4]
    z = [4,4,4]

    ax.scatter(x,y,z)
    plt.show()




