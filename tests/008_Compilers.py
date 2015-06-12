from __future__ import print_function
from TestBase   import TestBase
from util       import run_cmd, capture

class Compilers(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def description(self):
    return "Check compilers:"

  def error(self):
    print(self.error_message)

  def execute(self):
      compilers=["gcc","g++","gfortran","icc","icpc","ifort","mpicc","mpicxx","mpif90"]
      
      Flag=True

      for compiler1 in compilers:
        typecmd="type %s" %compiler1 
        output=capture(typecmd)
#       print(output)
        if "not found" in output:
          Flag=False
	  self.error_message+="        Error: Compiler %s is not available now!\n" %compiler1
      return Flag     

  def help(self):
      print("        Please check your $PATH again, compilers are missing.\n",
     	    "       If you unload the compilers on purpose, please ignore this test.\n")
  def name(self):
      return "Check compilers"

