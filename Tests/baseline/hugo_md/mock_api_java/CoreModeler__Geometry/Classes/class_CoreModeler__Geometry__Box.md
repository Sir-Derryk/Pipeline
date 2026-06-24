---
title: "Box class"
sidebar_position: 1
parent: "CoreModeler::Geometry.Classes"
---

A 3D rectangular box shape.

## Fields

- `transient long CoreModeler.Geometry.Box.swigCPtr`

## Methods

### Box
`CoreModeler.Geometry.Box.Box(long cPtr, boolean cMemoryOwn)`

| Parameter | Type | Description |
| --- | --- | --- |
| cPtr | `long` |  |
| cMemoryOwn | `boolean` |  |

### finalize
`void CoreModeler.Geometry.Box.finalize()`

### getCPtr
`static long CoreModeler.Geometry.Box.getCPtr(Box obj)`

| Parameter | Type | Description |
| --- | --- | --- |
| obj | `Box` |  |

### delete
`synchronized void CoreModeler.Geometry.Box.delete()`

### Box
`CoreModeler.Geometry.Box.Box(double width, double height, double depth)`

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
`double CoreModeler.Geometry.Box.getVolume()`

Inherited from Shape.

### renderToScreen
`void CoreModeler.Geometry.Box.renderToScreen()`

Inherited from IDrawable.

### renderToScreen
`int CoreModeler.Geometry.Box.renderToScreen(CoreModeler.RenderMode mode)`

Inherited from IDrawable.
 Note: Missing and

and

| Parameter | Type | Description |
| --- | --- | --- |
| mode | `CoreModeler.RenderMode` |  |

### scale
`void CoreModeler.Geometry.Box.scale(double factor)`

Scale the box by a uniform factor.

factor

Uniform scale factor.

Uniform scale factor.

| Parameter | Type | Description |
| --- | --- | --- |
| factor | `double` |  |

### scale
`void CoreModeler.Geometry.Box.scale(double xFactor, double yFactor, double zFactor)`

Scale the box non-uniformly by width, height, and depth factors.
 Note: Overloaded method.

xFactor

Width scale factor.
 Note: Missing

yFactor

and

zFactor

tags.

Width scale factor.
 Note: Missing

and

tags.

| Parameter | Type | Description |
| --- | --- | --- |
| xFactor | `double` |  |
| yFactor | `double` |  |
| zFactor | `double` |  |

