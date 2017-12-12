Testing new ways of packing block data. Testapp in python/analysator/C
for testing different variants. Tested by reading in double precision
blocks from vlsv file, and comparing error metrics after compress/decompress
cycle.


Planned variants:

1 Single precision (like now)

2 Single precision, scaling factor.

3 Half precision, scaling factor

4 Variable precision (mantissa, exponent) with no sign-bit,  4 bytes: (24,8), 2 bytes: (10,6), 1 byte: (3,5)  scaling factor

5 Mix: Use different precision depending on how max value in block (tail vs. peaks). In vlasiator we could have three vectors for (8), 4, 2, 1 byte cell values



Scaling factors scale max value in block to max representable value of
fp format. This is to use as much of the exponent bits as
possible. Additionally, this value can be fine tune to preserve mass
on a block level(!), which for lower precisions can be important.


