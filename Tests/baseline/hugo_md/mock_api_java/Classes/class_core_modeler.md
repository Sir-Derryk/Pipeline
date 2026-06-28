---
title: "core_modeler class"
sidebar_position: 1
parent: "Classes"
---

## Methods

### setG_systemState
`static void core_modeler.setG_systemState(int value)`

A global variable containing the current system state.
 This variable is updated by the global initialization functions.

| Parameter | Type | Description |
| --- | --- | --- |
| value | `int` |  |

### getG_systemState
`static int core_modeler.getG_systemState()`

A global variable containing the current system state.
 This variable is updated by the global initialization functions.

### setG_piValue
`static void core_modeler.setG_piValue(double value)`

A global mathematical constant for Pi.
 No documentation tags here, testing completely missing tag description.

| Parameter | Type | Description |
| --- | --- | --- |
| value | `double` |  |

### getG_piValue
`static double core_modeler.getG_piValue()`

A global mathematical constant for Pi.
 No documentation tags here, testing completely missing tag description.

### globalInitialize
`static int core_modeler.globalInitialize(GlobalConfig config)`

Initializes the global system components.
 This function is undocumented for parameters and return values.

config

The configuration to apply.

The configuration to apply.

| Parameter | Type | Description |
| --- | --- | --- |
| config | `GlobalConfig` |  |

### getDIAG_SUCCESS
`static long core_modeler.getDIAG_SUCCESS()`

Constant representing a successful diagnostic run.

### getDIAG_FAILURE
`static long core_modeler.getDIAG_FAILURE()`

Constant representing a generic diagnostic failure.

### setG_diagnosticRunCount
`static void core_modeler.setG_diagnosticRunCount(long value)`

A global variable representing the total number of diagnostic runs.

| Parameter | Type | Description |
| --- | --- | --- |
| value | `long` |  |

### getG_diagnosticRunCount
`static long core_modeler.getG_diagnosticRunCount()`

A global variable representing the total number of diagnostic runs.

### checkSystemHealth
`static long core_modeler.checkSystemHealth()`

Checks the current health status of the system.
 Note: Missing tag.

tag.

### pingSubsystem
`static boolean core_modeler.pingSubsystem(long timeoutMs)`

Performs a ping to verify subsystem responsiveness.
 This is an overloaded function.

timeoutMs

Timeout in milliseconds.
 Note: Missing 

tag.

Timeout in milliseconds.
 Note: Missing

tag.

| Parameter | Type | Description |
| --- | --- | --- |
| timeoutMs | `long` |  |

### pingSubsystem
`static boolean core_modeler.pingSubsystem()`

Performs a ping to verify subsystem responsiveness using a default timeout.
 This is an overloaded function.
 Note: Completely undocumented function, tests parser fallback.

### resetCounters
`static void core_modeler.resetCounters()`

Resets the internal diagnostic counters.

