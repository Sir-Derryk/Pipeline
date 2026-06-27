---
title: "Box class"
sidebar_position: 1
parent: "CoreModeler::Geometry::Classes"
---

A 3D rectangular box shape.

## Methods

### Box
`CoreModeler::Geometry::Box::Box(double width, double height, double depth)`

Constructs a box with specified dimensions.

width

Width of the box. 

height

Height of the box. 

depth

Depth of the box.

Width of the box.

Height of the box.

Depth of the box.

| Parameter | Type | Description |
| --- | --- | --- |
| width | `double` |  |
| height | `double` |  |
| depth | `double` |  |

### getVolume
`double CoreModeler::Geometry::Box::getVolume() const override`

Inherited from Shape.

### draw
`void CoreModeler::Geometry::Box::draw() override`

Inherited from IDrawable.

### draw
`int CoreModeler::Geometry::Box::draw(RenderMode mode) override`

Inherited from IDrawable.

Missing 

and

tags.

Missing

and

| Parameter | Type | Description |
| --- | --- | --- |
| mode | `RenderMode` |  |

### scale
`void CoreModeler::Geometry::Box::scale(double factor)`

Scale the box by a uniform factor.

factor

Uniform scale factor.

Uniform scale factor.

| Parameter | Type | Description |
| --- | --- | --- |
| factor | `double` |  |

### scale
`void CoreModeler::Geometry::Box::scale(double xFactor, double yFactor, double zFactor)`

Scale the box non-uniformly by width, height, and depth factors.

Overloaded method. 

xFactor

Width scale factor. 

Missing

yFactor

and

zFactor

tags.

Overloaded method.

Width scale factor.

Missing

and

tags.

| Parameter | Type | Description |
| --- | --- | --- |
| xFactor | `double` |  |
| yFactor | `double` |  |
| zFactor | `double` |  |

