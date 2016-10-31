#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
from sp_threshold import sp_threshold
from gnuradio import blocks
from gnuradio import filter

class costas_loop(gr.sync_block):
    """
    docstring for block costas_loop
    """
    def __init__(self, sample_rate, iter):
        gr.sync_block.__init__(self,
            name="costas_loop",
            in_sig=[<+numpy.float+>],
            out_sig=[<+numpy.float+>])
        self.samp_rate = samp_rate;
        self.iter = iter;

    ##################################################
        # Blocks
    ##################################################
        
    self.iir_filter_ffd_0 = filter.iir_filter_ffd(([1.0001,-1]), ([-1,1]), True)
    self.costas8_sp_threshold_1 = costas8.sp_threshold()
    self.costas8_sp_threshold_0 = costas8.sp_threshold()
    self.blocks_vco_c_0 = blocks.vco_c(samp_rate, -5, 1)
                


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        loop_input[0] = 1
        loop_input[1] = in0
        for i in xrange(1,self.iter):
            on_first_mul = loop_input[i].*loop_input[i-1]
            real = on_first_mul.real
            imag = on_first_mul.imag
            
        out[:] = in0
        return len(output_items[0])

