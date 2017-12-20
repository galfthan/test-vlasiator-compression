#include <Python.h>
#include "numpy/arrayobject.h"

#include "zfpmodule.h"
//#include "zfp.h"

//http://scipy-cookbook.readthedocs.io/items/C_Extensions_NumPy_arrays.html

/* ==== Set up the methods table ====================== */
static PyMethodDef zfpmodule_methods[] = {
    {"compress_block", compress_block, METH_VARARGS},
    {NULL, NULL}     /* Sentinel - marks the end of this structure */
};

/* ==== Initialize the C_test functions ====================== */
PyMODINIT_FUNC initzfpmodule(void)  {
    (void) Py_InitModule("zfpmodule", zfpmodule_methods);
    import_array();  // Must be present for NumPy.  Called first after above line.
}

static PyObject * compress_block(PyObject *self, PyObject *args){
  PyArrayObject *arrayin;
  //  PyArrayObject *arrayout;
  double *array;
  int i, n;

  if (!PyArg_ParseTuple(args, "O!",  &PyArray_Type, &arrayin))
    return NULL;
  
  if (arrayin->nd != 1 || arrayin->descr->type_num != PyArray_DOUBLE) {
    PyErr_SetString(PyExc_ValueError, "arrayin must be one-dimensional and of type double");
    return NULL;
  }

  n = arrayin->dimensions[0];
  printf("n is %d\n", n);

  array = (double*)arrayin->data;
  for (i = 0; i < n; i++)
    printf("%d: %g\n", i, array[i]);
  
  return 0;

}
