# from sympy.abc import _clash1, _clash2, _clash # dont impport clashes
import logging
import re as resub

#try :
#    from exercises.questiontypes.safe_run import safe_run
#except:
#    pass
import sympy
from sympy import *
from sympy.core.sympify import SympifyError
from sympy.physics.quantum.operatorordering import normal_ordered_form 
from sympy.physics.quantum.boson import BosonOp, BosonFockKet, BosonFockBra ;
from sympy.physics.quantum import TensorProduct
from sympy.physics.quantum import Dagger, qapply 
from fockspace import *
logger = logging.getLogger(__name__)



logger = logging.getLogger(__name__)

ns = {}

class com(sympy.Function):
    nargs = 2
    @classmethod
    def eval(cls, x, y ):
        return x*y - y*x

class no(sympy.Function):
    nargs = 1
    @classmethod
    def eval(cls, x ):
        xnew = normal_ordered_form( expand( qapply( x ) ), independent=True );
        while not xnew == x :
            x = xnew ;
            xnew = normal_ordered_form( expand( qapply(  x ) ) , independent=True );
        return xnew


#
# Future-protect source by hiding connection to sympy.quantum
#
ns.update(
    {
        "FiniteBosonFockSpace" : FiniteBosonFockSpace,
        "tp" : TensorProduct,   
        "qapply": qapply,
        "bket" : BosonFockKet,
        "bbra" : BosonFockBra,
        "boson" : BosonOp,
        "dboson" : lambda x: Dagger( BosonOp(x) ),
        "var" : Symbol,
        "dagger" : Dagger,
        "com": com,
        "no": no,
        "zeta": zeta,
        "N": N,
        "Q": Q,
        "beta": beta,
        "S": S,
        "gamma": gamma,
        "ff": Symbol("ff"),
        "FF": Symbol("FF"),
    }
)


lambdifymodules = ["numpy", {"cot": lambda x: 1.0 / numpy.tan(x)}]



#class quantumUnitError(Exception):
#    def __init__(self, value):
#        self.value = value
#
#    def __str__(self):
#        return str(self.value)
#

def asciiToSympy(expression):
    dict = {
        "^": "**",
        #        '_': '',
        #        '.': '',
        #        '[': '',
        #        ']': ''
    }
    result = expression;
    result = resub.sub(r"(?<=[\w)])\s+(?=[(\w])", r" * ", expression)
    result = resub.sub(r"(\W*[0-9]+)([A-Za-z]+)", r"\1 * \2", result)
    result = resub.sub(r"([a-zA-Z0-9\(\)])\)\(([a-zA-Z0-9\(\)])", r"\1)*(\2", result)
    for old, new in dict.items():
        result = result.replace(old, new)
    return result

def b(s) :
    return BosonOp(s);

def bd(s) :
    return Dagger( BosonOp( s) )






def qm_compare(expression1, expression2,global_text):  # {{{
    # Do some initial formatting
    response = {}
    print(f"QUANTUM_INTERNAL GLOBAL_TEXT = {global_text}")
    p = ";\n".join( [ item.strip() for item in global_text.split(";") ] )
    try:
        ns.update( globals() )
        exec( p , ns )
        print(f" EXPRESSION1 = {expression1}")
        print(f" EXPRESSION2 = {expression2}")
        sexpression1 =  asciiToSympy(expression1) 
        sexpression2 =  asciiToSympy(expression2) 
        print(f" SEXPRESSION1 = {sexpression1}")
        print(f" SEXPRESSION2 = {sexpression2}")
        sympy1 = no( qapply(  sympify(sexpression1, ns) ) )
        sympy2 = no( qapply( sympify(sexpression2, ns) ) )
        print("sympy1 = ",  sympy1)
        print("sympy2 = ",  sympy2)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Expression 1: " + str(sympy1))
            logger.debug("Expression 2: " + str(sympy2))
        diffy = expand( simplify(sympy1 - sympy2) )
        if diffy == 0:
            response["correct"] = True
        else:
            response["correct"] = False
            response["debug"] = ". Diff reduces to " + str(diffy)
    except SympifyError as e:
        logger.error([str(e), expression1, expression2])
        response["error"] = _("Failed to evaluate expression.")
    except Exception as e:
        logger.error([str(e), expression1, expression2])
        response["error"] = _("Unknown error, check your expression.")
    return response  # }}}


def qm_runner(expression1, expression2, global_text ,result_queue):
    response = qm_compare(expression1, expression2 ,global_text )
    result_queue.put(response)


def qm(expression1, expression2, global_text):
    """
    Starts a process with quantum_internal that will be terminated if it takes too long. This implementation uses multiprocessing.Process.
    """
    invalid_strings = ["_", "[", "]"]
    for i in invalid_strings:
        if i in expression1:
            return {"error": _("Answer contains invalid character ") + i}
    try :
        return safe_run(qm_runner, args=(expression1, expression2,global_text))
    except: 
        pass


def to_latex(expression):
    latex = ""
    try:
        latex = latex(sympify(asciiToSympy(expression), ns))  # _clash))
    except SympifyError as e:
        print(e)
        latex = "error"
    return latex
