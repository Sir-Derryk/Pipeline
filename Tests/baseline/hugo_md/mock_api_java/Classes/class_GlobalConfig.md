---
title: "GlobalConfig class"
sidebar_position: 3
parent: "Classes"
---

Global configuration structure used to initialize the SDK.

## Fields

- `transient long GlobalConfig.swigCPtr`
- `transient boolean GlobalConfig.swigCMemOwn`

## Methods

### GlobalConfig
`GlobalConfig.GlobalConfig(long cPtr, boolean cMemoryOwn)`

| Parameter | Type | Description |
| --- | --- | --- |
| cPtr | `long` |  |
| cMemoryOwn | `boolean` |  |

### finalize
`void GlobalConfig.finalize()`

### getCPtr
`static long GlobalConfig.getCPtr(GlobalConfig obj)`

| Parameter | Type | Description |
| --- | --- | --- |
| obj | `GlobalConfig` |  |

### delete
`synchronized void GlobalConfig.delete()`

### setMaxThreads
`void GlobalConfig.setMaxThreads(int value)`

The maximum number of concurrent threads.

| Parameter | Type | Description |
| --- | --- | --- |
| value | `int` |  |

### getMaxThreads
`int GlobalConfig.getMaxThreads()`

The maximum number of concurrent threads.

### setEnableLogging
`void GlobalConfig.setEnableLogging(boolean value)`

Flag to enable or disable verbose log output.

| Parameter | Type | Description |
| --- | --- | --- |
| value | `boolean` |  |

### getEnableLogging
`boolean GlobalConfig.getEnableLogging()`

Flag to enable or disable verbose log output.

### setTimeoutSeconds
`void GlobalConfig.setTimeoutSeconds(double value)`

Timeout duration in seconds.

| Parameter | Type | Description |
| --- | --- | --- |
| value | `double` |  |

### getTimeoutSeconds
`double GlobalConfig.getTimeoutSeconds()`

Timeout duration in seconds.

### GlobalConfig
`GlobalConfig.GlobalConfig()`

