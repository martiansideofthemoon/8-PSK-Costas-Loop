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
from scipy import signal
import time
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
    self.samples = 0
    self.start_time = time.time()

  ##################################################
    # Blocks
  ##################################################

    self.prev_output = np.zeros(self.iter, dtype=np.float64)
    self.prev_output2 = np.zeros(self.iter, dtype=np.float64)
    self.prev_phase = np.zeros(self.iter, dtype=np.float64)

    self.costas8_sp_threshold_1 = costas8.sp_threshold()
    self.costas8_sp_threshold_0 = costas8.sp_threshold()
    self.k_factor = -5/samp_rate
    self.prev_in_iir = 0
    self.prev_out_iir = 0
    self.prev_in_vco = 0
    self.feedback = 0

  def work(self, input_items, output_items):
    in0 = input_items[0]
    out = output_items[0]
    self.call += 1
    self.samples += in0.shape[0]
    for i in range(0, in0.shape[0]):
      on_first_mul = in0[i]*self.feedback
      out[i] = on_first_mul
      real = on_first_mul.real
      imag = on_first_mul.imag
      a = self.costas8_sp_threshold_0.execute(imag)
      b = self.costas8_sp_threshold_1.execute(real)
      in_iir = np.arcsin(imag*b - real*a)
      out_iir = 1.0001*in_iir - self.prev_in_iir + self.prev_out_iir
      self.prev_in_iir = in_iir
      self.prev_out_iir = out_iir
      in_vco = out_iir + self.prev_in_vco
      self.prev_in_vco = in_vco
      real_part = np.cos(self.k_factor*in_vco)
      imag_part = np.sin(self.k_factor*in_vco)
      out_vco = real_part + 1j*imag_part
      self.feedback = out_vco
    print self.samples
    return len(output_items[0])
  # def work(self, input_items, output_items):
  #   self.call += 1
  #   in0 = input_items[0]
  #   out = output_items[0]
  #   self.samples += in0.shape[0]
  #   # import pdb
  #   # pdb.set_trace()
  #   # <+signal processing here+>
  #   feedback = np.ones(in0.shape, dtype=np.complex64)
  #   on_first_mul = np.ones(in0.shape, dtype=np.complex64)
  #   op_thresh_imag = np.ones(in0.shape, dtype=np.float64)
  #   op_thresh_real = np.ones(in0.shape, dtype=np.float64)
  #   a = np.array([op_thresh_imag])
  #   b = np.array([op_thresh_real])
  #   in_iir = np.zeros(in0.shape, dtype=np.float64)
  #   out_iir = np.ones(in0.shape, dtype=np.float64)
  #   out_iir2 = np.ones(in0.shape, dtype=np.float64)
  #   out_vco = np.ones(in0.shape, dtype=np.complex64)
  #   in0 = in0/math.sqrt(2)
  #   for i in xrange(0,self.iter):
  #     # Multiply input signal with feedback of that iteration
  #     on_first_mul = in0*feedback
  #     # Phase error detector
  #     real = on_first_mul.real
  #     imag = on_first_mul.imag
  #     self.costas8_sp_threshold_0.work(np.array([imag]), a)
  #     self.costas8_sp_threshold_1.work(np.array([real]), b)
  #     in_iir = np.arcsin(imag*b[0] - real*a[0])

  #     #inital = signal.lfiltic([1], [1, 0.99], [self.prev_output[i]])
  #     #out_iir, _ = signal.lfilter([1], [1, 0.99], in_iir, zi=inital)
  #     out_iir = in_iir

  #     inital = signal.lfiltic([1.0001,-1], [1, -1], [self.prev_output2[i]], [self.prev_output[i]])
  #     out_iir2, _ = signal.lfilter([1.0001,-1], [1, -1], out_iir, zi=inital)
  #     self.prev_output2[i] = out_iir2[-1]
  #     self.prev_output[i] = out_iir[-1]

  #     # VCO implementation 1/(1 - z) (old style)
  #     inital = signal.lfiltic([1], [1, -1], [self.prev_phase[i]])
  #     in_vco, _ = signal.lfilter([1], [1, -1], out_iir2, zi=inital)
  #     self.prev_phase[i] = in_vco[-1]

  #     real_part = np.cos(self.k_factor*in_vco)
  #     imag_part = np.sin(self.k_factor*in_vco)
  #     out_vco = real_part + 1j*imag_part
  #     feedback = out_vco

  #     if (i == 1):
  #       append = str(self.samples) + ", " + str(in_iir[-1]) + "\n"
  #       with open("/home/kalpesh/Academics/EE340_Project/gr-costas8/python/data2_samples_error_iter1.csv", "a") as myfile:
  #         pass
  #         #myfile.write(append)
  #     if (i == 50):
  #       append2 = str(self.samples) + ", " + str(in_iir[-1]) + "\n"
  #       with open("/home/kalpesh/Academics/EE340_Project/gr-costas8/python/data2_samples_error_iter50.csv", "a") as myfile:
  #         pass
  #         #myfile.write(append2)
  #     if (i == 98):
  #       append3 = str(self.samples) + ", " + str(in_iir[-1]) + "\n"
  #       with open("/home/kalpesh/Academics/EE340_Project/gr-costas8/python/data2_samples_error_iter98.csv", "a") as myfile:
  #         pass
  #         #myfile.write(append3)

  #     if (self.call == 1):
  #       append = str(i) + ", " + str(in_iir[-1]) + "\n"
  #       with open("/home/kalpesh/Academics/EE340_Project/gr-costas8/python/data2_iter_vs_error_sample1.csv", "a") as myfile:
  #         pass
  #         myfile.write(append)
  #     if (self.call == 150):
  #       append2 = str(i) + ", " + str(in_iir[-1]) + "\n"
  #       with open("/home/kalpesh/Academics/EE340_Project/gr-costas8/python/data2_iter_vs_error_sample150.csv", "a") as myfile:
  #         pass
  #         myfile.write(append2)
  #     if (self.call == 300):
  #       append3 = str(i) + ", " + str(in_iir[-1]) + "\n"
  #       with open("/home/kalpesh/Academics/EE340_Project/gr-costas8/python/data2_iter_vs_error_sample300.csv", "a") as myfile:
  #         pass
  #         myfile.write(append3)


  #   #print self.k_factor*self.prev_phase[-1]
  #   #print self.prev_phase[180:]
  #   self.prev_phase = np.round(self.prev_phase % (2*np.pi/self.k_factor), 3)
  #   #print self.k_factor*self.prev_phase[-1]

  #   if self.call % 1 == 0:
  #     s = np.angle([feedback[100]], deg=True)
  #     s2 = np.angle([in0[100]], deg=True)
  #     #print self.samples
  #     print str(self.call) + ", " + str(in_iir[-1])
  #     #print time.time() - self.start_time
  #     #print str(mean) + ", " + str(np.std(self.prev_phase[180:]))
  #     #print str(self.call) + ", " + str(np.average(s)) + ", " + str(np.average(s2))
  #     #import pdb
  #     #pdb.set_trace()
  #     pass

  #   out[:] = (on_first_mul)#[1:]

  #   return len(output_items[0])


