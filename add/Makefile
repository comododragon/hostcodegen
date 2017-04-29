# #############################################################################################
# # Makefile                                                                                  #
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

GENERALFLAGS=-fPIC -DCOMMON_COLOURED_PRINTS -Iinclude/common
AOCLFLAGS=`aocl compile-config` `aocl link-config`

emu/emulate: include/common/common.h src/host.c src/preamble.c emu/program.aocx
	mkdir -p emu
	$(CC) src/host.c src/preamble.c -o emu/emulate $(GENERALFLAGS) $(AOCLFLAGS)

emu/program.aocx: src/device.cl
	mkdir -p emu
	aoc -v -march=emulator -g --board s5phq_a7 src/device.cl -o emu/program.aocx

bin/execute: include/common/common.h src/host.c src/preamble.c bin/program.aocx
	mkdir -p bin
	$(CC) src/host.c src/preamble.c -o bin/execute $(GENERALFLAGS) $(AOCLFLAGS)

bin/program.aocx: src/device.cl
	mkdir -p bin
	aoc -v --board s5phq_a7 src/device.cl -o bin/program.aocx

clean:
	rm -r bin emu
