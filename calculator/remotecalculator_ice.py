from sys import version_info as _version_info_
import Ice, IcePy

# Start of module RemoteCalculator
_M_RemoteCalculator = Ice.openModule('RemoteCalculator')
__name__ = 'RemoteCalculator'

if 'ZeroDivisionError' not in _M_RemoteCalculator.__dict__:
    _M_RemoteCalculator.ZeroDivisionError = Ice.createTempClass()
    class ZeroDivisionError(Ice.UserException):
        def __init__(self):
            pass

        def __str__(self):
            return IcePy.stringifyException(self)

        __repr__ = __str__

        _ice_id = '::RemoteCalculator::ZeroDivisionError'

    _M_RemoteCalculator._t_ZeroDivisionError = IcePy.defineException('::RemoteCalculator::ZeroDivisionError', ZeroDivisionError, (), False, None, ())
    ZeroDivisionError._ice_type = _M_RemoteCalculator._t_ZeroDivisionError

    _M_RemoteCalculator.ZeroDivisionError = ZeroDivisionError
    del ZeroDivisionError

_M_RemoteCalculator._t_Calculator = IcePy.defineValue('::RemoteCalculator::Calculator', Ice.Value, -1, (), False, True, None, ())

if 'CalculatorPrx' not in _M_RemoteCalculator.__dict__:
    _M_RemoteCalculator.CalculatorPrx = Ice.createTempClass()
    class CalculatorPrx(Ice.ObjectPrx):

        def sum(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_sum.invoke(self, ((a, b), context))

        def sumAsync(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_sum.invokeAsync(self, ((a, b), context))

        def begin_sum(self, a, b, _response=None, _ex=None, _sent=None, context=None):
            return _M_RemoteCalculator.Calculator._op_sum.begin(self, ((a, b), _response, _ex, _sent, context))

        def end_sum(self, _r):
            return _M_RemoteCalculator.Calculator._op_sum.end(self, _r)

        def sub(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_sub.invoke(self, ((a, b), context))

        def subAsync(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_sub.invokeAsync(self, ((a, b), context))

        def begin_sub(self, a, b, _response=None, _ex=None, _sent=None, context=None):
            return _M_RemoteCalculator.Calculator._op_sub.begin(self, ((a, b), _response, _ex, _sent, context))

        def end_sub(self, _r):
            return _M_RemoteCalculator.Calculator._op_sub.end(self, _r)

        def mult(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_mult.invoke(self, ((a, b), context))

        def multAsync(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_mult.invokeAsync(self, ((a, b), context))

        def begin_mult(self, a, b, _response=None, _ex=None, _sent=None, context=None):
            return _M_RemoteCalculator.Calculator._op_mult.begin(self, ((a, b), _response, _ex, _sent, context))

        def end_mult(self, _r):
            return _M_RemoteCalculator.Calculator._op_mult.end(self, _r)

        def div(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_div.invoke(self, ((a, b), context))

        def divAsync(self, a, b, context=None):
            return _M_RemoteCalculator.Calculator._op_div.invokeAsync(self, ((a, b), context))

        def begin_div(self, a, b, _response=None, _ex=None, _sent=None, context=None):
            return _M_RemoteCalculator.Calculator._op_div.begin(self, ((a, b), _response, _ex, _sent, context))

        def end_div(self, _r):
            return _M_RemoteCalculator.Calculator._op_div.end(self, _r)

        @staticmethod
        def checkedCast(proxy, facetOrContext=None, context=None):
            return _M_RemoteCalculator.CalculatorPrx.ice_checkedCast(proxy, '::RemoteCalculator::Calculator', facetOrContext, context)

        @staticmethod
        def uncheckedCast(proxy, facet=None):
            return _M_RemoteCalculator.CalculatorPrx.ice_uncheckedCast(proxy, facet)

        @staticmethod
        def ice_staticId():
            return '::RemoteCalculator::Calculator'
    _M_RemoteCalculator._t_CalculatorPrx = IcePy.defineProxy('::RemoteCalculator::Calculator', CalculatorPrx)

    _M_RemoteCalculator.CalculatorPrx = CalculatorPrx
    del CalculatorPrx

    _M_RemoteCalculator.Calculator = Ice.createTempClass()
    class Calculator(Ice.Object):

        def ice_ids(self, current=None):
            return ('::Ice::Object', '::RemoteCalculator::Calculator')

        def ice_id(self, current=None):
            return '::RemoteCalculator::Calculator'

        @staticmethod
        def ice_staticId():
            return '::RemoteCalculator::Calculator'

        def sum(self, a, b, current=None):
            raise NotImplementedError("servant method 'sum' not implemented")

        def sub(self, a, b, current=None):
            raise NotImplementedError("servant method 'sub' not implemented")

        def mult(self, a, b, current=None):
            raise NotImplementedError("servant method 'mult' not implemented")

        def div(self, a, b, current=None):
            raise NotImplementedError("servant method 'div' not implemented")

        def __str__(self):
            return IcePy.stringify(self, _M_RemoteCalculator._t_CalculatorDisp)

        __repr__ = __str__

    _M_RemoteCalculator._t_CalculatorDisp = IcePy.defineClass('::RemoteCalculator::Calculator', Calculator, (), None, ())
    Calculator._ice_type = _M_RemoteCalculator._t_CalculatorDisp

    Calculator._op_sum = IcePy.Operation('sum', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_float, False, 0), ((), IcePy._t_float, False, 0)), (), ((), IcePy._t_float, False, 0), ())
    Calculator._op_sub = IcePy.Operation('sub', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_float, False, 0), ((), IcePy._t_float, False, 0)), (), ((), IcePy._t_float, False, 0), ())
    Calculator._op_mult = IcePy.Operation('mult', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_float, False, 0), ((), IcePy._t_float, False, 0)), (), ((), IcePy._t_float, False, 0), ())
    Calculator._op_div = IcePy.Operation('div', Ice.OperationMode.Normal, Ice.OperationMode.Normal, False, None, (), (((), IcePy._t_float, False, 0), ((), IcePy._t_float, False, 0)), (), ((), IcePy._t_float, False, 0), (_M_RemoteCalculator._t_ZeroDivisionError,))

    _M_RemoteCalculator.Calculator = Calculator
    del Calculator

# End of module RemoteCalculator
