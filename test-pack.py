import pytools as pt
import numpy as np
cellid=1001
blockid=100

f=pt.vlsvfile.VlsvReader("bulk.0000001.vlsv")
velspace = f.read_blocks(cellid)

for block in velspace[1]:
    
#block = velspace[1][blockid]
#    if np.max(block) < 1e-15:
 #       continue

    block_max=np.max(block)
    block_min=np.min(block)

    block_float=block.astype(np.float32)
    block_float2=(np.finfo(np.float32).max * (block / block_max)).astype(np.float32)
    block_half=(np.finfo(np.float16).max * (block / block_max)).astype(np.float16)

    block_float_d=block_float.astype(np.float64)
    block_float2_d=block_float2.astype(np.float64)/ np.finfo(np.float32).max * block_max
    block_half_d=block_half.astype(np.float64)/ np.finfo(np.float16).max * block_max
    


    rel_error_float=np.abs(block - block_float_d)/np.abs(block)
    rel_error_float2=np.abs(block - block_float2_d)/np.abs(block)
    rel_error_half=np.abs(block - block_half_d)/np.abs(block)



    print "--------------------------------------------------------------------------"
    print "block stats    avg, max, min:", np.average(block), np.max(block), np.min(block)
    print "Rel err float  avg, max, min:",  np.average(rel_error_float), np.max(rel_error_float), np.min(rel_error_float), np.median(rel_error_float)
    print "Rel err float2  avg, max, min:",  np.average(rel_error_float2), np.max(rel_error_float2), np.min(rel_error_float2), np.median(rel_error_float2)
    print "Rel err half  avg, max, min:",  np.average(rel_error_half), np.max(rel_error_half), np.min(rel_error_half), np.median(rel_error_half)


    





