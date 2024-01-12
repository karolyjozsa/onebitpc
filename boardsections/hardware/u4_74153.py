"""Simulate the 74153 IC"""

from typedefinitions import TTL

def multiplexer(
    data0: TTL,
    data1: TTL,
    data2: TTL,
    data3: TTL,
    enable_inv: TTL,
    select0: TTL,
    select1: TTL,
) -> TTL:
    # Output LOW if multiplexer not enabled
    if enable_inv.value:
        return TTL.L
    
    if ~select0 & ~select1:
        return data0
    
    if select0 & ~select1:
        return data1
    
    if ~select0 & select1:
        return data2
    
    if select0 & select1:
        return data3

    raise ValueError('This should never happen')