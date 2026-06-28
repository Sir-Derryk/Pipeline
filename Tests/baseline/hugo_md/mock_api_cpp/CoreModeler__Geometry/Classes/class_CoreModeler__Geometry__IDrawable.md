---
title: "IDrawable class"
sidebar_position: 2
parent: "CoreModeler::Geometry::Classes"
---

Interface for any elements that can be rendered to the display.

Represents a pure virtual C++ interface.

## Methods

### ~IDrawable
`virtual CoreModeler::Geometry::IDrawable::~IDrawable()=default`

### draw
`virtual void CoreModeler::Geometry::IDrawable::draw()=0`

Renders the drawable element to the screen.

### draw
`virtual int CoreModeler::Geometry::IDrawable::draw(RenderMode mode)=0`

Renders the drawable element using a specific render mode.

Overloaded method. 

mode

The rendering mode to use. 

Missing 

tag and incomplete documentation.

Overloaded method.

The rendering mode to use.

Missing

tag and incomplete documentation.

| Parameter | Type | Description |
| --- | --- | --- |
| mode | `RenderMode` |  |

