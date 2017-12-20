Testing new ways of packing block data from Vlasiator. Testapp in
python & C for testing different variants. Tested by reading in double
precision blocks from vlsv file, and comparing error metrics after
compress/decompress cycle.


Planned variants:

1  Single precision (like now)
2  Single precision, scaling factor.
3  Half precision, scaling factor
4. ZFP https://github.com/LLNL/zfp
5. SZ https://github.com/disheng222/SZ

Scaling factors scale max value in block to max representable value of
fp format. This is to use as much of the exponent bits as
possible. Additionally, this value can be fine tune to preserve mass
on a block level, which for lower precisions can be important.


