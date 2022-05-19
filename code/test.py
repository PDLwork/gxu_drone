import numpy

store_state = numpy.zeros((1000, 3, 32, 32))
a = numpy.ones((3,32,32))
store_state[0] = a
print(store_state)