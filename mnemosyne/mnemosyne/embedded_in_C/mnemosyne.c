// mnemosyne.c <Peter.Bienstman@UGent.be>

#include <string.h>
#include <Python.h>

#define BUFFER_SIZE 4096

char buffer[BUFFER_SIZE];

PyObject* log_CaptureStdout(PyObject* self, PyObject* pArgs)
{ 
 printf("stdout"); 
 char* LogStr = NULL;
 if (!PyArg_ParseTuple(pArgs, "s", &LogStr)) return NULL;

 printf("%s", LogStr); 

 strncpy(buffer, LogStr, BUFFER_SIZE);
 printf("bufferin:%s\n", buffer);

 Py_INCREF(Py_None);
 return Py_None;
}

// Notice we have STDERR too.
PyObject* log_CaptureStderr(PyObject* self, PyObject* pArgs)
{
 char* LogStr = NULL;
 if (!PyArg_ParseTuple(pArgs, "s", &LogStr)) return NULL;

 printf("%s", LogStr);
 strncpy(buffer, LogStr, BUFFER_SIZE);

 Py_INCREF(Py_None);
 return Py_None;
}

static PyMethodDef logMethods[] = {
 {"CaptureStdout", log_CaptureStdout, METH_VARARGS, "Logs stdout"},
 {"CaptureStderr", log_CaptureStderr, METH_VARARGS, "Logs stderr"},
 {NULL, NULL, 0, NULL}
};


int main(int argc, char *argv[])
{

  Py_Initialize();
  Py_InitModule("log", logMethods);

 PyRun_SimpleString(
"import log\n"
"import sys\n"
"class StdoutCatcher:\n"
"\tdef write(self, str):\n"
"\t\tlog.CaptureStdout(str)\n"
"class StderrCatcher:\n"
"\tdef write(self, str):\n"
"\t\tlog.CaptureStderr(str)\n"
"sys.stdout = StdoutCatcher()\n"
"sys.stderr = StderrCatcher()\n"
);

  PyRun_SimpleString(
    "import sys\n"
    "sys.path.insert(0, \"/home/pbienst/source/mnemosyne-proj-pbienst/mnemosyne\")\n"
    "from mnemosyne.libmnemosyne import Mnemosyne\n"
    "mnemosyne = Mnemosyne()\n"
    "mnemosyne.components.insert(0, (\"mnemosyne.libmnemosyne.translator\", \"GetTextTranslator\"))\n"
    "mnemosyne.components.append((\"mnemosyne.embedded_in_C.C_main_widget\", \"C_MainWidget\"))\n"
    "mnemosyne.components.append((\"mnemosyne.embedded_in_C.C_review_widget\", \"C_ReviewWidget\"))\n"
    "mnemosyne.initialise(data_dir=\"/home/pbienst/source/mnemosyne-proj-pbienst/mnemosyne/dot_mnemosyne2\", filename=\"default.db\")\n"
    "mnemosyne.config()[\"upload_science_logs\"] = False"
);

  // Illustration on how to get data from Python to C.
  buffer[0] = 0;
  PyRun_SimpleString(
    "print mnemosyne.database().card_count()");
  int card_count = atoi(buffer);  
  printf("buffer:%s\n", buffer);
  printf("count+1:%d\n", card_count+1);

  PyObject* obj = PyRun_String("1", Py_single_input, PyEval_GetGlobals(), PyEval_GetLocals());
  long d = PyLong_AsLong(obj);
  printf("long:%ld\n", d);  
  Py_DECREF(obj);



  PyObject* pyIntObject = PyInt_FromLong(5);
  if (pyIntObject == NULL) ; // Error

  PyObject* module = PyImport_ImportModule("__builtin__");
  PyObject* obj = PyRun_String("unicode(1).encode(\"utf-8\")", Py_eval_input, PyModule_GetDict(module), NULL);
  Py_DECREF(module);
  char* s = PyString_AsString(obj);
  //PyErr_Print();
  printf("string: %s\n", s);  
  Py_DECREF(obj);

  Py_Finalize();
  return 0;
}
