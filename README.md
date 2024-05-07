# Overview

[[_TOC_]]

## Installation
Currently, Plot Serializer can only be installed from a local repository.

To install it, first clone this repository to a directory of your choice by navigating to the directory and executing

```cmd
git clone git@git.rwth-aachen.de:fst-tuda/projects/rdm/plot-serializer.git
```

Activate the pip environment into which you would like to install Plot Serializer. If you need to create a new pip environment, follow the section `Creating virtual environment` below.

With the pip environment activated, install Plot Serializer using pip, giving the path to the cloned repository:

```cmd
pip install path/to/directory/plot-serializer
```

## Documentation

View Plot Serializer's documentation on [Read the Docs](https://plot-serializer.readthedocs.io/en/latest/)

## Contributing
Clone this repository with

```cmd
git clone git@git.rwth-aachen.de:fst-tuda/projects/rdm/plot-serializer.git
```



### Creating the virtual environment
On Windows, run

```cmd
py -m venv env
```
The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it env.

venv will create a virtual Python installation in the env folder.

Before you can start installing or using packages in your virtual environment you’ll need to activate it. Activating a virtual environment will put the virtual environment-specific python and pip executables into your shell’s PATH.

```cmd
.\env\Scripts\activate
```

You can confirm you’re in the virtual environment by checking the location of your Python interpreter:

```cmd
where python
```
Tell pip to install all of the packages in the `requirements.txt` file using the -r flag:

```cmd
py -m pip install -r requirements.txt
```

Update the `requirements.txt` file when you install new packages.

For more detailed instructions, check https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/.

### Linting
This project uses the `flake8` linter and the `black` autoformatter.

### Documentation
Documentation is an essential part of writing code.

:warning: All public functions, methods, classes and modules must be properly documented with docstrings.

This project uses `google`-style docstrings. An example for a good docstring:

```python
def find_largest_distance(point, polygon):
    """Finds the largest distance between a point and the edges of a polygon.

    Args:
        point (shapely.geometry.Point): shapely point object
        polygon (shapely.geometry.Polygon): shapely polygon object

    Returns:
        float: the largest distance between a point and the edges of a polygon
    """
    distance_list = np.array([])
    for poly_point in list(zip(*polygon.exterior.coords.xy)):
        distance = point.distance(Point(poly_point))
        distance_list = np.append(distance_list, distance)
    max_distance = max(distance_list)
    return max_distance
```
because:
- [x] short and easy to understand description
- [x] starts with a verb in third person
- [x] `type` of the args are given
- [x] args and returns are described sufficiently

Where necessary, add additional information using comments.

### Naming Convention
Follow [Guido](https://en.wikipedia.org/wiki/Guido_van_Rossum)'s recommendations (taken from [Google Python Styleguide](https://google.github.io/styleguide/pyguide.html#3164-guidelines-derived-from-guidos-recommendations)):

<table rules="all" border="1" summary="Guidelines from Guido's Recommendations"
       cellspacing="2" cellpadding="2">

  <tr>
    <th>Type</th>
    <th>Public</th>
    <th>Internal</th>
  </tr>

  <tr>
    <td>Packages</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Modules</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>Classes</td>
    <td><code>CapWords</code></td>
    <td><code>_CapWords</code></td>
  </tr>

  <tr>
    <td>Exceptions</td>
    <td><code>CapWords</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Functions</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code></td>
  </tr>

  <tr>
    <td>Global/Class Constants</td>
    <td><code>CAPS_WITH_UNDER</code></td>
    <td><code>_CAPS_WITH_UNDER</code></td>
  </tr>

  <tr>
    <td>Global/Class Variables</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code></td>
  </tr>

  <tr>
    <td>Instance Variables</td>
    <td><code>lower_with_under</code></td>
    <td><code>_lower_with_under</code> (protected)</td>
  </tr>

  <tr>
    <td>Method Names</td>
    <td><code>lower_with_under()</code></td>
    <td><code>_lower_with_under()</code> (protected)</td>
  </tr>

  <tr>
    <td>Function/Method Parameters</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

  <tr>
    <td>Local Variables</td>
    <td><code>lower_with_under</code></td>
    <td></td>
  </tr>

</table>

For better readability, use meaningful, expressive names instead of hard-to-understand short names. Don’t drop letters from your source code. Although dropped letters in names like `memcpy` (memory copy) and `strcmp` (string compare) were popular in the C programming language before the 1990s, they’re an unreadable style of naming that you shouldn’t use today. If a name isn’t easily pronounceable, it isn’t easily understood.

Additionally, feel free to use short phrases that can make your code read like plain English. For example, `number_of_trials` is more readable than simply `number_trials`.

[More on naming.](https://inventwithpython.com/beyond/chapter4.html)

Use a spell checker.

### Code Structure
The maximum line length is 120 characters.

Whitespaces should be automatically deleted; the autoformatter should take care of this.

Improve readability by limiting the number of nested statements.

Preferrably write short functions, and [pure functions](https://realpython.com/python-functional-programming/#:~:text=A%20pure%20function%20is%20a,to%20state%20or%20mutable%20data.) that can be tested.
