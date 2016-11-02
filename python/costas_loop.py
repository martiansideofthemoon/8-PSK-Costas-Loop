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
    self.call = 0

  ##################################################
    # Blocks
  ##################################################

    self.prev_input = np.zeros(self.iter, dtype=np.float64)
    self.prev_output = np.zeros(self.iter, dtype=np.float64)
    self.prev_phase = np.zeros(self.iter, dtype=np.float64)

    self.costas8_sp_threshold_1 = costas8.sp_threshold()
    self.costas8_sp_threshold_0 = costas8.sp_threshold()
    self.k_factor = -5/samp_rate

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
    self.call += 1
    in0 = input_items[0]
    out = output_items[0]
    # <+signal processing here+>
    feedback = np.ones(in0.shape, dtype=np.complex64)
    on_first_mul = np.ones(in0.shape, dtype=np.complex64)
    op_thresh_imag = np.ones(in0.shape, dtype=np.float64)
    op_thresh_real = np.ones(in0.shape, dtype=np.float64)
    a = np.array([op_thresh_imag])
    b = np.array([op_thresh_real])
    in_iir = np.zeros(in0.shape, dtype=np.float64)
    out_iir = np.ones(in0.shape, dtype=np.float64)
    out_vco = np.ones(in0.shape, dtype=np.complex64)
    in0 = in0/math.sqrt(2)
    for i in xrange(0,self.iter):
      # Multiply input signal with feedback of that iteration
      on_first_mul = in0*feedback
      # Phase error detector
      real = on_first_mul.real
      imag = on_first_mul.imag
      self.costas8_sp_threshold_0.work(np.array([imag]), a)
      self.costas8_sp_threshold_1.work(np.array([real]), b)
      in_iir = np.arcsin(imag*b[0] - real*a[0])

      # IIR filter implementing (1.0001 - z)/(1 - z) (old style)
      # self.prev_input[i] contains last input value from previous in0 chunk
      in_iir_delay = np.concatenate([[self.prev_input[i]],in_iir[0:-1]])
      # Update this for next in0 chunk
      self.prev_input[i] = in_iir[-1]
      out_temp = in_iir*1.0001 - in_iir_delay
      # Workaround for adding y[n-1]
      out_temp[0] += self.prev_output[i]
      out_iir = np.cumsum(out_temp)
      self.prev_output[i] = out_iir[-1]

      # VCO implementation 1/(1 - z) (old style)
      out_iir[0] += self.prev_phase[i]
      in_vco = np.cumsum(out_iir)
      self.prev_phase[i] = in_vco[-1]
      real_part = np.cos(self.k_factor*in_vco)
      imag_part = np.sin(self.k_factor*in_vco)
      out_vco = real_part + 1j*imag_part
      feedback = out_vco

    if self.call % 1 == 0:
      s = np.angle([feedback[100]], deg=True)
      s2 = np.angle([in0[100]], deg=True)
      #print str(self.call) + ", " + str(np.average(s)) + ", " + str(np.average(s2))
      #import pdb
      #pdb.set_trace()
      pass

    out[:] = (on_first_mul)#[1:]

    return len(output_items[0])

