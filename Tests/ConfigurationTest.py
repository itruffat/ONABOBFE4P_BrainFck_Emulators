from Tests.Test import Emulation_Test

# sample case
test0 = Emulation_Test("+++++++>>>>>>>+++++++")
test0.run()
assert(test0.data == [7,0,0,0,0,0,0,7])

# Normal data run
test1 = Emulation_Test("+>++>+++>++++")
test1.run()
assert(test1.data == [1,2,3,4,0,0,0,0])

# Unwanted data underflow
test2 = Emulation_Test("+>++>+++>++++>-")
try:
    test2.run()
except AssertionError as e:
    assert(test2.data == [1,2,3,4,0,0,0,0])
except Exception as e:
    raise e

# Data underflow
test3 = Emulation_Test("+>++>+++>++++>-", allow_data_underflow= True)
test3.run()
assert(test3.data == [1,2,3,4,7,0,0,0])

# Negative data
test4 = Emulation_Test("+>++>+++>++++>-", use_negatives=True)
test4.run()
assert(test4.data == [1,2,3,4,-1,0,0,0])

# Negative Data (with underflow enabled)
test5 = Emulation_Test("+>++>+++>++++>-", use_negatives=True, allow_data_underflow= True)
test5.run()
assert(test5.data == [1,2,3,4,-1,0,0,0])

# Unwanted data underflow (with negative data)
test6 = Emulation_Test("+>++>+++>++++>---------", use_negatives=True)
try:
    test6.run()
except AssertionError as e:
    assert(test6.data == [1,2,3,4,-7,0,0,0])
except Exception as e:
    raise e

# Negative Data underflow
test7 = Emulation_Test("+>++>+++>++++>---------", use_negatives=True, allow_data_underflow= True)
test7.run()
assert(test7.data == [1,2,3,4,6,0,0,0])

# Unwanted data overflow
test8 = Emulation_Test("+>++>+++>++++>++++++++")
try:
    test8.run()
except AssertionError as e:
    assert(test8.data == [1,2,3,4,7,0,0,0])
except Exception as e:
    raise e

# Unwanted data overflow (with negatives)
test9 = Emulation_Test("+>++>+++>++++>++++++++", use_negatives=True)
try:
    test9.run()
except AssertionError as e:
    assert(test9.data == [1,2,3,4,7,0,0,0])
except Exception as e:
    raise e

# Data overflow
test10 = Emulation_Test("+>++>+++>++++>+++++++++", allow_data_overflow=True)
test10.run()
assert(test10.data == [1,2,3,4,1,0,0,0])

# Data overflow (with negatives)
test11 = Emulation_Test("+>++>+++>++++>+++++++++", use_negatives=True, allow_data_overflow=True)
test11.run()
assert(test11.data == [1,2,3,4,-6,0,0,0])

# Normal pointer run
test12 = Emulation_Test("+>++>+++>++++>++++>+++>++>+")
test12.run()
assert(test12.data == [1,2,3,4,4,3,2,1] and test12.data_pointer == 7)

# Unwanted Pointer overflow
test13 = Emulation_Test("+>++>+++>++++>++++>+++>++>+>")
try:
    test13.run()
except AssertionError as e:
    assert(test13.data == [1,2,3,4,4,3,2,1] and test13.data_pointer == 7)
except Exception as e:
    raise e

# Pointer overflow
test14 = Emulation_Test("+>++>+++>++++>++++>+++>++>+>-", allow_pointer_overflow=True)
test14.run()
assert(test14.data == [0,2,3,4,4,3,2,1] and test14.data_pointer == 0)

# Unwanted Pointer underflow
test15 = Emulation_Test("+>++>+++>++++>++++>+++>++>+<<<<<<<<")
try:
    test15.run()
except AssertionError as e:
    assert(test15.data == [1,2,3,4,4,3,2,1] and test15.data_pointer == 0)
except Exception as e:
    raise e

# Pointer underflow
test16 = Emulation_Test("+>++>+++>++++>++++>+++>++>+<<<<<<<<-", allow_pointer_underflow= True)
test16.run()
assert(test16.data == [1,2,3,4,4,3,2,0] and test16.data_pointer == 7)