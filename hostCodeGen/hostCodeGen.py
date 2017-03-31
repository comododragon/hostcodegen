#!/usr/bin/env python3

# #############################################################################################
# # Host Code Generator for Kernel Execution                                                  #
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


import sys
from codeemitter import CodeEmitter


if "__main__" == __name__:
	if len(sys.argv) != 3:
		sys.stderr.write("Usage: hostCodeGen KERNELSXML TARGETFILE KERNELSXML\n");
		sys.stderr.write("\tKERNELSXML\tXML with descriptions of kernels\n");
		sys.stderr.write("\tTARGETFILE\tOutput source code filename\n");
		exit(1)

	ce = CodeEmitter(sys.argv[1], sys.argv[2])

	print("Printing header...")
	ce.printHeader()

	print("Printing queue declarations...")
	ce.printQueueDeclarations()

	print("Printing program declarations...")
	ce.printProgramDeclarations()

	print("Printing kernel declarations...")
	ce.printKernelDeclarations()

	print("Printing last declarations...")
	ce.printLastDeclarations()
	ce.printSeparator()

	print("Printing variables declaration...")
	ce.printVariablesDeclaration()
	ce.printSeparator()

	print("Printing getPlatformIDs section...")
	ce.printGetPlatformIDs()
	ce.printSeparator()

	print("Printing getDevicesIDs section...")
	ce.printGetDevicesIDs()
	ce.printSeparator()

	print("Printing createContext section...")
	ce.printCreateContext()
	ce.printSeparator()

	print("Printing createCommandQueue sections...")
	ce.printCreateCommandQueues()
	ce.printSeparator()

	print("Printing createAndBuildProgram sections...")
	ce.printCreateAndBuildProgram()
	ce.printSeparator()

	print("Printing createKernel sections...")
	ce.printCreateKernels()
	ce.printSeparator()

	print("Printing createBuffer sections...")
	ce.printCreateBuffers()
	ce.printSeparator()

	print("Printing setKernelArgs sections...")
	ce.printSetKernelsArgs()
	ce.printSeparator()

	print("Printing enqueueKernel sections...")
	ce.printEnqueueKernel()
	ce.printSeparator()

	print("Printing enqueueReadBuffer sections...")
	ce.printEnqueueReadBuffer()
	ce.printSeparator()

	print("Printing validation sections...")
	ce.printValidation()
	ce.printSeparator()

	print("Printing error goto label...")
	ce.printErrorLabel()
	ce.printSeparator()

	print("Printing buffers deallocation sections...")
	ce.printFreeBuffers()
	ce.printSeparator()

	print("Printing kernels deallocation sections...")
	ce.printFreeKernels()
	ce.printSeparator()

	print("Printing program deallocation section...")
	ce.printFreeProgram()
	ce.printSeparator()

	print("Printing queues deallocation sections...")
	ce.printFreeQueues()
	ce.printSeparator()

	print("Printing footer...")
	ce.printFooter()
