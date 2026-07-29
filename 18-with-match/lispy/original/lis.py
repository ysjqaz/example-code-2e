################ Lispy：Python 3.3+ 中的 Scheme 解释器

## (c) Peter Norvig, 2010-18；参见 http://norvig.com/lispy.html

################ 导入与类型

import math
import operator as op
from collections import ChainMap as Environment

Symbol = str          # Lisp 的 Symbol 用 Python 的 str 实现
List   = list         # Lisp 的 List   用 Python 的 list 实现
Number = (int, float) # Lisp 的 Number 用 Python 的 int 或 float 实现

class Procedure(object):
    "一个用户定义的 Scheme 过程。"
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        env =  Environment(dict(zip(self.parms, args)), self.env)
        return eval(self.body, env)

################ 全局环境

def standard_env():
    "一个包含部分 Scheme 标准过程的环境。"
    env = {}
    env.update(vars(math)) # sin、cos、sqrt、pi 等……
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv, 
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
        'abs':     abs,
        'append':  op.add,  
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:], 
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_, 
        'equal?':  op.eq, 
        'length':  len, 
        'list':    lambda *x: list(x), 
        'list?':   lambda x: isinstance(x,list), 
        'map':     lambda *args: list(map(*args)),
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [], 
        'number?': lambda x: isinstance(x, Number),   
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

################ 解析：parse、tokenize 和 read_from_tokens

def parse(program):
    "从字符串中读取一个 Scheme 表达式。"
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "将字符串转换为词法单元（token）列表。"
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "从词法单元序列中读取一个表达式。"
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # 弹出 ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "数字转换为数字；其他所有词法单元都是符号。"
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

################ 交互：REPL

def repl(prompt='lis.py> '):
    "一个「提示—读取—求值—打印」循环。"
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))

def lispstr(exp):
    "将 Python 对象转换回 Lisp 可读的字符串。"
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')' 
    else:
        return str(exp)

################ eval

def eval(x, env=global_env):
    "在环境中求值一个表达式。"
    if isinstance(x, Symbol):      # 变量引用
        return env[x]
    elif not isinstance(x, List):  # 常量字面量
        return x
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                          # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)
