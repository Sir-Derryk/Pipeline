---
title: "Shape class"
sidebar_position: 6
parent: "CoreModeler::Geometry.Classes"
---

Base abstract class for geometric shapes.

## Fields

- `transient long CoreModeler.Geometry.Shape.swigCPtr`
- `transient boolean CoreModeler.Geometry.Shape.swigCMemOwn`

## Methods

### Shape
`CoreModeler.Geometry.Shape.Shape(long cPtr, boolean cMemoryOwn)`

| Parameter | Type | Description |
| --- | --- | --- |
| cPtr | `long` |  |
| cMemoryOwn | `boolean` |  |

### finalize
`void CoreModeler.Geometry.Shape.finalize()`

### getCPtr
`static long CoreModeler.Geometry.Shape.getCPtr(Shape obj)`

| Parameter | Type | Description |
| --- | --- | --- |
| obj | `Shape` |  |

### delete
`synchronized void CoreModeler.Geometry.Shape.delete()`

### getVolume
`double CoreModeler.Geometry.Shape.getVolume()`

Retrieves the volume of the shape.
 The shape's volume as a double.

The shape's volume as a double.

