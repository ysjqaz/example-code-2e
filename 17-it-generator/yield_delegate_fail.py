""" 示例摘自 `Python: The Full Monty`__ —— A Tested Semantics for the
Python Programming Language

__ http://cs.brown.edu/~sk/Publications/Papers/Published/pmmwplck-python-full-monty/

「下面这段程序……似乎对 yield 的过程做了一个简单的抽象：」

引文：

Joe Gibbs Politz, Alejandro Martinez, Matthew Milano, Sumner Warren,
Daniel Patterson, Junsong Li, Anand Chitipothu, and Shriram Krishnamurthi.
2013. Python: the full monty. SIGPLAN Not. 48, 10 (October 2013), 217-232.
DOI=10.1145/2544173.2509536 http://doi.acm.org/10.1145/2544173.2509536
"""

# tag::YIELD_DELEGATE_FAIL[]
def f():
    def do_yield(n):
        yield n
    x = 0
    while True:
        x += 1
        do_yield(x)
# end::YIELD_DELEGATE_FAIL[]

if __name__ == '__main__':
    print('Invoking f() results in an infinite loop')
    f()
