import pytools as pt
import numpy as np
import zfpmodule as zfp



f=pt.vlsvfile.VlsvReader("bulk.0000001.vlsv")
cells = np.sort(f.read_variable("CellID"))


rates=[8, 16, 24, 32]

print "#cellid blocks sum float float-scaled half-scaled zfp-8 zfp-16 zfp-24 zfp-32"
for cellid in cells:
    
    velspace = f.read_blocks(cellid)
    if len(velspace) == 0:
        continue

    tot_error_float=np.empty(0, dtype = np.float64)
    tot_error_float2=np.empty(0, dtype = np.float64)
    tot_error_half2=np.empty(0, dtype = np.float64)
    tot_error_zfp =  {}
    
    for rate in rates:
        tot_error_zfp[rate] = np.empty(0, dtype = np.float64)

    
    cell_sum = 0
    for block in velspace[1]:
        block_max=np.max(block)
        block_min=np.min(block)
        block_sum=np.sum(block)
        cell_sum = cell_sum + block_sum
        
        block_float=block.astype(np.float32)
        block_float2=(np.finfo(np.float32).max * (block / block_max)).astype(np.float32)
        block_half2=(np.finfo(np.float16).max * (block / block_max)).astype(np.float16)

        block_float_d=block_float.astype(np.float64)
        block_float2_d=block_float2.astype(np.float64)/ np.finfo(np.float32).max * block_max
        block_half2_d=block_half2.astype(np.float64)/ np.finfo(np.float16).max * block_max

        for rate in rates:
            block_zfp_d = np.empty(64, dtype=np.float64)
            zfp.compress_block(block, block_zfp_d, rate)
            tot_error_zfp[rate] = np.append(tot_error_zfp[rate], np.abs(block - block_zfp_d))            

        tot_error_float = np.append(tot_error_float, np.abs(block - block_float_d))
        tot_error_float2 = np.append(tot_error_float2, np.abs(block - block_float2_d))
        tot_error_half2 = np.append(tot_error_half2, np.abs(block - block_half2_d))


    print cellid, len(velspace[1]), cell_sum, \
        np.median(tot_error_float), \
        np.median(tot_error_float2), \
        np.median(tot_error_half2), \
        np.median(tot_error_zfp[8]), \
        np.median(tot_error_zfp[16]), \
        np.median(tot_error_zfp[24]), \
        np.median(tot_error_zfp[32])

    

    # print "Tot err float  avg, max, min, median:",  np.average(tot_error_float), np.max(tot_error_float), np.min(tot_error_float), np.median(tot_error_float)
    # print "Tot err float-scaled 32  avg, max, min, median:",  np.average(tot_error_float2), np.max(tot_error_float2), np.min(tot_error_float2), np.median(tot_error_float2)
    # print "Tot err half-scaled 16  avg, max, min, median:",  np.average(tot_error_half2), np.max(tot_error_half2), np.min(tot_error_half2), np.median(tot_error_half2)
    # for rate in rates:
    #     print "Tot err zfp",rate,"  avg, max, min, median:",  np.average(tot_error_zfp[rate]), np.max(tot_error_zfp[rate]), np.min(tot_error_zfp[rate]), np.median(tot_error_zfp[rate])










