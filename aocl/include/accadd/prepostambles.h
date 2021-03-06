/* ********************************************************************************************* */
/* * Example of pre/postamble functions for filling some input and output data                 * */
/* * Author: André Bannwart Perina                                                             * */
/* ********************************************************************************************* */
/* * Copyright (c) 2017 André B. Perina                                                        * */
/* *                                                                                           * */
/* * Permission is hereby granted, free of charge, to any person obtaining a copy of this      * */
/* * software and associated documentation files (the "Software"), to deal in the Software     * */
/* * without restriction, including without limitation the rights to use, copy, modify,        * */
/* * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to        * */
/* * permit persons to whom the Software is furnished to do so, subject to the following       * */
/* * conditions:                                                                               * */
/* *                                                                                           * */
/* * The above copyright notice and this permission notice shall be included in all copies     * */
/* * or substantial portions of the Software.                                                  * */
/* *                                                                                           * */
/* * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,       * */
/* * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR  * */
/* * PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE * */
/* * FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR      * */
/* * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER    * */
/* * DEALINGS IN THE SOFTWARE.                                                                 * */
/* ********************************************************************************************* */

int gCounter;
float *gRedundantUnnecessaryDynamicExampleVar = NULL;\

#define PREAMBLE(a, aSz, b, bSz, c, cSz, cC, cCSz, d, dSz, dC, dCSz) {\
	int _i;\
	float _example[10] = {57, 54, 51, 48, 45, 42, 39, 36, 33, 30};\
\
	gRedundantUnnecessaryDynamicExampleVar = malloc(10 * sizeof(float));\
	memcpy(gRedundantUnnecessaryDynamicExampleVar, _example, 10 * sizeof(float));\
\
	gCounter = 0;\
\
	for(_i = 0; _i < bSz; _i++)\
		b[_i] = _i;\
	for(_i = 0; _i < dSz; _i++)\
		d[_i] = 0;\
	for(_i = 0; _i < dCSz; _i++)\
		dC[_i] = gRedundantUnnecessaryDynamicExampleVar[_i];\
}

#define LOOPPREAMBLE(a, aSz, b, bSz, c, cSz, cC, cCSz, d, dSz, dC, dCSz, loopFlag) {\
	int _i;\
	for(_i = 0; _i < dSz; _i++)\
		d[_i]++;\
}

#define LOOPPOSTAMBLE(a, aSz, b, bSz, c, cSz, cC, cCSz, d, dSz, dC, dCSz, loopFlag) {\
	int _i;\
	for(_i = 0; _i < bSz; _i++)\
		b[_i] = c[_i];\
\
	gCounter++;\
	loopFlag = (gCounter < 3);\
}

#define POSTAMBLE(a, aSz, b, bSz, c, cSz, cC, cCSz, d, dSz, dC, dCSz) {\
}

#define CLEANUP(a, aSz, b, bSz, c, cSz, cC, cCSz, d, dSz, dC, dCSz) {\
	if(gRedundantUnnecessaryDynamicExampleVar)\
		free(gRedundantUnnecessaryDynamicExampleVar);\
}
