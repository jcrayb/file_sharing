<style>
    h-center{
        display: flex;
        justify-content: center;
    }

    red-highlighter{
        background-color: red;
        color: black;
    }
</style>

# PrairieLearn Python Drawing Docs

The aim of this tool is to simplify and increase the efficiency of creating highly dynamic diagrams, i.e. diagrams that are very sensitive to changes in the problem's initial conditions. In such cases, one might find themselves declaring dozens of `data['params'][variable]` in their Python file and `{{ params.variable }}` in their HTML file. It becomes therefore hard to keep track of what has been declared, as well as keeping a consistant naming convention to prevent interference. 

This tool uses as close a syntax as possible to the original prairielearn HTML elements to avoid confusion and seemless transition. Therefore each element is named as closely as possible to its HTML counterpart, while simplifying where needed. For example:

- pl-rectangle => Rectangle
- pl-arc-vector => ArcVector
- pl-double-headed-vector => DoubleVector

For arguments, they follow the exact same names as the ones from PrairieLearn, except when they contain dashes, which are replaced by underscores due to limitations in Python. Therefore:

- x1 => x1
- width => width
- anchor-is-tail => anchor_is_tail.

## How to declare elements

First, import the tool by adding `from pl_drawing import *` into your `server.py` file. Then, when you need to start creating elements, simply declare them like any regular variable. For example:
<h-center>
```python 
circle1 = Circle(20, 20, 30, color='red', ...)
```
</h-center>

Some attributes are required, which shouldn't be named, and declared in their original order. Optional arguments should be declared using the `name=value` convention. Refer to the example above.

<red-highlighter>/!\ Warning /!\ </red-highlighter>, not all attributes are implemented, some rarely used ones are missing. Refer to the chart below to see which elements and attributes can be used. 

## Compiling elements and inserting into HTML page

Everytime an element is declared, its existence is kept track of under-the-hood. When time comes to convert the code into an HTML string, the tool contains a `compile()` function embeded into every element. This means any declared element can be used for this purpose. Using our previous example, we get:

```python 
dims = Dimensions(30, 40, 'L=30', width=30, angle=15)
code = circle1.compile()
```

which returns:

```HTML
<pl-circle x1=20 y1=20 radius=30 color='red'></pl-circle>
<pl-dimensions x1=30 y1=40 label='L=30' width=30 angle=15></pl-dimensions>
```

Here, using `dims.compile()` would've have produced the same result.

Elements are rendered in the order they are declared. Therefore if you have overlapping elements, keep in mind the order in which you want them to appear, as elements declared last will appear on top of those declared earlier.

## Elements currently supported:

Unless specified, all arguments are native to PrairieLearn and therefore documentation about them can be found <a href="https://prairielearn.readthedocs.io/en/latest/pl-drawing/">here.</a>

Every element is contained within a class of elements, which have shared attributed. For example all shapes contain the `color` and `opacity` arguments.

Every element has an `x1`, `y1` attribute, while most have `color` and `opacity`.

### Shapes: 

Common attributes:

- color
- opacity
- stroke_color (equiv. stroke-color) (except Line)
- stroke_width (equiv. stroke-width)

### Rectangle:
Equivalent: `<pl-rectangle>`.

#### Required arguments:

- `x1`
- `y1`
- `height`
- `width`

#### Optional arguments:

- `top_right_corner`: This isn't a native PrairieLearn option, but I've found it more intuitive to sometimes declare the coordinates of the top-right-corner instead of the center, especially if the height and width of the element is variable.
- `angle`

Example code:

```python
rect = Rectangle(x1, y1, height, width, top_right_corner=False, color="", opacity=float, stroke_color="", stroke_width=float, angle=float)
```
</h-center>

### Circle:
Equivalent: `<pl-circle>`.

#### Required arguments:

- `x1`
- `y1`
- `radius`

#### Optional arguments:

- `label`
- `angle`

Example code:

```python
circ = Circle(x1, y1, radius, color="", opacity=float, stroke_color="", stroke_width=float)
```

### Line:
Equivalent: `<pl-line>`.

#### Required arguments:

- `x1`
- `y1`

#### Optional arguments:

- `x2`
- `y2`
- `width`
- `angle`
- `dashed_size` (equiv. dashed-size)


Note: `x2, y2` and `width, angle` are supposed to be mutually exclusive, use one or the other, but not both. This tool doesn't have anything implemented to stop you from doing that, so beware the footgun.

Example code:

```python
line = Line(x1, y1, x2=float, y2=float, width=float, angle=float, dashed_size=float, stroke_width=float, color="", opacity=float)
```

### Label elements: 

Common attributes:

- label
- offsetx
- offsety

### Point:
Equivalent: `<pl-point>`.

#### Required arguments:

- `x1`
- `y1`
- `label`

#### Optional arguments:

- `radius`

Example code:

```python
point = Point(x1, y1, label, radius=float,offsetx=float, offsety=float, color="", opacity=float)
```

### Dimensions:
Equivalent: `<pl-dimensions>`.

#### Required arguments:

- `x1`
- `y1`
- `label`

#### Optional arguments:

- `x2`
- `y2`
- `width`
- `angle`
- `dashed_size`
- `arrow_head_width` (equiv. arrow-head-width)
- `arrow_head_length` (equiv. arrow-head-length)
- `stroke_color` (equiv. stroke-color)
- `stroke_width` (equiv. stroke-width)

Note: `x2, y2` and `width, angle` are supposed to be mutually exclusive, use one or the other, but not both. This tool doesn't have anything implemented to stop you from doing that, so beware the footgun.

Example code:

```python
dims = Dimensions(x1, y1, label, x2=float, y2=float, width=float, angle=float, arrow_head_width=float, arrow_head_length=float, stroke_color="", stroke_width=float, offsetx=float, offsety=float)
```

### Text:
Equivalent: `<pl-text>`.

#### Required arguments:

- `x1`
- `y1`
- `label`

#### Optional arguments:

- `latex`
- `font_size` (equiv. font-size)

Example code:

```python
text = Text(x1, y1, label, latex=True, font_size=float, offsetx=float, offsety=float)
```

### Vectors

Common attributes:

- color
- offsetx
- offsety
- arrow_head_width (equiv. arrow-head-width)
- arrow_head_length (equiv. arrow-head-length)
- stroke_width (equiv. stroke-width)

### Vector
Equivalent: `<pl-vector>`.

#### Required arguments:

- `x1`
- `y1`
- `label`

#### Optional arguments:

- `width`
- `angle`
- `anchor_is_tail` (equiv. anchor-is-tail)

Example code:

```python
vect = Vector(x1, y1, label, width=float, angle=float, anchor_is_tail=True, arrow_head_width=float, arrow_head_length=float, stroke_width=float, offsetx=float, offsety=float, color="")
```

### DoubleVector
Equivalent: `<pl-double-headed-vector>`.

#### Required arguments:

- `x1`
- `y1`
- `label`

#### Optional arguments:

- `width`
- `angle`
- `anchor_is_tail` (equiv. anchor-is-tail)

Example code:

```python
dvect = DoubleVector(x1, y1, label, width=float, angle=float, anchor_is_tail=True, arrow_head_width=float, arrow_head_length=float, stroke_width=float, offsetx=float, offsety=float, color="")
```

### ArcVector
Equivalent: `<pl-arc-vector>`.

#### Required arguments:

- `x1`
- `y1`
- `radius`
- `label`

#### Optional arguments:

- `draw_center` (equiv. draw-center)
- `start_angle` (equiv. start-angle)
- `end_angle` (equiv. end-angle)
- `clockwise_direction` (equiv. clockwise-direction)

Example code:

```python
avect = ArcVector(x1, y1, label, radius, draw_center=True, start_angle=float, end_angle=float, clockwise_direction=True, arrow_head_width=float, arrow_head_length=float, stroke_width=float, offsetx=float, offsety=float, color="")
```