from get_median import MedianKeeper
from numpy import median, random
def test():
    def myTest(testValues):
        m = MedianKeeper()
        errors = 0
        for i,value in enumerate(testValues):
            m.add_element(value)
            my_median = m.get_median()
            np_median = median(testValues[:i+1])
            try:
                assert(my_median == np_median)
            except:
                errors +=1
        print "The first ten values of the test input: {0} ...".format(testValues[:10])
        print "Complete With {0} Errors\n".format(errors), "-"*30
    test_0 = [4,5,4,5]
    test_1 = range(100)
    test_2 = random.randint(-100, 100, 1000)

    myTest(test_0)
    myTest(test_1)
    myTest(test_2)

if __name__ == "__main__":
    test()
