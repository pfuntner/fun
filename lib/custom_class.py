class CustomClass:
  def __init__(self, data):
    print(f'My class name is {self.__class__.__name__!r}')
    self.data = data
