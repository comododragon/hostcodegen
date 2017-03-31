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


	def __init__(self, xmlFile, targetFile):
		self._xmlRoot = ElementTree.parse(xmlFile).getroot()

		# Clean file
		self._targetFile = targetFile
		with open(self._targetFile, "w") as f:
			pass


	# Print header: includes, macros, function prototypes and first declarations of main()
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
					'/**\n'
					' * @brief Standard statements for OpenCL error handling and printing.\n'
					' *\n'
					' * @param funcName Function name that failed.\n'
					' */\n'
					'#define CL_ERROR_STATEMENTS(funcName) {\\\n'
					'	rv = EXIT_FAILURE;\\\n'
					'	PRINT_FAIL();\\\n'
					'	fprintf(stderr, "Error: %s failed with return code %d.\\n", funcName, clRet);\\\n'
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
				)
			)

			# Iterate through every variable declaration
			firstPrinted = False
			for k in self._xmlRoot:
				for v in k:
					# If function attribute is present, the function prototype must be declared before main()
					if "function" in v.attrib:
						if not firstPrinted:
							f.write(
								'/* Functions prototypes for input and/or output data */\n'
							)
							firstPrinted = True

						if int(v.attrib["nmemb"]) > 1:
							f.write(
								'void {}({} *, int, int);\n'.format(v.attrib["function"], v.attrib["type"])
							)
						else:
							f.write(
								'{} {}(void);\n'.format(v.attrib["type"], v.attrib["function"])
							)
			if firstPrinted:
				f.write('\n')

			f.write(
				(
					'int main(void) {\n'
					'	int rv = EXIT_SUCCESS;\n'
					'\n'
					'	int i;\n'
					'	cl_int platformsLen, devicesLen, clRet;\n'
					'	cl_platform_id *platforms = NULL;\n'
					'	cl_device_id *devices = NULL;\n'
					'	cl_context context = NULL;\n'
				)
			)


	# Print queue declarations for each kernel
	def printQueueDeclarations(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
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
					'	char *programBin = NULL;\n'
					'	cl_int programRet;\n'
					'	cl_program program = NULL;\n'
				)
			)


	# Print kernel declarations
	def printKernelDeclarations(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				f.write(
					'	cl_kernel kernel{} = NULL;\n'.format(k.attrib["name"].title())
				)


	# Print last declarations: some flags and other stuff
	def printLastDeclarations(self):
		with open(self._targetFile, "a") as f:
			f.write(
				'	bool invalidDataFound = false;\n'
			)

			# Iterate through every kernel
			for k in self._xmlRoot:
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
			# Configure multiplier string
			if "repeat" in self._xmlRoot.attrib:
				repeatCnt = int(self._xmlRoot.attrib["repeat"])
				multiplierStr = " * {}".format(repeatCnt)
			else:
				repeatCnt = 1
				multiplierStr = ""

			# Iterate through every variable of every kernel
			for k in self._xmlRoot:
				for v in k:
					# Function is being used instead of explicit variable assignment
					if "function" in v.attrib:
						# Declare variable, its opencl buffer and call the function to assign values to variable
						if "input" == v.tag:
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									'	{0} {1}[{2}{3}];\n'
									'	cl_mem {1}K = NULL;\n'
									'	{4}({1}, {2}, {5});\n'.format(
										v.attrib["type"],
										v.attrib["name"],
										v.attrib["nmemb"],
										multiplierStr,
										v.attrib["function"],
										repeatCnt
									)
								)
							else:
								f.write(
									'	{0} {1} = {2}();\n'.format(v.attrib["type"], v.attrib["name"], v.attrib["function"])
								)
						# Declare variable, its opencl buffer and call the function to assign values to validation variable
						elif "output" == v.tag:
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									(
										'	{0} {1}[{2}{3}];\n'
										'	cl_mem {1}K = NULL;\n'
										'	{0} {1}C[{2}{3}];\n'
										'	{4}({1}C, {2}, {5});\n'.format(
											v.attrib["type"],
											v.attrib["name"],
											v.attrib["nmemb"],
											multiplierStr,
											v.attrib["function"],
											repeatCnt
										)
									)
								)
							else:
								f.write(
									(
										'	{0} {1};\n'
										'	cl_mem {1}K;\n'
										'	{0} {1}C = {2}();\n'.format(v.attrib["type"], v.attrib["name"], v.attrib["function"])
									)
								)
					# Explicit variable assignment
					else:
						# Declare variable, assign values to it and declare its opencl buffer
						if "input" == v.tag:
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									'	{} {}[{}{}] = {{\n'.format(v.attrib["type"], v.attrib["name"], v.attrib["nmemb"], multiplierStr)
								)

								for x in range(0, repeatCnt):
									f.write(
										'		{}{}\n'.format(v.text, "" if x == (repeatCnt - 1) else ",")
									)

								f.write(
									(
										'	}};\n'
										'	cl_mem {}K = NULL;\n'.format(v.attrib["name"])
									)
								)
							else:
								f.write(
									'	{} {} = {};\n'.format(v.attrib["type"], v.attrib["name"], v.text)
								)
						# Declare variable, assign values to its validation variable and declare its opencl buffer
						elif "output" == v.tag:
							if int(v.attrib["nmemb"]) > 1:
								f.write(
									(
										'	{0} {1}[{2}{3}];\n'
										'	cl_mem {1}K = NULL;\n'.format(
											v.attrib["type"],
											v.attrib["name"],
											v.attrib["nmemb"],
											multiplierStr
										)
									)
								)
								if v.text is not None:
									f.write(
										'	{} {}C[{}{}] = {{\n'.format(
											v.attrib["type"],
											v.attrib["name"],
											v.attrib["nmemb"],
											multiplierStr
										)
									)

									for x in range(0, repeatCnt):
										f.write(
											'		{}{}\n'.format(v.text, "" if x == (repeatCnt - 1) else ",")
										)

									f.write(
										'	};\n'
									)
							else:
								f.write(
									(
										'	{0} {1};\n'
										'	cl_mem {1}K;\n'.format(v.attrib["type"], v.attrib["name"])
									)
								)

								if v.text is not None:
									f.write(
										'	{} {}C = {};\n'.format(v.attrib["type"], v.attrib["name"], v.text)
									)


	# Print clGetPlatformIDs section
	def printGetPlatformIDs(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Get platforms IDs */\n'
					'	PRINT_STEP("Getting platforms IDs...");\n'
					'	clRet = clGetPlatformIDs(0, NULL, &platformsLen);\n'
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clGetPlatformIDs"));\n'
					'	platforms = malloc(platformsLen * sizeof(cl_platform_id));\n'
					'	clRet = clGetPlatformIDs(platformsLen, platforms, NULL);\n'
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clGetPlatformIDs"));\n'
					'	PRINT_SUCCESS();\n'
				)
			)


	# Print clGetDevicesIDs section
	def printGetDevicesIDs(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Get devices IDs for first platform availble */\n'
					'	PRINT_STEP("Getting devices IDs for first platform...");\n'
					'	clRet = clGetDeviceIDs(platforms[0], CL_DEVICE_TYPE_ACCELERATOR, 0, NULL, &devicesLen);\n'
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clGetDevicesIDs"));\n'
					'	devices = malloc(devicesLen * sizeof(cl_device_id));\n'
					'	clRet = clGetDeviceIDs(platforms[0], CL_DEVICE_TYPE_ACCELERATOR, devicesLen, devices, NULL);\n'
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clGetDevicesIDs"));\n'
					'	PRINT_SUCCESS();\n'
				)
			)


	# Print clCreateContext section
	def printCreateContext(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Create context for first available device */\n'
					'	PRINT_STEP("Creating context...");\n'
					'	context = clCreateContext(NULL, 1, devices, NULL, NULL, &clRet);\n'
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clCreateContext"));\n'
					'	PRINT_SUCCESS();\n'
				)
			)


	# Print clCreateCommandQueues section
	def printCreateCommandQueues(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				f.write(
					(
						'	/* Create command queue for {0} kernel */\n'
						'	PRINT_STEP("Creating command queue for \\"{0}\\"...");\n'
						'	queue{1} = clCreateCommandQueue(context, devices[0], 0, &clRet);\n'
						'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clCreateCommandQueue"));\n'
						'	PRINT_SUCCESS();\n'.format(k.attrib["name"], k.attrib["name"].title())
					)
				)


	# Print clCreateProgramWithBinary and clBuildProgram section
	def printCreateAndBuildProgram(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Open aocx file */\n'
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
					'	programBin = malloc(programSz);\n'
					'	fread(programBin, programSz, 1, programFile);\n'
					'	fclose(programFile);\n'
					'	programFile = NULL;\n'
					'	PRINT_SUCCESS();\n'
					'\n'
					'	/* Create program from aocx file */\n'
					'	PRINT_STEP("Creating program from binary...");\n'
					'	program = clCreateProgramWithBinary(context, 1, devices, &programSz, (const unsigned char **) &programBin, &programRet, &clRet);\n'
					'	ASSERT_CALL(CL_SUCCESS == programRet, CL_ERROR_STATEMENTS("clCreateProgramWithBinary (when loading aocx)"));\n'
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clCreateProgramWithBinary"));\n'
					'	PRINT_SUCCESS();\n'
					'\n'
					'	/* Build program */\n'
					'	PRINT_STEP("Building program...");\n'
					'	clRet = clBuildProgram(program, 1, devices, NULL, NULL, NULL);\n'
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clBuildProgram"));\n'
					'	PRINT_SUCCESS();\n'.format(self._xmlRoot.attrib["program"])
				)
			)


	# Print clCreateKernel for each kernel
	def printCreateKernels(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				f.write(
					(
						'	/* Create {0} kernel */\n'
						'	PRINT_STEP("Creating kernel \\"{0}\\" from program...");\n'
						'	kernel{1} = clCreateKernel(program, "{0}", &clRet);\n'
						'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clCreateKernel"));\n'
						'	PRINT_SUCCESS();\n'.format(k.attrib["name"], k.attrib["name"].title())
					)
				)


	# Print clCreateBuffer for all buffered variables
	def printCreateBuffers(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	/* Create input and output buffers */\n'
					'	PRINT_STEP("Creating and setting buffers...");\n'
				)
			)

			multiplierStr = " * {}".format(self._xmlRoot.attrib["repeat"]) if "repeat" in self._xmlRoot.attrib else ""

			for k in self._xmlRoot:
				for v in k:
					if "input" == v.tag:
						if int(v.attrib["nmemb"]) > 1:
							f.write(
								(
									'	{0}K = clCreateBuffer(context, CL_MEM_COPY_HOST_PTR | CL_MEM_READ_ONLY, {1}{2} * sizeof({3}), {0}, &clRet);\n'
									'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clCreateBuffer ({0}K)"));\n'.format(
										v.attrib["name"],
										v.attrib["nmemb"],
										multiplierStr,
										v.attrib["type"]
									)
								)
							)
					elif "output" == v.tag:
						if int(v.attrib["nmemb"]) > 1:
							f.write(
								(
									'	{0}K = clCreateBuffer(context, CL_MEM_COPY_HOST_PTR, {1}{2} * sizeof({3}), {0}, &clRet);\n'
									'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clCreateBuffer ({0}K)"));\n'.format(
										v.attrib["name"],
										v.attrib["nmemb"],
										multiplierStr,
										v.attrib["type"]
									)
								)
							)
						else:
							f.write(
								(
									'	{0}K = clCreateBuffer(context, CL_MEM_COPY_HOST_PTR, {1} * sizeof({2}), &{0}, &clRet);\n'
									'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clCreateBuffer ({0}K)"));\n'.format(
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
				f.write(
					(
						'	/* Set kernel arguments for {0} */\n'
						'	PRINT_STEP("Setting kernel arguments for \\"{0}\\"...");\n'.format(k.attrib["name"])
					)
				)

				for v in k:
					if "input" == v.tag and 1 == int(v.attrib["nmemb"]):
						f.write(
							(
								'	clRet = clSetKernelArg(kernel{0}, {1}, sizeof({2}), &{3});\n'
								'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clSetKernelArg ({3})"));\n'.format(k.attrib["name"].title(), v.attrib["arg"], v.attrib["type"], v.attrib["name"])
							)
						)
					elif "input" == v.tag or "output" == v.tag:
						f.write(
							(
								'	clRet = clSetKernelArg(kernel{0}, {1}, sizeof(cl_mem), &{2}K);\n'
								'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clSetKernelArg ({2}K)"));\n'.format(k.attrib["name"].title(), v.attrib["arg"], v.attrib["name"])
							)
						)

				f.write(
					'	PRINT_SUCCESS();\n'
				)


	# Print clEnqueueNDRangeKernel for all kernels
	def printEnqueueKernel(self):
		with open(self._targetFile, "a") as f:
			hasOrder = False
			kernels = {}
			orderedIndexes = []

			# If order attribute is found in at least one kernel, we assume that all kernels has order attributes
			for k in self._xmlRoot:
				if "order" in k.attrib:
					hasOrder = True

			# Kernels has ordering
			if hasOrder:
				# For every kernel
				for k in self._xmlRoot:
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
						'	cl_event blockers[{}];\n'
						'	PRINT_STEP("Running kernels...");\n'.format(len(orderedIndexes) - 1)
					)
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
									if "local" == v.tag:
										localSize = "localSize{}".format(k.attrib["name"].title())

						f.write(
							(
								'	clRet = clEnqueueNDRangeKernel(queue{0}, kernel{0}, workDim{0}, NULL, globalSize{0}, {1}, {2}, {3}, {4});\n'
								'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clEnqueueNDRangeKernel"));\n'.format(
									k.attrib["name"].title(),
									localSize,
									"0" if 0 == i else "1",
									"NULL" if 0 == i else "&blockers[{}]".format(i - 1),
									"&blockers[{}]".format(i) if i < (len(orderedIndexes) - 1) else "NULL"
								)
							)
						)

				f.write(
					'	PRINT_SUCCESS();\n'
				)
			# Kernels has no ordering
			else:
				f.write(
					'	PRINT_STEP("Running kernels...");\n'
				)

				for k in self._xmlRoot:
					dim = "1"
					localSize = "NULL"
					for v in k:
						if "ndrange" == v.tag:
							for d in v:
								if "local" == v.tag:
									localSize = "localSize{}".format(k.attrib["name"].title())

					f.write(
						(
							'	clRet = clEnqueueNDRangeKernel(queue{0}, kernel{0}, workDim{0}, NULL, globalSize{0}, {1}, 0, NULL, NULL);\n'
							'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clEnqueueNDRangeKernel"));\n'.format(
								k.attrib["name"].title(),
								localSize
							)
						)
					)

				f.write(
					'	PRINT_SUCCESS();\n'
				)


	# Print clEnqueueReadBuffer section
	def printEnqueueReadBuffer(self):
		with open(self._targetFile, "a") as f:
			if "repeat" in self._xmlRoot.attrib:
				repeatCnt = int(self._xmlRoot.attrib["repeat"])
				multiplierStr = " * {}".format(repeatCnt)
			else:
				repeatCnt = 1
				multiplierStr = ""

			f.write(
				(
					'	/* Get output buffers */\n'
					'	PRINT_STEP("Getting kernels arguments...");\n'
				)
			)

			for k in self._xmlRoot:
				for v in k:
					if "output" == v.tag:
						f.write(
							'	clRet = clEnqueueReadBuffer(queue{0}, {1}K, CL_TRUE, 0, {2}{3} * sizeof({4}), {5}{1}, 0, NULL, NULL);\n'.format(
								k.attrib["name"].title(),
								v.attrib["name"],
								v.attrib["nmemb"],
								multiplierStr if int(v.attrib["nmemb"]) > 1 else "",
								v.attrib["type"],
								"" if int(v.attrib["nmemb"]) > 1 else "&"
							)
						)

			f.write(
				(
					'	ASSERT_CALL(CL_SUCCESS == clRet, CL_ERROR_STATEMENTS("clEnqueueReadBuffer"));\n'
					'	PRINT_SUCCESS();\n'
				)
			)


	# Print code for output validation
	def printValidation(self):
		with open(self._targetFile, "a") as f:
			if "repeat" in self._xmlRoot.attrib:
				repeatCnt = int(self._xmlRoot.attrib["repeat"])
				multiplierStr = " * {}".format(repeatCnt)
			else:
				repeatCnt = 1
				multiplierStr = ""

			f.write(
				(
					'	/* Validate received data */\n'
					'	PRINT_STEP("Validating received data...");\n'
				)
			)

			for k in self._xmlRoot:
				for v in k:
					if "output" == v.tag and v.text is not None:
						if int(v.attrib["nmemb"]) > 1:
							f.write(
								(
									'	for(i = 0; i < {0}{1}; i++) {{\n'
									'		if({2}C[i] != {2}[i]) {{\n'
									'			if(!invalidDataFound) {{\n'
									'				PRINT_FAIL();\n'
									'				invalidDataFound = true;\n'
									'			}}\n'
									'			printf("Variable {2}[%d]: Expected %x got %x.\\n", i, {2}C[i], {2}[i]);\n'
									'		}}\n'
									'	}}\n'.format(
										v.attrib["nmemb"],
										multiplierStr,
										v.attrib["name"]
									)
								)
							)
						else:
							f.write(
								(
									'	if({0}C != {0}) {{\n'
									'		if(!invalidDataFound) {{\n'
									'			PRINT_FAIL();\n'
									'			invalidDataFound = true;\n'
									'		}}\n'
									'		printf("Variable {0}: Expected %x got %x.\\n", i, {0}C, {0});\n'
									'	}}\n'.format(v.attrib["name"])
								)
							)

			f.write(
				(
					'	if(!invalidDataFound)\n'
					'		PRINT_SUCCESS();\n'
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
			for k in self._xmlRoot:
				for v in k:
					if ("input" == v.tag or "output" == v.tag) and int(v.attrib["nmemb"]) > 1:
						f.write(
							(
								'	if({0}K)\n'
								'		clReleaseMemObject({0}K);\n'.format(v.attrib["name"])
							)
						)


	# Print clReleaseKernel section
	def printFreeKernels(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
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
					'	if(program)\n'
					'		clReleaseProgram(program);\n'
					'	if(programBin)\n'
					'		free(programBin);\n'
					'	if(programFile)\n'
					'		fclose(programFile);\n'
				)
			)


	# Print clReleaseCommandQueue section
	def printFreeQueues(self):
		with open(self._targetFile, "a") as f:
			for k in self._xmlRoot:
				f.write(
					(
						'	if(queue{0})\n'
						'		clReleaseCommandQueue(queue{0});\n'.format(k.attrib["name"].title())
					)
				)


	# Print last part of code
	def printFooter(self):
		with open(self._targetFile, "a") as f:
			f.write(
				(
					'	if(context)\n'
					'		clReleaseContext(context);\n'
					'	if(devices)\n'
					'		free(devices);\n'
					'	if(platforms)\n'
					'		free(platforms);\n'
					'\n'
					'	return rv;\n'
					'}\n'
				)
			)
