---
title: "core_modelerJNI class"
sidebar_position: 2
parent: "Classes"
---

## Methods

### GlobalConfig_maxThreads_set
`static final native void core_modelerJNI.GlobalConfig_maxThreads_set(long jarg1, GlobalConfig jarg1_, int jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalConfig` |  |
| jarg2 | `int` |  |

### GlobalConfig_maxThreads_get
`static final native int core_modelerJNI.GlobalConfig_maxThreads_get(long jarg1, GlobalConfig jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalConfig` |  |

### GlobalConfig_enableLogging_set
`static final native void core_modelerJNI.GlobalConfig_enableLogging_set(long jarg1, GlobalConfig jarg1_, boolean jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalConfig` |  |
| jarg2 | `boolean` |  |

### GlobalConfig_enableLogging_get
`static final native boolean core_modelerJNI.GlobalConfig_enableLogging_get(long jarg1, GlobalConfig jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalConfig` |  |

### GlobalConfig_timeoutSeconds_set
`static final native void core_modelerJNI.GlobalConfig_timeoutSeconds_set(long jarg1, GlobalConfig jarg1_, double jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalConfig` |  |
| jarg2 | `double` |  |

### GlobalConfig_timeoutSeconds_get
`static final native double core_modelerJNI.GlobalConfig_timeoutSeconds_get(long jarg1, GlobalConfig jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalConfig` |  |

### new_GlobalConfig
`static final native long core_modelerJNI.new_GlobalConfig()`

### delete_GlobalConfig
`static final native void core_modelerJNI.delete_GlobalConfig(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### g_systemState_set
`static final native void core_modelerJNI.g_systemState_set(int jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `int` |  |

### g_systemState_get
`static final native int core_modelerJNI.g_systemState_get()`

### g_piValue_set
`static final native void core_modelerJNI.g_piValue_set(double jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `double` |  |

### g_piValue_get
`static final native double core_modelerJNI.g_piValue_get()`

### GlobalLoggerProxy_logMessage__SWIG_0
`static final native void core_modelerJNI.GlobalLoggerProxy_logMessage__SWIG_0(long jarg1, GlobalLoggerProxy jarg1_, String jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalLoggerProxy` |  |
| jarg2 | `String` |  |

### GlobalLoggerProxy_logMessage__SWIG_1
`static final native boolean core_modelerJNI.GlobalLoggerProxy_logMessage__SWIG_1(long jarg1, GlobalLoggerProxy jarg1_, String jarg2, int jarg3)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalLoggerProxy` |  |
| jarg2 | `String` |  |
| jarg3 | `int` |  |

### GlobalLoggerProxy_forceFlush
`static final native void core_modelerJNI.GlobalLoggerProxy_forceFlush(long jarg1, GlobalLoggerProxy jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalLoggerProxy` |  |

### new_GlobalLoggerProxy
`static final native long core_modelerJNI.new_GlobalLoggerProxy()`

### delete_GlobalLoggerProxy
`static final native void core_modelerJNI.delete_GlobalLoggerProxy(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### globalInitialize
`static final native int core_modelerJNI.globalInitialize(long jarg1, GlobalConfig jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `GlobalConfig` |  |

### new_CoreModeler_Model
`static final native long core_modelerJNI.new_CoreModeler_Model(int jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `int` |  |

### CoreModeler_Model_MetadataIterator_hasNext
`static final native boolean core_modelerJNI.CoreModeler_Model_MetadataIterator_hasNext(long jarg1, CoreModeler.Model.MetadataIterator jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Model.MetadataIterator` |  |

### CoreModeler_Model_MetadataIterator_next
`static final native String core_modelerJNI.CoreModeler_Model_MetadataIterator_next(long jarg1, CoreModeler.Model.MetadataIterator jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Model.MetadataIterator` |  |

### new_CoreModeler_Model_MetadataIterator
`static final native long core_modelerJNI.new_CoreModeler_Model_MetadataIterator()`

### delete_CoreModeler_Model_MetadataIterator
`static final native void core_modelerJNI.delete_CoreModeler_Model_MetadataIterator(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### delete_CoreModeler_Model
`static final native void core_modelerJNI.delete_CoreModeler_Model(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### delete_CoreModeler_Geometry_IDrawable
`static final native void core_modelerJNI.delete_CoreModeler_Geometry_IDrawable(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### CoreModeler_Geometry_IDrawable_renderToScreen__SWIG_0
`static final native void core_modelerJNI.CoreModeler_Geometry_IDrawable_renderToScreen__SWIG_0(long jarg1, CoreModeler.Geometry.IDrawable jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.IDrawable` |  |

### CoreModeler_Geometry_IDrawable_renderToScreen__SWIG_1
`static final native int core_modelerJNI.CoreModeler_Geometry_IDrawable_renderToScreen__SWIG_1(long jarg1, CoreModeler.Geometry.IDrawable jarg1_, int jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.IDrawable` |  |
| jarg2 | `int` |  |

### delete_CoreModeler_Geometry_Shape
`static final native void core_modelerJNI.delete_CoreModeler_Geometry_Shape(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### CoreModeler_Geometry_Shape_getVolume
`static final native double core_modelerJNI.CoreModeler_Geometry_Shape_getVolume(long jarg1, CoreModeler.Geometry.Shape jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Shape` |  |

### new_CoreModeler_Geometry_Box
`static final native long core_modelerJNI.new_CoreModeler_Geometry_Box(double jarg1, double jarg2, double jarg3)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `double` |  |
| jarg2 | `double` |  |
| jarg3 | `double` |  |

### CoreModeler_Geometry_Box_getVolume
`static final native double core_modelerJNI.CoreModeler_Geometry_Box_getVolume(long jarg1, CoreModeler.Geometry.Box jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Box` |  |

### CoreModeler_Geometry_Box_renderToScreen__SWIG_0
`static final native void core_modelerJNI.CoreModeler_Geometry_Box_renderToScreen__SWIG_0(long jarg1, CoreModeler.Geometry.Box jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Box` |  |

### CoreModeler_Geometry_Box_renderToScreen__SWIG_1
`static final native int core_modelerJNI.CoreModeler_Geometry_Box_renderToScreen__SWIG_1(long jarg1, CoreModeler.Geometry.Box jarg1_, int jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Box` |  |
| jarg2 | `int` |  |

### CoreModeler_Geometry_Box_scale__SWIG_0
`static final native void core_modelerJNI.CoreModeler_Geometry_Box_scale__SWIG_0(long jarg1, CoreModeler.Geometry.Box jarg1_, double jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Box` |  |
| jarg2 | `double` |  |

### CoreModeler_Geometry_Box_scale__SWIG_1
`static final native void core_modelerJNI.CoreModeler_Geometry_Box_scale__SWIG_1(long jarg1, CoreModeler.Geometry.Box jarg1_, double jarg2, double jarg3, double jarg4)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Box` |  |
| jarg2 | `double` |  |
| jarg3 | `double` |  |
| jarg4 | `double` |  |

### delete_CoreModeler_Geometry_Box
`static final native void core_modelerJNI.delete_CoreModeler_Geometry_Box(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### DIAG_SUCCESS_get
`static final native long core_modelerJNI.DIAG_SUCCESS_get()`

### DIAG_FAILURE_get
`static final native long core_modelerJNI.DIAG_FAILURE_get()`

### g_diagnosticRunCount_set
`static final native void core_modelerJNI.g_diagnosticRunCount_set(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### g_diagnosticRunCount_get
`static final native long core_modelerJNI.g_diagnosticRunCount_get()`

### checkSystemHealth
`static final native long core_modelerJNI.checkSystemHealth()`

### pingSubsystem__SWIG_0
`static final native boolean core_modelerJNI.pingSubsystem__SWIG_0(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### pingSubsystem__SWIG_1
`static final native boolean core_modelerJNI.pingSubsystem__SWIG_1()`

### resetCounters
`static final native void core_modelerJNI.resetCounters()`

### CoreModeler_Geometry_Point3Di_x_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Di_x_set(long jarg1, CoreModeler.Geometry.Point3Di jarg1_, int jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Di` |  |
| jarg2 | `int` |  |

### CoreModeler_Geometry_Point3Di_x_get
`static final native int core_modelerJNI.CoreModeler_Geometry_Point3Di_x_get(long jarg1, CoreModeler.Geometry.Point3Di jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Di` |  |

### CoreModeler_Geometry_Point3Di_y_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Di_y_set(long jarg1, CoreModeler.Geometry.Point3Di jarg1_, int jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Di` |  |
| jarg2 | `int` |  |

### CoreModeler_Geometry_Point3Di_y_get
`static final native int core_modelerJNI.CoreModeler_Geometry_Point3Di_y_get(long jarg1, CoreModeler.Geometry.Point3Di jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Di` |  |

### CoreModeler_Geometry_Point3Di_z_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Di_z_set(long jarg1, CoreModeler.Geometry.Point3Di jarg1_, int jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Di` |  |
| jarg2 | `int` |  |

### CoreModeler_Geometry_Point3Di_z_get
`static final native int core_modelerJNI.CoreModeler_Geometry_Point3Di_z_get(long jarg1, CoreModeler.Geometry.Point3Di jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Di` |  |

### new_CoreModeler_Geometry_Point3Di__SWIG_0
`static final native long core_modelerJNI.new_CoreModeler_Geometry_Point3Di__SWIG_0()`

### new_CoreModeler_Geometry_Point3Di__SWIG_1
`static final native long core_modelerJNI.new_CoreModeler_Geometry_Point3Di__SWIG_1(int jarg1, int jarg2, int jarg3)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `int` |  |
| jarg2 | `int` |  |
| jarg3 | `int` |  |

### CoreModeler_Geometry_Point3Di_translate
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Di_translate(long jarg1, CoreModeler.Geometry.Point3Di jarg1_, int jarg2, int jarg3, int jarg4)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Di` |  |
| jarg2 | `int` |  |
| jarg3 | `int` |  |
| jarg4 | `int` |  |

### delete_CoreModeler_Geometry_Point3Di
`static final native void core_modelerJNI.delete_CoreModeler_Geometry_Point3Di(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### CoreModeler_Geometry_Point3Df_x_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Df_x_set(long jarg1, CoreModeler.Geometry.Point3Df jarg1_, float jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Df` |  |
| jarg2 | `float` |  |

### CoreModeler_Geometry_Point3Df_x_get
`static final native float core_modelerJNI.CoreModeler_Geometry_Point3Df_x_get(long jarg1, CoreModeler.Geometry.Point3Df jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Df` |  |

### CoreModeler_Geometry_Point3Df_y_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Df_y_set(long jarg1, CoreModeler.Geometry.Point3Df jarg1_, float jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Df` |  |
| jarg2 | `float` |  |

### CoreModeler_Geometry_Point3Df_y_get
`static final native float core_modelerJNI.CoreModeler_Geometry_Point3Df_y_get(long jarg1, CoreModeler.Geometry.Point3Df jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Df` |  |

### CoreModeler_Geometry_Point3Df_z_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Df_z_set(long jarg1, CoreModeler.Geometry.Point3Df jarg1_, float jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Df` |  |
| jarg2 | `float` |  |

### CoreModeler_Geometry_Point3Df_z_get
`static final native float core_modelerJNI.CoreModeler_Geometry_Point3Df_z_get(long jarg1, CoreModeler.Geometry.Point3Df jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Df` |  |

### new_CoreModeler_Geometry_Point3Df__SWIG_0
`static final native long core_modelerJNI.new_CoreModeler_Geometry_Point3Df__SWIG_0()`

### new_CoreModeler_Geometry_Point3Df__SWIG_1
`static final native long core_modelerJNI.new_CoreModeler_Geometry_Point3Df__SWIG_1(float jarg1, float jarg2, float jarg3)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `float` |  |
| jarg2 | `float` |  |
| jarg3 | `float` |  |

### CoreModeler_Geometry_Point3Df_translate
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Df_translate(long jarg1, CoreModeler.Geometry.Point3Df jarg1_, float jarg2, float jarg3, float jarg4)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Df` |  |
| jarg2 | `float` |  |
| jarg3 | `float` |  |
| jarg4 | `float` |  |

### delete_CoreModeler_Geometry_Point3Df
`static final native void core_modelerJNI.delete_CoreModeler_Geometry_Point3Df(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### CoreModeler_Geometry_Point3Dd_x_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Dd_x_set(long jarg1, CoreModeler.Geometry.Point3Dd jarg1_, double jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Dd` |  |
| jarg2 | `double` |  |

### CoreModeler_Geometry_Point3Dd_x_get
`static final native double core_modelerJNI.CoreModeler_Geometry_Point3Dd_x_get(long jarg1, CoreModeler.Geometry.Point3Dd jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Dd` |  |

### CoreModeler_Geometry_Point3Dd_y_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Dd_y_set(long jarg1, CoreModeler.Geometry.Point3Dd jarg1_, double jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Dd` |  |
| jarg2 | `double` |  |

### CoreModeler_Geometry_Point3Dd_y_get
`static final native double core_modelerJNI.CoreModeler_Geometry_Point3Dd_y_get(long jarg1, CoreModeler.Geometry.Point3Dd jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Dd` |  |

### CoreModeler_Geometry_Point3Dd_z_set
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Dd_z_set(long jarg1, CoreModeler.Geometry.Point3Dd jarg1_, double jarg2)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Dd` |  |
| jarg2 | `double` |  |

### CoreModeler_Geometry_Point3Dd_z_get
`static final native double core_modelerJNI.CoreModeler_Geometry_Point3Dd_z_get(long jarg1, CoreModeler.Geometry.Point3Dd jarg1_)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Dd` |  |

### new_CoreModeler_Geometry_Point3Dd__SWIG_0
`static final native long core_modelerJNI.new_CoreModeler_Geometry_Point3Dd__SWIG_0()`

### new_CoreModeler_Geometry_Point3Dd__SWIG_1
`static final native long core_modelerJNI.new_CoreModeler_Geometry_Point3Dd__SWIG_1(double jarg1, double jarg2, double jarg3)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `double` |  |
| jarg2 | `double` |  |
| jarg3 | `double` |  |

### CoreModeler_Geometry_Point3Dd_translate
`static final native void core_modelerJNI.CoreModeler_Geometry_Point3Dd_translate(long jarg1, CoreModeler.Geometry.Point3Dd jarg1_, double jarg2, double jarg3, double jarg4)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |
| jarg1_ | `CoreModeler.Geometry.Point3Dd` |  |
| jarg2 | `double` |  |
| jarg3 | `double` |  |
| jarg4 | `double` |  |

### delete_CoreModeler_Geometry_Point3Dd
`static final native void core_modelerJNI.delete_CoreModeler_Geometry_Point3Dd(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

### CoreModeler_Geometry_Box_SWIGUpcast
`static final native long core_modelerJNI.CoreModeler_Geometry_Box_SWIGUpcast(long jarg1)`

| Parameter | Type | Description |
| --- | --- | --- |
| jarg1 | `long` |  |

