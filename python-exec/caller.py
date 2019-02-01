#! /usr/bin/env python

class MyClass(object):
  def my_function(self):
    print 'This is MyClass.my_function'

print 'Running caller.py'
myclass = MyClass()
with open('callee.py') as stream:
  exec stream
  print 'Calling callee_function() from caller.py'
  callee_function()
print 'Done'
