Matplotlib PlotSerializer 0.2.0
================================
.. code-block:: json

    {
    "$defs": {
        "Axis": {
        "properties": {
            "label": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Label"
            },
            "scale": {
            "anyOf": [
                {
                "const": "linear"
                },
                {
                "const": "logarithmic"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Scale"
            }
        },
        "title": "Axis",
        "type": "object"
        },
        "Bar2D": {
        "properties": {
            "y": {
            "title": "Y",
            "type": "number"
            },
            "label": {
            "title": "Label",
            "type": "string"
            },
            "color": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Color"
            }
        },
        "required": [
            "y",
            "label"
        ],
        "title": "Bar2D",
        "type": "object"
        },
        "BarTrace2D": {
        "properties": {
            "type": {
            "const": "bar",
            "title": "Type"
            },
            "datapoints": {
            "items": {
                "$ref": "#/$defs/Bar2D"
            },
            "title": "Datapoints",
            "type": "array"
            }
        },
        "required": [
            "type",
            "datapoints"
        ],
        "title": "BarTrace2D",
        "type": "object"
        },
        "Box": {
        "properties": {
            "data": {
            "items": {
                "type": "number"
            },
            "title": "Data",
            "type": "array"
            },
            "label": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Label"
            },
            "usermedian": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Usermedian"
            },
            "conf_interval": {
            "anyOf": [
                {
                "maxItems": 2,
                "minItems": 2,
                "prefixItems": [
                    {
                    "type": "number"
                    },
                    {
                    "type": "number"
                    }
                ],
                "type": "array"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Conf Interval"
            }
        },
        "required": [
            "data"
        ],
        "title": "Box",
        "type": "object"
        },
        "BoxTrace2D": {
        "properties": {
            "type": {
            "const": "box",
            "title": "Type"
            },
            "notch": {
            "anyOf": [
                {
                "type": "boolean"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Notch"
            },
            "whis": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "maxItems": 2,
                "minItems": 2,
                "prefixItems": [
                    {
                    "type": "number"
                    },
                    {
                    "type": "number"
                    }
                ],
                "type": "array"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Whis"
            },
            "bootstrap": {
            "anyOf": [
                {
                "type": "integer"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Bootstrap"
            },
            "boxes": {
            "items": {
                "$ref": "#/$defs/Box"
            },
            "title": "Boxes",
            "type": "array"
            }
        },
        "required": [
            "type",
            "boxes"
        ],
        "title": "BoxTrace2D",
        "type": "object"
        },
        "LineTrace2D": {
        "properties": {
            "type": {
            "const": "line",
            "title": "Type"
            },
            "line_color": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Line Color"
            },
            "line_thickness": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Line Thickness"
            },
            "line_style": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Line Style"
            },
            "label": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Label"
            },
            "datapoints": {
            "items": {
                "$ref": "#/$defs/Point2D"
            },
            "title": "Datapoints",
            "type": "array"
            }
        },
        "required": [
            "type",
            "datapoints"
        ],
        "title": "LineTrace2D",
        "type": "object"
        },
        "LineTrace3D": {
        "properties": {
            "type": {
            "const": "line3D",
            "title": "Type"
            },
            "line_color": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Line Color"
            },
            "line_thickness": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Line Thickness"
            },
            "line_style": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Line Style"
            },
            "label": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Label"
            },
            "datapoints": {
            "items": {
                "$ref": "#/$defs/Point3D"
            },
            "title": "Datapoints",
            "type": "array"
            }
        },
        "required": [
            "type",
            "datapoints"
        ],
        "title": "LineTrace3D",
        "type": "object"
        },
        "PiePlot": {
        "properties": {
            "type": {
            "const": "pie",
            "title": "Type"
            },
            "title": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Title"
            },
            "slices": {
            "items": {
                "$ref": "#/$defs/Slice"
            },
            "title": "Slices",
            "type": "array"
            }
        },
        "required": [
            "type",
            "slices"
        ],
        "title": "PiePlot",
        "type": "object"
        },
        "Plot2D": {
        "properties": {
            "type": {
            "const": "2d",
            "title": "Type"
            },
            "title": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Title"
            },
            "x_axis": {
            "$ref": "#/$defs/Axis"
            },
            "y_axis": {
            "$ref": "#/$defs/Axis"
            },
            "traces": {
            "items": {
                "discriminator": {
                "mapping": {
                    "bar": "#/$defs/BarTrace2D",
                    "box": "#/$defs/BoxTrace2D",
                    "line": "#/$defs/LineTrace2D",
                    "scatter": "#/$defs/ScatterTrace2D"
                },
                "propertyName": "type"
                },
                "oneOf": [
                {
                    "$ref": "#/$defs/ScatterTrace2D"
                },
                {
                    "$ref": "#/$defs/LineTrace2D"
                },
                {
                    "$ref": "#/$defs/BarTrace2D"
                },
                {
                    "$ref": "#/$defs/BoxTrace2D"
                }
                ]
            },
            "title": "Traces",
            "type": "array"
            }
        },
        "required": [
            "type",
            "x_axis",
            "y_axis",
            "traces"
        ],
        "title": "Plot2D",
        "type": "object"
        },
        "Plot3D": {
        "properties": {
            "type": {
            "const": "3d",
            "title": "Type"
            },
            "title": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Title"
            },
            "x_axis": {
            "$ref": "#/$defs/Axis"
            },
            "y_axis": {
            "$ref": "#/$defs/Axis"
            },
            "z_axis": {
            "$ref": "#/$defs/Axis"
            },
            "traces": {
            "items": {
                "discriminator": {
                "mapping": {
                    "line3D": "#/$defs/LineTrace3D",
                    "scatter3D": "#/$defs/ScatterTrace3D",
                    "surface3D": "#/$defs/SurfaceTrace3D"
                },
                "propertyName": "type"
                },
                "oneOf": [
                {
                    "$ref": "#/$defs/ScatterTrace3D"
                },
                {
                    "$ref": "#/$defs/LineTrace3D"
                },
                {
                    "$ref": "#/$defs/SurfaceTrace3D"
                }
                ]
            },
            "title": "Traces",
            "type": "array"
            }
        },
        "required": [
            "type",
            "x_axis",
            "y_axis",
            "z_axis",
            "traces"
        ],
        "title": "Plot3D",
        "type": "object"
        },
        "Point2D": {
        "properties": {
            "x": {
            "title": "X",
            "type": "number"
            },
            "y": {
            "title": "Y",
            "type": "number"
            },
            "color": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Color"
            },
            "size": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Size"
            }
        },
        "required": [
            "x",
            "y"
        ],
        "title": "Point2D",
        "type": "object"
        },
        "Point3D": {
        "properties": {
            "x": {
            "title": "X",
            "type": "number"
            },
            "y": {
            "title": "Y",
            "type": "number"
            },
            "z": {
            "title": "Z",
            "type": "number"
            },
            "color": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Color"
            },
            "size": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Size"
            }
        },
        "required": [
            "x",
            "y",
            "z"
        ],
        "title": "Point3D",
        "type": "object"
        },
        "ScatterTrace2D": {
        "properties": {
            "type": {
            "const": "scatter",
            "title": "Type"
            },
            "label": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "title": "Label"
            },
            "datapoints": {
            "items": {
                "$ref": "#/$defs/Point2D"
            },
            "title": "Datapoints",
            "type": "array"
            }
        },
        "required": [
            "type",
            "label",
            "datapoints"
        ],
        "title": "ScatterTrace2D",
        "type": "object"
        },
        "ScatterTrace3D": {
        "properties": {
            "type": {
            "const": "scatter3D",
            "title": "Type"
            },
            "label": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "title": "Label"
            },
            "datapoints": {
            "items": {
                "$ref": "#/$defs/Point3D"
            },
            "title": "Datapoints",
            "type": "array"
            }
        },
        "required": [
            "type",
            "label",
            "datapoints"
        ],
        "title": "ScatterTrace3D",
        "type": "object"
        },
        "Slice": {
        "properties": {
            "size": {
            "title": "Size",
            "type": "number"
            },
            "radius": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Radius"
            },
            "offset": {
            "anyOf": [
                {
                "type": "number"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Offset"
            },
            "name": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Name"
            },
            "color": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Color"
            }
        },
        "required": [
            "size"
        ],
        "title": "Slice",
        "type": "object"
        },
        "SurfaceTrace3D": {
        "properties": {
            "type": {
            "const": "surface3D",
            "title": "Type"
            },
            "length": {
            "title": "Length",
            "type": "integer"
            },
            "width": {
            "title": "Width",
            "type": "integer"
            },
            "label": {
            "anyOf": [
                {
                "type": "string"
                },
                {
                "type": "null"
                }
            ],
            "default": null,
            "title": "Label"
            },
            "datapoints": {
            "items": {
                "$ref": "#/$defs/Point3D"
            },
            "title": "Datapoints",
            "type": "array"
            }
        },
        "required": [
            "type",
            "length",
            "width",
            "datapoints"
        ],
        "title": "SurfaceTrace3D",
        "type": "object"
        }
    },
    "properties": {
        "title": {
        "anyOf": [
            {
            "type": "string"
            },
            {
            "type": "null"
            }
        ],
        "default": null,
        "title": "Title"
        },
        "metadata": {
        "additionalProperties": {
            "anyOf": [
            {
                "type": "integer"
            },
            {
                "type": "number"
            },
            {
                "type": "string"
            }
            ]
        },
        "default": {},
        "title": "Metadata",
        "type": "object"
        },
        "plots": {
        "default": [],
        "items": {
            "discriminator": {
            "mapping": {
                "2d": "#/$defs/Plot2D",
                "3d": "#/$defs/Plot3D",
                "pie": "#/$defs/PiePlot"
            },
            "propertyName": "type"
            },
            "oneOf": [
            {
                "$ref": "#/$defs/PiePlot"
            },
            {
                "$ref": "#/$defs/Plot2D"
            },
            {
                "$ref": "#/$defs/Plot3D"
            }
            ]
        },
        "title": "Plots",
        "type": "array"
        }
    },
    "title": "Figure",
    "type": "object"
    }