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
import math
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

    self.prev_output_iir = 0
    self.costas8_sp_threshold_1 = costas8.sp_threshold()
    self.costas8_sp_threshold_0 = costas8.sp_threshold()
    self.k_factor = -5.0/samp_rate
    self.set_history(2);     # For the filter block

  def sp_threshold(self, in0):
    output = 0
    if in0 <= math.cos(7*math.pi/8):
      output = -1
    elif in0 > math.cos(7*math.pi/8) and in0 <= math.cos(5*math.pi/8):
      output = -1/(2**0.5)
    elif in0 > math.cos(5*math.pi/8) and in0 <= math.cos(3*math.pi/8):
      output = 0
    elif in0 > math.cos(3*math.pi/8) and in0 <= math.cos(math.pi/8):
      output = 1/(2**0.5)
    elif in0 > math.cos(math.pi/8):
      output = 1
    return output

  def work(self, input_items, output_items):
    in0 = input_items[0]
    out = output_items[0]
    # <+signal processing here+>
    feedback = 1
    on_first_mul = np.ones(in0.shape, dtype=np.complex64)
    op_thresh_imag = np.ones(in0.shape, dtype=np.complex64)
    op_thresh_real = np.ones(in0.shape, dtype=np.complex64)
    in_iir = np.zeros(in0.shape, dtype=np.complex64)
    out_iir = np.ones(in0.shape, dtype=np.complex64)
    out_vco = np.ones(in0.shape, dtype=np.complex64)
    prev_output_iir = np.zeros(in0.shape, dtype=np.complex64)
    prev_output_iir[0] = self.prev_output_iir
    for i in xrange(1,self.iter):
      on_first_mul = in0*feedback
      real = on_first_mul.real
      imag = on_first_mul.imag
      #op_thresh_imag = self.sp_threshold(imag)
      #op_thresh_real = self.sp_threshold(real)
      self.costas8_sp_threshold_0.work(np.array([imag]), np.array([op_thresh_imag]))
      self.costas8_sp_threshold_1.work(np.array([real]), np.array([op_thresh_real]))
      in_iir = imag*op_thresh_real - real*op_thresh_imag
      in_iir2 = np.concatenate([[0],in_iir[0:-1]])
      out_iir = in_iir*1.001 - in_iir2 + prev_output_iir
      real_part = np.cos(self.k_factor*out_iir)
      imag_part = np.sin(self.k_factor*out_iir)
      out_vco = real_part + 1j*imag_part
      feedback = out_vco
      prev_output_iir = np.concatenate([[0],out_iir[0:-1]])
      if i == 1:
        self.prev_output_iir = out_iir[-1]
    out[:] = (on_first_mul)[1:]

    return len(output_items[0])

