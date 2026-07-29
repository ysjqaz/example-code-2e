#!/usr/bin/env python

################ Lispy：Python 3.9 中的 Scheme 解释器

## (c) Peter Norvig, 2010-18；参见 http://norvig.com/lispy.html
## 为《流畅的 Python（第二版）》（O'Reilly, 2021）做了少量修改
## 由 Luciano Ramalho 编写，添加了类型提示（type hint）和模式匹配（pattern matching）。


################ 导入与类型

import math
import operator as op
from collections import ChainMap
from itertools import chain
from typing import Any, Union, NoReturn

Symbol = str
Atom = Union[float, int, Symbol]
Expression = Union[Atom, list]


################ 解析：parse、tokenize 和 read_from_tokens

def parse(program: str) -> Expression:
    "从字符串中读取一个 Scheme 表达式。"
    return read_from_tokens(tokenize(program))

def tokenize(s: str) -> list[str]:
    "将字符串转换为词法单元（token）列表。"
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def read_from_tokens(tokens: list[str]) -> Expression:
    "从词法单元序列中读取一个表达式。"
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        exp = []
        while tokens[0] != ')':
            exp.append(read_from_tokens(tokens))
        tokens.pop(0)  # 丢弃 ')'
        return exp
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return parse_atom(token)

def parse_atom(token: str) -> Atom:
    "数字转换为数字；其他所有词法单元都是符号。"
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


################ 全局环境

class Environment(ChainMap[Symbol, Any]):
    "一个允许就地修改元素的 ChainMap。"

    def change(self, key: Symbol, value: Any) -> None:
        "找到 key 定义的位置并在那里修改值。"
        for map in self.maps:
            if key in map:
                map[key] = value  # type: ignore[index]
                return
        raise KeyError(key)


def standard_env() -> Environment:
    "一个包含部分 Scheme 标准过程的环境。"
    env = Environment()
    env.update(vars(math))   # sin、cos、sqrt、pi 等……
    env.update({
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            'quotient': op.floordiv,
            '>': op.gt,
            '<': op.lt,
            '>=': op.ge,
            '<=': op.le,
            '=': op.eq,
            'abs': abs,
            'append': lambda *args: list(chain(*args)),
            'apply': lambda proc, args: proc(*args),
            'begin': lambda *x: x[-1],
            'car': lambda x: x[0],
            'cdr': lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'display': lambda x: print(lispstr(x)),
            'eq?': op.is_,
            'equal?': op.eq,
            'filter': lambda *args: list(filter(*args)),
            'length': len,
            'list': lambda *x: list(x),
            'list?': lambda x: isinstance(x, list),
            'map': lambda *args: list(map(*args)),
            'max': max,
            'min': min,
            'not': op.not_,
            'null?': lambda x: x == [],
            'number?': lambda x: isinstance(x, (int, float)),
            'procedure?': callable,
            'round': round,
            'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


################ 交互：REPL

def repl(prompt: str = 'lis.py> ') -> NoReturn:
    "一个「提示—读取—求值—打印」循环。"
    global_env = Environment({}, standard_env())
    while True:
        ast = parse(input(prompt))
        val = evaluate(ast, global_env)
        if val is not None:
            print(lispstr(val))

def lispstr(exp: object) -> str:
    "将 Python 对象转换回 Lisp 可读的字符串。"
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)


################ 求值器

def evaluate(exp: Expression, env: Environment) -> Any:
    "在环境中求值一个表达式。"
    if isinstance(exp, Symbol):      # 变量引用
        return env[exp]
    elif not isinstance(exp, list):  # 常量字面量
        return exp
    elif exp[0] == 'quote':          # (quote exp)
        (_, x) = exp
        return x
    elif exp[0] == 'if':             # (if test conseq alt)
        (_, test, consequence, alternative) = exp
        if evaluate(test, env):
            return evaluate(consequence, env)
        else:
            return evaluate(alternative, env)
    elif exp[0] == 'lambda':         # (lambda (parm…) body…)
        (_, parms, *body) = exp
        if not isinstance(parms, list):
            raise SyntaxError(lispstr(exp))
        return Procedure(parms, body, env)
    elif exp[0] == 'define':
        (_, name_exp, *rest) = exp
        if isinstance(name_exp, Symbol):  # (define name exp)
            value_exp = rest[0]
            env[name_exp] = evaluate(value_exp, env)
        else:  # (define (name parm…) body…)
            name, *parms = name_exp
            env[name] = Procedure(parms, rest, env)
    elif exp[0] == 'set!':
        (_, var, value_exp) = exp
        env.change(var, evaluate(value_exp, env))
    else:                          # (proc arg…)
        (func_exp, *args) = exp
        proc = evaluate(func_exp, env)
        args = [evaluate(arg, env) for arg in args]
        return proc(*args)


class Procedure:
    "一个用户定义的 Scheme 过程。"

    def __init__(
        self, parms: list[Symbol], body: list[Expression], env: Environment
    ):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args: Expression) -> Any:
        local_env = dict(zip(self.parms, args))
        env = Environment(local_env, self.env)
        for exp in self.body:
            result = evaluate(exp, env)
        return result


################ 命令行接口

def run(source: str) -> Any:
    global_env = Environment({}, standard_env())
    tokens = tokenize(source)
    while tokens:
        exp = read_from_tokens(tokens)
        result = evaluate(exp, global_env)
    return result

def main(args: list[str]) -> None:
    if len(args) == 1:
        with open(args[0]) as fp:
            run(fp.read())
    else:
        repl()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
