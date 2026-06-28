---
title: "Point3D class"
sidebar_position: 3
parent: "CoreModeler::Geometry::Classes"
---

Generic template representing a 3D coordinate point.

T

The numeric type (e.g., int, float, double).

The numeric type (e.g., int, float, double).

## Fields

- `T CoreModeler::Geometry::Point3D< T >::x`
- `T CoreModeler::Geometry::Point3D< T >::y`
- `T CoreModeler::Geometry::Point3D< T >::z`

## Methods

### Point3D
`CoreModeler::Geometry::Point3D< T >::Point3D()`

### Point3D
`CoreModeler::Geometry::Point3D< T >::Point3D(T valX, T valY, T valZ)`

| Parameter | Type | Description |
| --- | --- | --- |
| valX | `T` |  |
| valY | `T` |  |
| valZ | `T` |  |

### translate
`void CoreModeler::Geometry::Point3D< T >::translate(T dx, T dy, T dz)`

Translates the point by given offsets.

dx

Offset in X direction. 

dy

Offset in Y direction. 

Missing

dz

documentation tag.

Offset in X direction.

Offset in Y direction.

Missing

documentation tag.

| Parameter | Type | Description |
| --- | --- | --- |
| dx | `T` |  |
| dy | `T` |  |
| dz | `T` |  |

