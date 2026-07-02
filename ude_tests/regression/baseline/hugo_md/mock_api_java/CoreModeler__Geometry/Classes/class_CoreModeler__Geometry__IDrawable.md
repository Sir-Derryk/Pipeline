---
title: "IDrawable class"
sidebar_position: 2
parent: "CoreModeler::Geometry.Classes"
---

Interface for any elements that can be rendered to the display.
 Represents a pure virtual C++ interface.

## Fields

- `transient long CoreModeler.Geometry.IDrawable.swigCPtr`
- `transient boolean CoreModeler.Geometry.IDrawable.swigCMemOwn`

## Methods

### IDrawable
`CoreModeler.Geometry.IDrawable.IDrawable(long cPtr, boolean cMemoryOwn)`

| Parameter | Type | Description |
| --- | --- | --- |
| cPtr | `long` |  |
| cMemoryOwn | `boolean` |  |

### finalize
`void CoreModeler.Geometry.IDrawable.finalize()`

### getCPtr
`static long CoreModeler.Geometry.IDrawable.getCPtr(IDrawable obj)`

| Parameter | Type | Description |
| --- | --- | --- |
| obj | `IDrawable` |  |

### delete
`synchronized void CoreModeler.Geometry.IDrawable.delete()`

### renderToScreen
`void CoreModeler.Geometry.IDrawable.renderToScreen()`

Renders the drawable element to the screen.

### renderToScreen
`int CoreModeler.Geometry.IDrawable.renderToScreen(CoreModeler.RenderMode mode)`

Renders the drawable element using a specific render mode.
 Note: Overloaded method.

mode

The rendering mode to use.
 Warning: Missing 

tag and incomplete documentation.

The rendering mode to use.
 Warning: Missing

tag and incomplete documentation.

| Parameter | Type | Description |
| --- | --- | --- |
| mode | `CoreModeler.RenderMode` |  |

