---
title: "GlobalLoggerProxy class"
sidebar_position: 4
parent: "Classes"
---

A global helper class for system-wide logging.
 This class is not inside any namespace.

## Fields

- `transient long GlobalLoggerProxy.swigCPtr`
- `transient boolean GlobalLoggerProxy.swigCMemOwn`

## Methods

### GlobalLoggerProxy
`GlobalLoggerProxy.GlobalLoggerProxy(long cPtr, boolean cMemoryOwn)`

| Parameter | Type | Description |
| --- | --- | --- |
| cPtr | `long` |  |
| cMemoryOwn | `boolean` |  |

### finalize
`void GlobalLoggerProxy.finalize()`

### getCPtr
`static long GlobalLoggerProxy.getCPtr(GlobalLoggerProxy obj)`

| Parameter | Type | Description |
| --- | --- | --- |
| obj | `GlobalLoggerProxy` |  |

### delete
`synchronized void GlobalLoggerProxy.delete()`

### logMessage
`void GlobalLoggerProxy.logMessage(String message)`

Writes a message to the global log.

message

The message to write.

The message to write.

| Parameter | Type | Description |
| --- | --- | --- |
| message | `String` |  |

### logMessage
`boolean GlobalLoggerProxy.logMessage(String message, int severity)`

Writes a formatted message to the global log with a severity level.
 Note: This is an overloaded method.

message

The message to write.
 Warning: The documentation for this overloaded method is missing the 

tag.

The message to write.
 Warning: The documentation for this overloaded method is missing the

tag.

| Parameter | Type | Description |
| --- | --- | --- |
| message | `String` |  |
| severity | `int` |  |

### forceFlush
`void GlobalLoggerProxy.forceFlush()`

Completely undocumented method returning void.

### GlobalLoggerProxy
`GlobalLoggerProxy.GlobalLoggerProxy()`

