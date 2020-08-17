#define PY_SSIZE_T_CLEAN

#include "disasm.h"

#include <inttypes.h>
#include "capstone/capstone.h"

#define ERROR "Failed to disassemble given code!"


PyObject* DisassembleException = NULL;


PyObject *
disasmARM(PyObject* self, PyObject* a_args)
{
	const char* args;
	Py_ssize_t args_size;

	char* buffer = "";
	char* tmp_buffer;

	csh handle;
	cs_insn *insn;
	size_t count;
	size_t j;

	if(!PyArg_ParseTuple(a_args, "s#", &args, &args_size))
		return NULL;

	if (cs_open(CS_ARCH_ARM, CS_MODE_ARM, &handle) != CS_ERR_OK)
		DISASSEMBLE_EXCEPTION(-1, "init failed");

	count = cs_disasm(handle, args, args_size, 0x1000, 0, &insn);

	if (count > 0)
	{
		for (j = 0; j < count; j++)
		{
			sprintf(tmp_buffer, "0x%"PRIx64":\t%s\t\t%s\n", insn[j].address, insn[j].mnemonic,insn[j].op_str);
			strcat(buffer, tmp_buffer);
		}

		cs_free(insn, count);
	}
	else
	{
		return Py_BuildValue("s", ERROR);
	}

	cs_close(&handle);

    return Py_BuildValue("s", buffer);
}


PyObject *
disasmX86(PyObject* self, PyObject* a_args)
{
	const char* args;
	Py_ssize_t args_size;


	char* buffer = "";
	char* tmp_buffer;

	csh handle;
	cs_insn *insn;
	size_t count;
	size_t j;


	if(!PyArg_ParseTuple(a_args, "s#", &args, &args_size))
		return NULL;

	if (cs_open(CS_ARCH_X86, CS_MODE_32, &handle) != CS_ERR_OK)
		DISASSEMBLE_EXCEPTION(-1, "init failed");


	count = cs_disasm(handle, args, args_size, 0x1000, 0, &insn);

	if (count > 0)
	{
		for (j = 0; j < count; j++)
		{
			sprintf(tmp_buffer, "0x%"PRIx64":\t%s\t\t%s\n", insn[j].address, insn[j].mnemonic,insn[j].op_str);
			strcat(buffer, tmp_buffer);
		}

		cs_free(insn, count);
	}
	else
	{
		return Py_BuildValue("s", ERROR);
	}

	cs_close(&handle);

    return Py_BuildValue("s", buffer);
}


PyMethodDef DisassembleMethods[] = {
	{"disasmX86", disasmX86, METH_VARARGS, "OPcode disassemble"},
	{"disasmARM", disasmARM, METH_VARARGS, "OPcode disassemble"},
	{NULL, NULL, 0, NULL}
};


struct PyModuleDef disassemblemodule = {
	PyModuleDef_HEAD_INIT,
	"disassemble",
	NULL,
	-1,
	DisassembleMethods
};


PyMODINIT_FUNC
PyInit_disassemble(void)
{
	PyObject* m = NULL;


	if(NULL == (m = PyModule_Create(&disassemblemodule)))
	{
		DEPRINT("Disassemble Module Exception");
		return NULL;
	}

	if (NULL == (DisassembleException = PyErr_NewException("disassemble.Exception",
													PyExc_Exception,
													NULL)))
	{
		DEPRINT("NewException");
		return NULL;
	}

	Py_INCREF(DisassembleException);

	if (PyModule_AddObject(m, "DisassembleException", DisassembleException) < 0)
	{
		Py_DECREF(DisassembleException);
		Py_CLEAR(DisassembleException);
		Py_DECREF(m);

		return NULL;
	}

	return m;
}
