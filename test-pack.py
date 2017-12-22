import pytools as pt
import numpy as np
import zfpmodule as zfp



f=pt.vlsvfile.VlsvReader("bulk.0000001.vlsv")
cells = np.sort(f.read_variable("CellID"))


rates=[8, 16, 24, 32]

print "#cellid blocks sum float float2 half2 zfp-8 zfp-16 zfp-24 zfp-32"
for cellid in cells:
    
    velspace = f.read_blocks(cellid)
    if len(velspace) == 0:
        continue
    block_zfp_d =  {}
    rms_zfp={}
    
    for rate in rates:
        rms_zfp[rate] = 0.0
        block_zfp_d[rate] = np.empty(64, dtype=np.float64)
        
    cell_sum = 0
    vcells_counted=0
    min_val=1e-20
    rms_float = 0.0
    rms_float2 = 0.0
    rms_half2 = 0.0
    
    for block in velspace[1]:
        block_max=np.max(block)
        block_min=np.min(block)
        block_sum=np.sum(block)
        cell_sum = cell_sum + block_sum

        #compress - decompress by casting, with or without some scaling
        block_float=block.astype(np.float32)
        block_float2=(np.finfo(np.float32).max * (block / block_max)).astype(np.float32)
        block_half2=(np.finfo(np.float16).max * (block / block_max)).astype(np.float16)
        block_float_d=block_float.astype(np.float64)
        block_float2_d=block_float2.astype(np.float64)/ np.finfo(np.float32).max * block_max
        block_half2_d=block_half2.astype(np.float64)/ np.finfo(np.float16).max * block_max

        #compress  - decompress with ZFP
        for rate in rates:
            block_zfp_d[rate] = np.empty(64, dtype=np.float64)
            zfp.compress_block(block, block_zfp_d[rate], rate)
            
        #compute root mean squares
        for i in range(64):
            if block[i] > min_val:
                vcells_counted = vcells_counted + 1
                rms_float = rms_float + ((block[i] - block_float_d[i])/block[i])**2
                rms_float2 = rms_float2 + ((block[i] - block_float2_d[i])/block[i])**2
                rms_half2 = rms_half2 + ((block[i] - block_half2_d[i])/block[i])**2

        for rate in rates:
            for i in range(64):
                if block[i] > min_val:
                    rms_zfp[rate] = rms_zfp[rate] + ((block[i] - block_zfp_d[rate][i])/block[i])**2

                    
 
    print cellid, len(velspace[1]), cell_sum, \
        np.sqrt(rms_float/vcells_counted), \
        np.sqrt(rms_float2/vcells_counted), \
        np.sqrt(rms_half2/vcells_counted), \
        np.sqrt(rms_zfp[8]/vcells_counted), \
        np.sqrt(rms_zfp[16]/vcells_counted), \
        np.sqrt(rms_zfp[24]/vcells_counted), \
        np.sqrt(rms_zfp[32]/vcells_counted)
    










