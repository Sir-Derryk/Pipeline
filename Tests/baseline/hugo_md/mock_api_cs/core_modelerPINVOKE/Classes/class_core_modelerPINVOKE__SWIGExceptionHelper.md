---
title: "SWIGExceptionHelper class"
sidebar_position: 1
parent: "core_modelerPINVOKE.Classes"
---

## Fields

- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.applicationDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.arithmeticDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.divideByZeroDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.indexOutOfRangeDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.invalidCastDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.invalidOperationDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.ioDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.nullReferenceDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.outOfMemoryDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.overflowDelegate`
- `ExceptionDelegate core_modelerPINVOKE.SWIGExceptionHelper.systemDelegate`
- `ExceptionArgumentDelegate core_modelerPINVOKE.SWIGExceptionHelper.argumentDelegate`
- `ExceptionArgumentDelegate core_modelerPINVOKE.SWIGExceptionHelper.argumentNullDelegate`
- `ExceptionArgumentDelegate core_modelerPINVOKE.SWIGExceptionHelper.argumentOutOfRangeDelegate`

## Methods

### ExceptionDelegate
`delegate void core_modelerPINVOKE.SWIGExceptionHelper.ExceptionDelegate(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### ExceptionArgumentDelegate
`delegate void core_modelerPINVOKE.SWIGExceptionHelper.ExceptionArgumentDelegate(string message, string paramName)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |
| paramName | `string` |  |

### SWIGRegisterExceptionCallbacks_core_modeler
`static void core_modelerPINVOKE.SWIGExceptionHelper.SWIGRegisterExceptionCallbacks_core_modeler(ExceptionDelegate applicationDelegate, ExceptionDelegate arithmeticDelegate, ExceptionDelegate divideByZeroDelegate, ExceptionDelegate indexOutOfRangeDelegate, ExceptionDelegate invalidCastDelegate, ExceptionDelegate invalidOperationDelegate, ExceptionDelegate ioDelegate, ExceptionDelegate nullReferenceDelegate, ExceptionDelegate outOfMemoryDelegate, ExceptionDelegate overflowDelegate, ExceptionDelegate systemExceptionDelegate)`

| Parameter | Type | Description |
| --- | --- | --- |
| applicationDelegate | `ExceptionDelegate` |  |
| arithmeticDelegate | `ExceptionDelegate` |  |
| divideByZeroDelegate | `ExceptionDelegate` |  |
| indexOutOfRangeDelegate | `ExceptionDelegate` |  |
| invalidCastDelegate | `ExceptionDelegate` |  |
| invalidOperationDelegate | `ExceptionDelegate` |  |
| ioDelegate | `ExceptionDelegate` |  |
| nullReferenceDelegate | `ExceptionDelegate` |  |
| outOfMemoryDelegate | `ExceptionDelegate` |  |
| overflowDelegate | `ExceptionDelegate` |  |
| systemExceptionDelegate | `ExceptionDelegate` |  |

### SWIGRegisterExceptionCallbacksArgument_core_modeler
`static void core_modelerPINVOKE.SWIGExceptionHelper.SWIGRegisterExceptionCallbacksArgument_core_modeler(ExceptionArgumentDelegate argumentDelegate, ExceptionArgumentDelegate argumentNullDelegate, ExceptionArgumentDelegate argumentOutOfRangeDelegate)`

| Parameter | Type | Description |
| --- | --- | --- |
| argumentDelegate | `ExceptionArgumentDelegate` |  |
| argumentNullDelegate | `ExceptionArgumentDelegate` |  |
| argumentOutOfRangeDelegate | `ExceptionArgumentDelegate` |  |

### SetPendingApplicationException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingApplicationException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingArithmeticException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingArithmeticException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingDivideByZeroException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingDivideByZeroException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingIndexOutOfRangeException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingIndexOutOfRangeException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingInvalidCastException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingInvalidCastException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingInvalidOperationException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingInvalidOperationException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingIOException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingIOException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingNullReferenceException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingNullReferenceException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingOutOfMemoryException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingOutOfMemoryException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingOverflowException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingOverflowException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingSystemException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingSystemException(string message)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |

### SetPendingArgumentException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingArgumentException(string message, string paramName)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |
| paramName | `string` |  |

### SetPendingArgumentNullException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingArgumentNullException(string message, string paramName)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |
| paramName | `string` |  |

### SetPendingArgumentOutOfRangeException
`static void core_modelerPINVOKE.SWIGExceptionHelper.SetPendingArgumentOutOfRangeException(string message, string paramName)`

| Parameter | Type | Description |
| --- | --- | --- |
| message | `string` |  |
| paramName | `string` |  |

### SWIGExceptionHelper
`static core_modelerPINVOKE.SWIGExceptionHelper.SWIGExceptionHelper()`

