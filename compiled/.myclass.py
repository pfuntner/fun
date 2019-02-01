class MyClass(object):
  def __init__(self, *args, **kwds):
    assert not args, 'positions arguments are not expected'
    for (key, value) in kwds.items():
      setattr(self, key, value)

  def kaboom(safe):
    raise Exception('Take your exception!  Take it!!')
