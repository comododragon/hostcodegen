#!/usr/bin/env python3

# #############################################################################################
# # Code Emitter of C Template for Kernel Execution                                           #
# # Author: André Bannwart Perina                                                             #
# #############################################################################################
# # Copyright (c) 2017 André B. Perina                                                        #
# #                                                                                           #
# # Permission is hereby granted, free of charge, to any person obtaining a copy of this      #
# # software and associated documentation files (the "Software"), to deal in the Software     #
# # without restriction, including without limitation the rights to use, copy, modify,        #
# # merge, publish, distribute, sublicense, and/or sell copies of the Software, and to        #
# # permit persons to whom the Software is furnished to do so, subject to the following       #
# # conditions:                                                                               #
# #                                                                                           #
# # The above copyright notice and this permission notice shall be included in all copies     #
# # or substantial portions of the Software.                                                  #
# #                                                                                           #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,       #
# # INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR  #
# # PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE #
# # FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR      #
# # OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER    #
# # DEALINGS IN THE SOFTWARE.                                                                 #
# #############################################################################################


import math
from xml.etree import ElementTree


class CodeEmitter:
	_targetFile = ""
	_xmlRoot = ()
	# Type of arguments used in the PRE/POSTAMBLE functions
	_varTypeList = []
	# Name of arguments used in the PRE/POSTAMBLE functions
	_varNameList = []
	# Mappers between C types and their printf format flags
	_printfMapper = {
		"char": "c",
		"signed char": "c",
		"unsigned char": "c",
		"short": "hd",
		"short int": "hd",
		"signed short": "hd",
		"signed short int": "hd",
		"unsigned short": "hu",
		"unsigned short int": "hu",
		"int": "d",
		"signed": "d",
		"signed int": "d",
		"unsigned": "u",
		"unsigned int": "u",
		"long": "ld",
		"long int": "ld",
		"signed long": "ld",
		"signed long int": "ld",
		"unsigned long": "lu",
		"unsigned long int": "lu",
		"long long": "lld",
		"long long int": "lld",
		"signed long long": "lld",
		"signed long long int": "lld",
		"unsigned long long": "llu",
		"unsigned long long int": "llu",
		"float": "f",
		"double": "lf",
		"long double": "Lf"
	}
	# Array of vector types
	_vectorTypes = {
		"cl_char2": (2, "char"),
		"cl_uchar2": (2, "unsigned char"),
		"cl_short2": (2, "short"),
		"cl_ushort2": (2, "unsigned short"),
		"cl_int2": (2, "int"),
		"cl_uint2": (2, "unsigned int"),
		"cl_long2": (2, "long"),
		"cl_ulong2": (2, "unsigned long"),
		"cl_half2": (2, "float"),
		"cl_float2": (2, "float"),
		"cl_double2": (2, "double"),
		"cl_char3": (3, "char"),
		"cl_uchar3": (3, "unsigned char"),
		"cl_short3": (3, "short"),
		"cl_ushort3": (3, "unsigned short"),
		"cl_int3": (3, "int"),
		"cl_uint3": (3, "unsigned int"),
		"cl_long3": (3, "long"),
		"cl_ulong3": (3, "unsigned long"),
		"cl_half3": (3, "float"),
		"cl_float3": (3, "float"),
		"cl_double3": (3, "double"),
		"cl_char4": (4, "char"),
		"cl_uchar4": (4, "unsigned char"),
		"cl_short4": (4, "short"),
		"cl_ushort4": (4, "unsigned short"),
		"cl_int4": (4, "int"),
		"cl_uint4": (4, "unsigned int"),
		"cl_long4": (4, "long"),
		"cl_ulong4": (4, "unsigned long"),
		"cl_half4": (4, "float"),
		"cl_float4": (4, "float"),
		"cl_double4": (4, "double"),
		"cl_char8": (8, "char"),
		"cl_uchar8": (8, "unsigned char"),
		"cl_short8": (8, "short"),
		"cl_ushort8": (8, "unsigned short"),
		"cl_int8": (8, "int"),
		"cl_uint8": (8, "unsigned int"),
		"cl_long8": (8, "long"),
		"cl_ulong8": (8, "unsigned long"),
		"cl_half8": (8, "float"),
		"cl_float8": (8, "float"),
		"cl_double8": (8, "double"),
		"cl_char16": (16, "char"),
		"cl_uchar16": (16, "unsigned char"),
		"cl_short16": (16, "short"),
		"cl_ushort16": (16, "unsigned short"),
		"cl_int16": (16, "int"),
		"cl_uint16": (16, "unsigned int"),
		"cl_long16": (16, "long"),
		"cl_ulong16": (16, "unsigned long"),
		"cl_half16": (16, "float"),
		"cl_float16": (16, "float"),
		"cl_double16": (16, "double")
	}


	def __init__(self, xmlFile, targetFile):
		self._xmlRoot = ElementTree.parse(xmlFile).getroot()

		# Clean file
		self._targetFile = targetFile
		with open(self._targetFile, "w") as f:
			pass


	# Print header: includes, macros and first declarations of main()
	def printHeader(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'/* ********************************************************************************************* */\n'
					'/* * C Template for Kernel Execution                                                           * */\n'
					'/* * Author: André Bannwart Perina                                                             * */\n'
					'/* ********************************************************************************************* */\n'
					'/* * Copyright (c) 2017 André B. Perina                                                        * */\n'
					'/* *                                                                                           * */\n'
					'/* * Permission is hereby granted, free of charge, to any person obtaining a copy of this      * */\n'
					'/* * software and associated documentation files (the "Software"), to deal in the Software     * */\n'
					'/* * without restriction, including without limitation the rights to use, copy, modify,        * */\n'
					'/* * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to        * */\n'
					'/* * permit persons to whom the Software is furnished to do so, subject to the following       * */\n'
					'/* * conditions:                                                                               * */\n'
					'/* *                                                                                           * */\n'
					'/* * The above copyright notice and this permission notice shall be included in all copies     * */\n'
					'/* * or substantial portions of the Software.                                                  * */\n'
					'/* *                                                                                           * */\n'
					'/* * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,       * */\n'
					'/* * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR  * */\n'
					'/* * PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE * */\n'
					'/* * FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR      * */\n'
					'/* * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER    * */\n'
					'/* * DEALINGS IN THE SOFTWARE.                                                                 * */\n'
					'/* ********************************************************************************************* */\n'
					'\n'
					'#include <CL/opencl.h>\n'
					'#include <errno.h>\n'
					'#include <stdbool.h>\n'
					'#include <stdio.h>\n'
					'#include <string.h>\n'
					'#include <sys/time.h>\n'
					'\n'
					'#include "common.h"\n'
					'\n'
				)
			)

			# Populate lists of arguments for PRE/POSTAMBLE functions
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						if ("input" == v.tag) or ("output" == v.tag):
							self._varTypeList.append("{}{}".format(v.attrib["type"], " *" if int(v.attrib["nmemb"]) > 1 else ""))
							self._varNameList.append(v.attrib["name"])
							self._varTypeList.append("unsigned int")
							self._varNameList.append(v.attrib["nmemb"])
	
						if ("output" == v.tag) and (("novalidation" not in v.attrib) or (v.attrib["novalidation"] != "true")):
							self._varTypeList.append("{}{}".format(v.attrib["type"], " *" if int(v.attrib["nmemb"]) > 1 else ""))
							self._varNameList.append("{}C".format(v.attrib["name"]))
							self._varTypeList.append("unsigned int")
							self._varNameList.append(v.attrib["nmemb"])

			# If any PRE/POSTAMBLE function was enabled, include the respective header
			if any(x in ["preamble", "postamble", "looppreamble", "looppostamble", "cleanup"] for x in self._xmlRoot.attrib):
				f.write(
					(
						'/**\n'
						' * @brief Header where pre/postamble macro functions should be located.\n'
						' *        Function headers:\n'
					)
				)

				functions = ("PREAMBLE", "POSTAMBLE", "LOOPPREAMBLE", "LOOPPOSTAMBLE", "CLEANUP")
				usesLoopVar = (False, False, True, True, False)
				for i in range(0, len(functions)):
					f.write(
						' *            {}('.format(functions[i])
					)

					firstExec = True
					for v, n in zip(self._varNameList[::2], self._varNameList[1::2]):
						if not firstExec:
							f.write(', ')
						else:
							firstExec = False

						f.write(
							'{}'.format(v)
						)

						if int(n) > 1:
							f.write(
								', {}Sz'.format(v)
							)

					if usesLoopVar[i]:
						f.write(', loopFlag);\n')
					else:
						f.write(');\n')

				f.write(
						' *        where:\n'
				)

				for i in range(0, len(self._varNameList), 2):
					f.write(
						' *            {0}: variable ({1});\n'.format(self._varNameList[i], self._varTypeList[i])
					)

					if int(self._varNameList[i + 1]) > 1:
						f.write(
							' *            {}Sz: number of members in variable (unsigned int);\n'.format(self._varNameList[i])
						)

				f.write(
					(
						' *            loopFlag: loop condition variable (bool).\n'
						' */\n'
						'#include "prepostambles.h"\n'
						'\n'
					)
				)

			f.write(
				(
					'/**\n'
					' * @brief Test if two operands are outside an epsilon range.\n'
					' *\n'
					' * @param a First operand.\n'
					' * @param b Second operand.\n'
					' * @param e Epsilon value.\n'
					' */\n'
					'#define TEST_EPSILON(a, b, e) (((a > b) && (a - b > e)) || ((b >= a) && (b - a > e)))\n'
					'\n'
					'/**\n'
					' * @brief Standard statements for function error handling and printing.\n'
					' *\n'
					' * @param funcName Function name that failed.\n'
					' */\n'
					'#define FUNCTION_ERROR_STATEMENTS(funcName) {\\\n'
					'	rv = EXIT_FAILURE;\\\n'
					'	PRINT_FAIL();\\\n'
					'	fprintf(stderr, "Error: %s failed with return code %d.\\n", funcName, fRet);\\\n'
					'}\n'
					'\n'
					'/**\n'
					' * @brief Standard statements for POSIX error handling and printing.\n'
					' *\n'
					' * @param arg Arbitrary string to the printed at the end of error string.\n'
					' */\n'
					'#define POSIX_ERROR_STATEMENTS(arg) {\\\n'
					'	rv = EXIT_FAILURE;\\\n'
					'	PRINT_FAIL();\\\n'
					'	fprintf(stderr, "Error: %s: %s\\n", strerror(errno), arg);\\\n'
					'}\n'
					'\n'
					'int main(void) {\n'
					'	/* Return variable */\n'
					'	int rv = EXIT_SUCCESS;\n'
					'\n'
					'	/* OpenCL and aux variables */\n'
					'	int i = 0, j = 0;\n'
					'	cl_int platformsLen, devicesLen, fRet;\n'
					'	cl_platform_id *platforms = NULL;\n'
					'	cl_device_id *devices = NULL;\n'
					'	cl_context context = NULL;\n'
				)
			)


	# Print queue declarations for each kernel
	def printQueueDeclarations(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					f.write(
						'	cl_command_queue queue{} = NULL;\n'.format(k.attrib["name"].title())
					)


	# Print variable declarations related to the program
	def printProgramDeclarations(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	FILE *programFile = NULL;\n'
					'	long programSz;\n'
					'	char *programContent = NULL;\n'
					'	cl_int programRet;\n'
					'	cl_program program = NULL;\n'
				)
			)


	# Print kernel declarations
	def printKernelDeclarations(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					f.write(
						'	cl_kernel kernel{} = NULL;\n'.format(k.attrib["name"].title())
					)


	# Print last declarations: some flags and other stuff
	def printLastDeclarations(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	bool loopFlag = false;\n'
					'	bool invalidDataFound = false;\n'
				)
			)

			# If profiling is on, add timer variables
			if "profile" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["profile"]:
				f.write(
					(
						'	struct timeval then, now;\n'
						'	long execTime = 0;\n'
					)
				)

			# Iterate through every kernel
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						# Search for ndrange tag
						if "ndrange" == v.tag:
							# If no dim attribute is present, default it to 1
							dim = v.attrib["dim"] if "dim" in v.attrib else "1"
							f.write(
								'	cl_uint workDim{} = {};\n'.format(k.attrib["name"].title(), dim)
							)
	
							# Set global and local (if any) dimensions
							for d in v:
								if "global" == d.tag:
									f.write(
										(
											'	size_t globalSize{}[{}] = {{\n'
											'		{}\n'
											'	}};\n'.format(
												k.attrib["name"].title(),
												dim,
												d.text
											)
										)
									)
								elif "local" == d.tag:
									f.write(
										(
											'	size_t localSize{}[{}] = {{\n'
											'		{}\n'
											'	}};\n'.format(
												k.attrib["name"].title(),
												dim,
												d.text
											)
										)
									)


	# Print a simple newline
	def printSeparator(self):
		with open(self._targetFile, "a") as f:
			f.write('\n')


	# Print declaration of inputs and outputs of kernels
	def printVariablesDeclaration(self):
		with open(self._targetFile, "a") as f:
			f.write(
				'	/* Input/output variables */\n'
			)

			# Iterate through every variable of every kernel
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						if "input" == v.tag:
							# Part 1: host variable
							# Function is being used instead of explicit variable initialisation
							if v.text is None:
								if int(v.attrib["nmemb"]) > 1:
									f.write(
										'	{0} *{1} = malloc({2} * sizeof({0}));\n'.format(
											v.attrib["type"], v.attrib["name"], v.attrib["nmemb"]
										)
									)
								else:
									f.write(
										'	{} {};\n'.format(v.attrib["type"], v.attrib["name"])
									)
							# Explicit variable initialisation
							# XXX: Note that big variables may lead to stack overflow!
							else:
								if int(v.attrib["nmemb"]) > 1:
									f.write(
										(
											'	{} {}[{}] = {{\n'
											'		{}\n'
											'	}};\n'.format(v.attrib["type"], v.attrib["name"], v.attrib["nmemb"], v.text)
										)
									)
								else:
									f.write(
										'	{} {} = {};\n'.format(v.attrib["type"], v.attrib["name"], v.text)
									)
	
							# Part 2: device variable
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									'	cl_mem {}K = NULL;\n'.format(v.attrib["name"])
								)
						elif "output" == v.tag:
							# Part 1: host variable
							# For output, initialisation data must come from PREAMBLE.
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									'	{0} *{1} = malloc({2} * sizeof({0}));\n'.format(
										v.attrib["type"], v.attrib["name"], v.attrib["nmemb"]
									)
								)
							else:
								f.write(
									'	{} {};\n'.format(v.attrib["type"], v.attrib["name"])
								)
	
							# Part 2: validation variable
							if ("novalidation" not in v.attrib) or (v.attrib["novalidation"] != "true"):
								# Function is being used instead of explicit validation variable assignment
								if v.text is None:
									if int(v.attrib["nmemb"]) > 1:
										f.write(
											'	{} {}C[{}];\n'.format(v.attrib["type"], v.attrib["name"], v.attrib["nmemb"])
										)
									else:
										f.write(
											'	{} {}C;\n'.format(v.attrib["type"], v.attrib["name"])
										)
								# Explicit variable assignment
								# XXX: Note that big variables may lead to stack overflow!
								else:
									if int(v.attrib["nmemb"]) > 1:
										f.write(
											(
												'	{} {}C[{}] = {{\n'
												'		{}\n'
												'	}};\n'.format(v.attrib["type"], v.attrib["name"], v.attrib["nmemb"], v.text)
											)
										)
									else:
										f.write(
											'	{} {}C = {};\n'.format(v.attrib["type"], v.attrib["name"], v.text)
										)
								# Epsilon variable (if supplied)
								if "epsilon" in v.attrib:
									f.write(
										'	double {}Epsilon = {};\n'.format(v.attrib["name"], v.attrib["epsilon"])
									)
	
							# Part 3: device variable
							f.write(
								'	cl_mem {}K = NULL;\n'.format(v.attrib["name"])
							)

			# Call PREAMBLE function if "preamble" attribute is "yes"
			if "preamble" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["preamble"]:
				f.write(
					'\n'
					'	/* Calling preamble function */\n'
					'	PRINT_STEP("Calling preamble function...");\n'
					'	PREAMBLE('
				)

				# Print arguments
				firstExec = True
				for v, n in zip(self._varNameList[::2], self._varNameList[1::2]):
					if not firstExec:
						f.write(', ')
					else:
						firstExec = False

					f.write(v)

					if int(n) > 1:
						f.write(', {}'.format(n))

				f.write(
					(
						');\n'
						'	PRINT_SUCCESS();\n'
					)
				)


	# Print clGetPlatformIDs section
	def printGetPlatformIDs(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Get platforms IDs */\n'
					'	PRINT_STEP("Getting platforms IDs...");\n'
					'	fRet = clGetPlatformIDs(0, NULL, &platformsLen);\n'
					'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clGetPlatformIDs"));\n'
					'	platforms = malloc(platformsLen * sizeof(cl_platform_id));\n'
					'	fRet = clGetPlatformIDs(platformsLen, platforms, NULL);\n'
					'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clGetPlatformIDs"));\n'
					'	PRINT_SUCCESS();\n'
				)
			)


	# Print clGetDevicesIDs section
	def printGetDevicesIDs(self):
		with open(self._targetFile, "a") as f:
			platformID = '0'
			for k in self._xmlRoot:
				if "devinfo" == k.tag:
					platformID = k.attrib["platform"]

			f.write(
				(
					'	/* Get devices IDs for first platform availble */\n'
					'	PRINT_STEP("Getting devices IDs for first platform...");\n'
					'	fRet = clGetDeviceIDs(platforms[{0}], CL_DEVICE_TYPE_ALL, 0, NULL, &devicesLen);\n'
					'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clGetDevicesIDs"));\n'
					'	devices = malloc(devicesLen * sizeof(cl_device_id));\n'
					'	fRet = clGetDeviceIDs(platforms[{0}], CL_DEVICE_TYPE_ALL, devicesLen, devices, NULL);\n'
					'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clGetDevicesIDs"));\n'
					'	PRINT_SUCCESS();\n'.format(platformID)
				)
			)


	# Print clCreateContext section
	def printCreateContext(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Create context for first available device */\n'
					'	PRINT_STEP("Creating context...");\n'
					'	context = clCreateContext(NULL, 1, devices, NULL, NULL, &fRet);\n'
					'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clCreateContext"));\n'
					'	PRINT_SUCCESS();\n'
				)
			)


	# Print clCreateCommandQueues section
	def printCreateCommandQueues(self):
		with open(self._targetFile, "a") as f:
			deviceID = '0'
			for k in self._xmlRoot:
				if "devinfo" == k.tag:
					deviceID = k.attrib["device"]

			for k in self._xmlRoot:
				if "kernel" == k.tag:
					f.write(
						(
							'	/* Create command queue for {0} kernel */\n'
							'	PRINT_STEP("Creating command queue for \\"{0}\\"...");\n'
							'	queue{1} = clCreateCommandQueue(context, devices[{2}], 0, &fRet);\n'
							'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clCreateCommandQueue"));\n'
							'	PRINT_SUCCESS();\n'.format(k.attrib["name"], k.attrib["name"].title(), deviceID)
						)
					)


	# Print clCreateProgramWithBinary and clBuildProgram section
	def printCreateAndBuildProgram(self):
		with open(self._targetFile, "a") as f:
			filename = self._xmlRoot.attrib["program"] if "program" in self._xmlRoot.attrib else self._xmlRoot.attrib["binary"]

			f.write(
				(
					'	/* Open binary file */\n'
					'	PRINT_STEP("Opening program binary...");\n'
					'	programFile = fopen("{0}", "rb");\n'
					'	ASSERT_CALL(programFile, POSIX_ERROR_STATEMENTS("{0}"));\n'
					'	PRINT_SUCCESS();\n'
					'\n'
					'	/* Get size and read file */\n'
					'	PRINT_STEP("Reading program binary...");\n'
					'	fseek(programFile, 0, SEEK_END);\n'
					'	programSz = ftell(programFile);\n'
					'	fseek(programFile, 0, SEEK_SET);\n'
					'	programContent = malloc(programSz);\n'
					'	fread(programContent, programSz, 1, programFile);\n'
					'	fclose(programFile);\n'
					'	programFile = NULL;\n'
					'	PRINT_SUCCESS();\n'
					'\n'.format(filename)
				)
			)

			if "program" in self._xmlRoot.attrib:
				f.write(
					(
						'	/* Create program from binary file */\n'
						'	PRINT_STEP("Creating program from binary...");\n'
						'	program = clCreateProgramWithBinary(context, 1, devices, &programSz, (const unsigned char **) &programContent, &programRet, &fRet);\n'
						'	ASSERT_CALL(CL_SUCCESS == programRet, FUNCTION_ERROR_STATEMENTS("clCreateProgramWithBinary (when loading binary)"));\n'
						'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clCreateProgramWithBinary"));\n'
						'	PRINT_SUCCESS();\n'
						'\n'
					)
				)
			else:
				f.write(
					(
						'	/* Create program from source file */\n'
						'	PRINT_STEP("Creating program from source...");\n'
						'	program = clCreateProgramWithSource(context, 1, (const char **) &programContent, &programSz, &fRet);\n'
						'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clCreateProgramWithSource"));\n'
						'	PRINT_SUCCESS();\n'
						'\n'
					)
				)

			f.write(
				(
					'	/* Build program */\n'
					'	PRINT_STEP("Building program...");\n'
					'	fRet = clBuildProgram(program, 1, devices, NULL, NULL, NULL);\n'
					'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clBuildProgram"));\n'
					'	PRINT_SUCCESS();\n'
				)
			)


	# Print clCreateKernel for each kernel
	def printCreateKernels(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					f.write(
						(
							'	/* Create {0} kernel */\n'
							'	PRINT_STEP("Creating kernel \\"{0}\\" from program...");\n'
							'	kernel{1} = clCreateKernel(program, "{0}", &fRet);\n'
							'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clCreateKernel"));\n'
							'	PRINT_SUCCESS();\n'.format(k.attrib["name"], k.attrib["name"].title())
						)
					)


	# Print clCreateBuffer for all buffered variables
	def printCreateBuffers(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Create input and output buffers */\n'
					'	PRINT_STEP("Creating buffers...");\n'
				)
			)

			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						if "input" == v.tag and int(v.attrib["nmemb"]) > 1:
							f.write(
								(
									'	{0}K = clCreateBuffer(context, CL_MEM_READ_ONLY, {1} * sizeof({2}), NULL, &fRet);\n'
									'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clCreateBuffer ({0}K)"));\n'.format(
										v.attrib["name"],
										v.attrib["nmemb"],
										v.attrib["type"]
									)
								)
							)
						elif "output" == v.tag:
							f.write(
								(
									'	{0}K = clCreateBuffer(context, CL_MEM_READ_WRITE, {1} * sizeof({2}), NULL, &fRet);\n'
									'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clCreateBuffer ({0}K)"));\n'.format(
										v.attrib["name"],
										v.attrib["nmemb"],
										v.attrib["type"]
									)
								)
							)

			f.write(
				'	PRINT_SUCCESS();\n'
			)


	# Print clSetKernelArgs for all kernels arguments
	def printSetKernelsArgs(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					f.write(
						(
							'	/* Set kernel arguments for {0} */\n'
							'	PRINT_STEP("Setting kernel arguments for \\"{0}\\"...");\n'.format(k.attrib["name"])
						)
					)
	
					for v in k:
						# If it is an input variable and its size is 1, send the variable explicitely
						if "input" == v.tag and 1 == int(v.attrib["nmemb"]):
							f.write(
								(
									'	fRet = clSetKernelArg(kernel{0}, {1}, sizeof({2}), &{3});\n'
									'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clSetKernelArg ({3})"));\n'.format(
										k.attrib["name"].title(), v.attrib["arg"], v.attrib["type"], v.attrib["name"]
									)
								)
							)
						elif "input" == v.tag or "output" == v.tag:
							f.write(
								(
									'	fRet = clSetKernelArg(kernel{0}, {1}, sizeof(cl_mem), &{2}K);\n'
									'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clSetKernelArg ({2}K)"));\n'.format(k.attrib["name"].title(), v.attrib["arg"], v.attrib["name"])
								)
							)
						# Arguments with __local keyword
						elif "local" == v.tag:
							f.write(
								(
									'	fRet = clSetKernelArg(kernel{0}, {1}, {2} * sizeof({3}), NULL);\n'
									'	ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clSetKernelArg (__local {1})"));\n'.format(
										k.attrib["name"].title(),
										v.attrib["arg"],
										v.attrib["nmemb"],
										v.attrib["type"]
									)
								)
							)

				f.write(
					'	PRINT_SUCCESS();\n'
				)


	# Print loop header and first calls
	def printLoopHeader(self):
		with open(self._targetFile, "a") as f:
			f.write('	do {\n')

			# Call LOOPPREAMBLE if set
			if "looppreamble" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["looppreamble"]:
				f.write(
					'		/* Calling loop preamble function */\n'
					'		PRINT_STEP("[%d] Calling loop preamble function...", i);\n'
					'		LOOPPREAMBLE('
				)

				for v, n in zip(self._varNameList[::2], self._varNameList[1::2]):
					f.write(
						'{}, '.format(v)
					)

					if int(n) > 1:
						f.write('{}, '.format(n))

				f.write(
					(
						'loopFlag);\n'
						'		PRINT_SUCCESS();\n'
						'\n'.format(v)
					)
				)

			f.write(
				(
					'		/* Setting input and output buffers */\n'
					'		PRINT_STEP("[%d] Setting buffers...", i);\n'
				)
			)

			# For each kernel, set the input/output data
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						# clEnqueueWriteBuffer for arrays, clSetKernelArg for single input
						if "input" == v.tag:
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									(
										'		fRet = clEnqueueWriteBuffer(queue{0}, {1}K, CL_TRUE, 0, {2} * sizeof({3}), {1}, 0, NULL, NULL);\n'
										'		ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clEnqueueWriteBuffer ({1}K)"));\n'.format(
											k.attrib["name"].title(),
											v.attrib["name"],
											v.attrib["nmemb"],
											v.attrib["type"]
										)
									)
								)
							else:
								f.write(
									(
										'		fRet = clSetKernelArg(kernel{0}, {1}, sizeof({2}), &{3});\n'
										'		ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clSetKernelArg ({3})"));\n'.format(
											k.attrib["name"].title(), v.attrib["arg"], v.attrib["type"], v.attrib["name"]
										)
									)
								)
						elif "output" == v.tag:
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									(
										'		fRet = clEnqueueWriteBuffer(queue{0}, {1}K, CL_TRUE, 0, {2} * sizeof({3}), {1}, 0, NULL, NULL);\n'
										'		ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clEnqueueWriteBuffer ({1}K)"));\n'.format(
											k.attrib["name"].title(),
											v.attrib["name"],
											v.attrib["nmemb"],
											v.attrib["type"]
										)
									)
								)
							else:
								f.write(
									(
										'		fRet = clEnqueueWriteBuffer(queue{0}, {1}K, CL_TRUE, 0, sizeof({2}), &{1}, 0, NULL, NULL);\n'
										'		ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clEnqueueWriteBuffer ({1}K)"));\n'.format(
											k.attrib["name"].title(),
											v.attrib["name"],
											v.attrib["type"]
										)
									)
								)

			f.write(
				'		PRINT_SUCCESS();\n'
			)


	# Print clEnqueueNDRangeKernel for all kernels
	def printEnqueueKernel(self):
		with open(self._targetFile, "a") as f:
			hasOrder = False
			profile = "profile" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["profile"]
			kernels = {}
			orderedIndexes = []

			# If order attribute is found in at least one kernel, we assume that all kernels has order attributes
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					if "order" in k.attrib:
						hasOrder = True

			# Kernels has ordering
			if hasOrder:
				# For every kernel
				for k in self._xmlRoot:
					if "kernel" == k.tag:
						order = int(k.attrib["order"])
	
						# First time this order number is being used
						if order not in orderedIndexes:
							# Append order number to order list
							orderedIndexes.append(order)
							# Create an array in the dictionary
							kernels[order] = []
	
						# Append kernel number to the order in the dictionary
						kernels[order].append(k)

				# Sort order list
				orderedIndexes = sorted(orderedIndexes)

				# Declare event blockers
				f.write(
					(
						'		cl_event blockers[{}];\n'
						'		PRINT_STEP("[%d] Running kernels...", i);\n'.format(len(orderedIndexes) - 1)
					)
				)

				# If profiling is on, get "then"
				if profile:
					f.write(
						'		gettimeofday(&then, NULL);\n'
					)

				# Iterate through all orders
				for i in range(0, len(orderedIndexes)):
					# Get kernel based on order and enqueue it
					for k in kernels[orderedIndexes[i]]:
						dim = "1"
						localSize = "NULL"
						for v in k:
							if "ndrange" == v.tag:
								for d in v:
									if "local" == d.tag:
										localSize = "localSize{}".format(k.attrib["name"].title())

						f.write(
							(
								'		fRet = clEnqueueNDRangeKernel(queue{0}, kernel{0}, workDim{0}, NULL, globalSize{0}, {1}, {2}, {3}, {4});\n'
								'		ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clEnqueueNDRangeKernel"));\n'.format(
									k.attrib["name"].title(),
									localSize,
									"0" if 0 == i else "1",
									"NULL" if 0 == i else "&blockers[{}]".format(i - 1),
									"&blockers[{}]".format(i) if i < (len(orderedIndexes) - 1) else "NULL"
								)
							)
						)

				# If profiling is on, get "now"
				if profile:
					f.write(
						'		gettimeofday(&now, NULL);\n'
					)

				f.write(
					'		PRINT_SUCCESS();\n'
				)
			# Kernels has no ordering
			else:
				f.write(
					'		PRINT_STEP("[%d] Running kernels...", i);\n'
				)

				# If profiling is on, get "then"
				if profile:
					f.write(
						'		gettimeofday(&then, NULL);\n'
					)

				for k in self._xmlRoot:
					if "kernel" == k.tag:
						dim = "1"
						localSize = "NULL"
						for v in k:
							if "ndrange" == v.tag:
								for d in v:
									if "local" == d.tag:
										localSize = "localSize{}".format(k.attrib["name"].title())
	
						f.write(
							(
								'		fRet = clEnqueueNDRangeKernel(queue{0}, kernel{0}, workDim{0}, NULL, globalSize{0}, {1}, 0, NULL, NULL);\n'
								'		ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clEnqueueNDRangeKernel"));\n'.format(
									k.attrib["name"].title(),
									localSize
								)
							)
						)

				# If profiling is on, get "now"
				if profile:
					f.write(
						'		gettimeofday(&now, NULL);\n'
					)

				f.write(
					'		PRINT_SUCCESS();\n'
				)


	# Print clEnqueueReadBuffer section
	def printEnqueueReadBuffer(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'		/* Get output buffers */\n'
					'		PRINT_STEP("[%d] Getting kernels arguments...", i);\n'
				)
			)

			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						if "output" == v.tag:
							f.write(
								'		fRet = clEnqueueReadBuffer(queue{0}, {1}K, CL_TRUE, 0, {2} * sizeof({3}), {4}{1}, 0, NULL, NULL);\n'.format(
									k.attrib["name"].title(),
									v.attrib["name"],
									v.attrib["nmemb"],
									v.attrib["type"],
									"" if int(v.attrib["nmemb"]) > 1 else "&"
								)
							)

			f.write(
				(
					'		ASSERT_CALL(CL_SUCCESS == fRet, FUNCTION_ERROR_STATEMENTS("clEnqueueReadBuffer"));\n'
					'		PRINT_SUCCESS();\n'
				)
			)

	# Print footer of loop
	def printLoopFooter(self):
		with open(self._targetFile, "a") as f:
			# Call LOOPPOSTAMBLE
			if "looppostamble" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["looppostamble"]:
				f.write(
					'		/* Calling loop postamble function */\n'
					'		PRINT_STEP("[%d] Calling loop postamble function...", i);\n'
					'		LOOPPOSTAMBLE('
				)

				for v, n in zip(self._varNameList[::2], self._varNameList[1::2]):
					f.write(
						'{}, '.format(v)
					)

					if int(n) > 1:
						f.write('{}, '.format(n))

				f.write(
					(
						'loopFlag);\n'
						'		PRINT_SUCCESS();\n'
					)
				)

			if "profile" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["profile"]:
				f.write(
					'		execTime += now.tv_usec - then.tv_usec;\n'
				)

			f.write(
				(
					'		i++;\n'
					'	} while(loopFlag);\n'
				)
			)


	# Print postamble
	def printPostamble(self):
		with open(self._targetFile, "a") as f:
			if "postamble" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["postamble"]:
				f.write(
					'	/* Calling postamble function */\n'
					'	PRINT_STEP("Calling postamble function...");\n'
					'	POSTAMBLE('
				)

				firstExec = True
				for v, n in zip(self._varNameList[::2], self._varNameList[1::2]):
					if not firstExec:
						f.write(', ')
					else:
						firstExec = False

					f.write(v)

					if int(n) > 1:
						f.write(', {}'.format(n))

				f.write(
					(
						');\n'
						'	PRINT_SUCCESS();\n'
					)
				)


	# Print code for output validation
	def printValidation(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Validate received data */\n'
					'	PRINT_STEP("Validating received data...");\n'
				)
			)

			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						if ("output" == v.tag) and (("novalidation" not in v.attrib) or (v.attrib["novalidation"] != "true")):
							# Variable is of vector type (e.g. cl_double2)
							if v.attrib["type"] in self._vectorTypes:
								vectorType = self._vectorTypes[v.attrib["type"]]
								if int(v.attrib["nmemb"]) > 1:
									if "epsilon" in v.attrib:
										validationStr = 'TEST_EPSILON({0}C[i].s[j], {0}[i].s[j], {0}Epsilon)'.format(v.attrib["name"])
										validationStr2 = ' (with epsilon)'
									else: 
										validationStr = '{0}C[i].s[j] != {0}[i].s[j]'.format(v.attrib["name"])
										validationStr2 = ''
	
									f.write(
										(
											'	for(i = 0; i < {0}; i++) {{\n'
											'		for(j = 0; j < {1}; j++) {{\n'
											'			if({2}) {{\n'
											'				if(!invalidDataFound) {{\n'
											'					PRINT_FAIL();\n'
											'					invalidDataFound = true;\n'
											'				}}\n'
											'				printf("Variable {3}[%d].s[%d]: expected %{4} got %{4}{5}.\\n", i, j, {3}C[i].s[j], {3}[i].s[j]);\n'
											'			}}\n'
											'		}}\n'
											'	}}\n'.format(
												v.attrib["nmemb"],
												vectorType[0],
												validationStr,
												v.attrib["name"],
												self._printfMapper[vectorType[1]] if vectorType[1] in self._printfMapper else "x",
												validationStr2
											)
										)
									)
								else:
									if "epsilon" in v.attrib:
										validationStr = 'TEST_EPSILON({0}C.s[i], {0}.s[i], {0}Epsilon)'.format(v.attrib["name"])
										validationStr2 = ' (with epsilon)'
									else: 
										validationStr = '{0}C.s[i] != {0}.s[i]'.format(v.attrib["name"])
										validationStr2 = ''
	
									f.write(
										(
											'	for(i = 0; i < {0}; i++) {{\n'
											'		if({1}) {{\n'
											'			if(!invalidDataFound) {{\n'
											'				PRINT_FAIL();\n'
											'				invalidDataFound = true;\n'
											'			}}\n'
											'			printf("Variable {2}.s[%d]: expected %{3} got %{3}{4}.\\n", i, {2}C.s[j], {2}.s[j]);\n'
											'		}}\n'
											'	}}\n'.format(
												vectorType[0],
												validationStr,
												v.attrib["name"],
												self._printfMapper[vectorType[1]] if vectorType[1] in self._printfMapper else "x",
												validationStr2
											)
										)
									)
							# Not vector type variable
							else:
								if int(v.attrib["nmemb"]) > 1:
									if "epsilon" in v.attrib:
										validationStr = 'TEST_EPSILON({0}C[i],  {0}[i], {0}Epsilon)'.format(v.attrib["name"])
										validationStr2 = ' (with epsilon)'
									else: 
										validationStr = '{0}C[i] != {0}[i]'.format(v.attrib["name"])
										validationStr2 = ''
	
									f.write(
										(
											'	for(i = 0; i < {0}; i++) {{\n'
											'		if({1}) {{\n'
											'			if(!invalidDataFound) {{\n'
											'				PRINT_FAIL();\n'
											'				invalidDataFound = true;\n'
											'			}}\n'
											'			printf("Variable {2}[%d]: expected %{3} got %{3}{4}.\\n", i, {2}C[i], {2}[i]);\n'
											'		}}\n'
											'	}}\n'.format(
												v.attrib["nmemb"],
												validationStr,
												v.attrib["name"],
												self._printfMapper[v.attrib["type"]] if v.attrib["type"] in self._printfMapper else "x",
												validationStr2
											)
										)
									)
								else:
									if "epsilon" in v.attrib:
										validationStr = 'TEST_EPSILON({0}C, {0}, {0}Epsilon)'.format(v.attrib["name"])
										validationStr2 = ' (with epsilon)'
									else: 
										validationStr = '{0}C != {0}'.format(v.attrib["name"])
										validationStr2 = ''
	
									f.write(
										(
											'	if({0}) {{\n'
											'		if(!invalidDataFound) {{\n'
											'			PRINT_FAIL();\n'
											'			invalidDataFound = true;\n'
											'		}}\n'
											'		printf("Variable {1}: expected %{2} got %{2}{3}.\\n", i, {1}C, {1});\n'
											'	}}\n'.format(
												validationStr,
												v.attrib["name"],
												self._printfMapper[v.attrib["type"]] if v.attrib["type"] in self._printfMapper else "x",
												validationStr2
											)
										)
									)

			f.write(
				(
					'	if(!invalidDataFound)\n'
					'		PRINT_SUCCESS();\n'
				)
			)


	# Print code for output validation
	def printProfileResults(self):
		with open(self._targetFile, "a") as f:
			if "profile" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["profile"]:
				f.write(
					(
						'	/* Print profiling results */\n'
						'	printf("Elapsed time spent on kernels: %ld us; Average time per iteration: %ld us.\\n", execTime, execTime / i);\n'
					)
				)


	# Print error label
	def printErrorLabel(self):
		with open(self._targetFile, "a") as f:
			f.write(
				'_err:\n'
			)


	# Print clReleaseMemObject section
	def printFreeBuffers(self):
		with open(self._targetFile, "a") as f:
			f.write(
				'	/* Dealloc buffers */\n'
			)

			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						if ("input" == v.tag or "output" == v.tag) and int(v.attrib["nmemb"]) > 1:
							f.write(
								(
									'	if({0}K)\n'
									'		clReleaseMemObject({0}K);\n'.format(v.attrib["name"])
								)
							)


	# Print variable deallocs section
	def printFreeVariables(self):
		with open(self._targetFile, "a") as f:
			f.write(
				'	/* Dealloc variables */\n'
			)

			# Iterate through every variable of every kernel
			for k in self._xmlRoot:
				if "kernel" == k.tag:
					for v in k:
						if "input" == v.tag:
							if v.text is None:
								if int(v.attrib["nmemb"]) > 1:
									f.write(
										'	free({});\n'.format(v.attrib["name"])
									)
						elif "output" == v.tag:
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									'	free({});\n'.format(v.attrib["name"])
								)


	# Print clReleaseKernel section
	def printFreeKernels(self):
		with open(self._targetFile, "a") as f:
			f.write(
				'	/* Dealloc kernels */\n'
			)

			for k in self._xmlRoot:
				if "kernel" == k.tag:
					f.write(
						(
							'	if(kernel{0})\n'
							'		clReleaseKernel(kernel{0});\n'.format(k.attrib["name"].title())
						)
					)


	# Print clReleaseProgram section
	def printFreeProgram(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Dealloc program */\n'
					'	if(program)\n'
					'		clReleaseProgram(program);\n'
					'	if(programContent)\n'
					'		free(programContent);\n'
					'	if(programFile)\n'
					'		fclose(programFile);\n'
				)
			)


	# Print clReleaseCommandQueue section
	def printFreeQueues(self):
		with open(self._targetFile, "a") as f:
			f.write(
				'	/* Dealloc queues */\n'
			)

			for k in self._xmlRoot:
				if "kernel" == k.tag:
					f.write(
						(
							'	if(queue{0})\n'
							'		clReleaseCommandQueue(queue{0});\n'.format(k.attrib["name"].title())
						)
					)


	# Print last OpenCL deallocs
	def printFreeFinalOpenCL(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Last OpenCL variables */\n'
					'	if(context)\n'
					'		clReleaseContext(context);\n'
					'	if(devices)\n'
					'		free(devices);\n'
					'	if(platforms)\n'
					'		free(platforms);\n'
				)
			)


	# Print cleanup function
	def printCleanup(self):
		with open(self._targetFile, "a") as f:
			# Call CLEANUP function if "cleanup" attribute is "yes"
			if "cleanup" in self._xmlRoot.attrib and "yes" == self._xmlRoot.attrib["cleanup"]:
				f.write(
					'	/* Calling cleanup function */\n'
					'	CLEANUP('
				)

				# Print arguments
				firstExec = True
				for v, n in zip(self._varNameList[::2], self._varNameList[1::2]):
					if not firstExec:
						f.write(', ')
					else:
						firstExec = False

					f.write(v)

					if int(n) > 1:
						f.write(', {}'.format(n))

				f.write(
					');\n'
				)


	# Print last part of code
	def printFooter(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	return rv;\n'
					'}\n'
				)
			)
