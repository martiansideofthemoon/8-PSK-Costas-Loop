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
# -

import numpy as np
from gnuradio import gr
import costas8
from gnuradio import blocks
from gnuradio import filter

class costas_loop(gr.sync_block):
    """
    docstring for block costas_loop
    """
    def __init__(self, samp_rate, iter):
        gr.sync_block.__init__(self,
            name="costas_loop",
            in_sig=[np.complex64],
            out_sig=[np.complex64])
        self.samp_rate = samp_rate;
        self.iter = iter;

    ##################################################
        # Blocks
    ##################################################
        
        self.iir_filter_ffd_0 = filter.iir_filter_ffd(([1.0001,-1]), ([-1,1]), True)
        self.costas8_sp_threshold_1 = costas8.sp_threshold()
        self.costas8_sp_threshold_0 = costas8.sp_threshold()
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, -5, 1)
        self.set_history(2);         # For the filter block


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        loop_input_prev = np.ones(in0.shape)
        loop_input_curr = in0
        op_thresh_imag = np.ones(in0.shape)
        op_thresh_real = np.ones(in0.shape)
        out_iir = np.ones(in0.shape)
        out_vco = np.ones(in0.shape)
        for i in xrange(1,self.iter):
            on_first_mul = loop_input_curr*loop_input_prev
            real = on_first_mul.real
            imag = on_first_mul.imag
            import pdb
            pdb.set_trace()
            np.array([op_thresh_imag])[0][np.array([imag])[0] > -1] = 1
            self.costas8_sp_threshold_0.work(np.array([imag]), np.array([op_thresh_imag]))
            self.costas8_sp_threshold_1.work(real, op_thresh_real)
            in_iir = imag*op_thresh_real - real*op_thresh_imag
            self.iir_filter_ffd_0.work(in_iir, out_iir)
            self.blocks_vco_c_0.work(out_iir, out_vco)
            loop_input_prev = loop_input_curr
            loop_input_curr = out_vco

        out[:] = loop_input[self.iter]*loop_input[self.iter-1]
        
        return len(output_items[0])

