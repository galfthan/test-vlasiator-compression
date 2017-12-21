#include <Python.h>
#include "numpy/arrayobject.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "zfp.h"
#include "zfpmodule.h"





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
  PyArrayObject *arrayout;
  double *original, *original_transform, *final;
  int nx, ny, nz;

  double rate;
  int decompress;
  int status = 0;    /* return value: 0 = success */
  zfp_type type;     /* array scalar type */
  zfp_field* field;  /* array meta data */
  zfp_field* fieldout;  /* array meta data */
  zfp_stream* zfp;   /* compressed stream */
  void* buffer;      /* storage for compressed stream */
  size_t bufsize;    /* byte size of compressed buffer */
  bitstream* stream; /* bit stream to write to or read from */
  size_t zfpsize;    /* byte size of compressed stream */
  int i;
  double max;
  
  if (!PyArg_ParseTuple(args, "O!O!d",  &PyArray_Type, &arrayin,  &PyArray_Type, &arrayout, &rate))
    return NULL;
  
  if (arrayin->nd != 1 || arrayin->descr->type_num != PyArray_DOUBLE) {
    PyErr_SetString(PyExc_ValueError, "arrayin must be one-dimensional and of type double");
    return NULL;
  }
  if (arrayout->nd != 1 || arrayout->descr->type_num != PyArray_DOUBLE) {
    PyErr_SetString(PyExc_ValueError, "arrayout must be one-dimensional and of type double");
    return NULL;
  }


  
  nx = 4;
  ny = 4;
  nz = 4;

  if( nx * ny * nz != arrayin->dimensions[0] || nx * ny * nz != arrayout->dimensions[0] ){
    PyErr_SetString(PyExc_ValueError, "Arrayout or arrayin has wrong number of elements (nx * ny * nz)");
    return NULL;
  }  
  
  original = (double*)arrayin->data;
  original_transform = (double *) malloc(sizeof(double) * nx * ny * nz);
    
  max = original[0];
  for (i = 1 ;i < nx * ny * nz; i++) {
    max = max < original[i] ? original[i]: max;

  }
  
  for (i = 0; i < nx * ny * nz; i++) {
    original_transform[i] = log(original[i] <= 0.0 ? 1e-200 : original[i]);
  }
  
  final = (double*)arrayout->data;
  
  
  /* allocate meta data for the 3D array a[nz][ny][nx] */
  type = zfp_type_double;
  field = zfp_field_3d(original_transform, type, nx, ny, nz);
  fieldout = zfp_field_3d(final, type, nx, ny, nz);
  
  /* allocate meta data for a compressed stream */
  zfp = zfp_stream_open(NULL);

  /* set compression mode and parameters via one of three functions */
  zfp_stream_set_rate(zfp, rate, type, 3, 0);
  
/*  zfp_stream_set_precision(zfp, precision); */
/*  zfp_stream_set_accuracy(zfp, tolerance);*/

  /* allocate buffer for compressed data */
  bufsize = zfp_stream_maximum_size(zfp, field);
  //  printf("bufsize %d\n", bufsize);
  
  buffer = malloc(bufsize);
  /* associate bit stream with allocated buffer */
  stream = stream_open(buffer, bufsize);
  zfp_stream_set_bit_stream(zfp, stream);
  zfp_stream_rewind(zfp);

  zfpsize = zfp_compress(zfp, field);
  if (!zfpsize) {
    status = 1;
  }

  
  zfp_stream_rewind(zfp);
  zfp_decompress(zfp, fieldout);

  for (i = 0 ;i < nx * ny * nz; i++) {
    final[i] = exp(final[i]);
  }
  //  for (i = 0; i < nx * ny * nz; i++) {
    //    printf("%g %g %g %g\n", original[i], final[i], original[i] - final[i], fabs(original[i] - final[i])/original[i] );
  // }
  /* clean up */
  zfp_field_free(field);
  zfp_field_free(fieldout);
  zfp_stream_close(zfp);
  stream_close(stream);
  free(buffer);
  free(original_transform);

  return PyFloat_FromDouble(0);


}
