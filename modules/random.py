from api import *
import random

def fun_random(data:DSPD): return NumberValue(random.random())
def fun_randint(data:DSPD): return NumberValue(random.randint(int(DSAPI.check_ret(data,"a","Number").value),int(DSAPI.check_ret(data,"b","Number").value)))
def fun_randfloat(data:DSPD): return NumberValue(random.uniform(float(DSAPI.check_ret(data,"a","Number").value),float(DSAPI.check_ret(data,"b","Number").value)))
def fun_seed(data:DSPD): return NullValue(random.seed(DSAPI.check_ret(data,"seed","Number").value))
def fun_randrange(data:DSPD): return NumberValue(random.randrange(int(DSAPI.check_ret(data,"start","Number").value),int(DSAPI.check_ret(data,"stop","Number").value),int(DSAPI.check_ret(data,"step","Number").value)))
def fun_randchoice(data:DSPD): return random.choice(DSAPI.check_ret(data, "list", "List").value)
def fun_betavariate(data:DSPD): return NumberValue(random.betavariate(float(DSAPI.check_ret(data, "alpha", "Number").value),float(DSAPI.check_ret(data,"beta","Number").value)))
def fun_expovariate(data:DSPD): return NumberValue(random.expovariate(float(DSAPI.check_ret(data, "lambda", "Number").value)))
def fun_gammavariate(data:DSPD): return NumberValue(random.gammavariate(float(DSAPI.check_ret(data, "alpha", "Number").value),float(DSAPI.check_ret(data,"beta","Number").value)))
def fun_gauss(data:DSPD): return NumberValue(random.gauss(float(DSAPI.check_ret(data, "mu", "Number").value),float(DSAPI.check_ret(data,"sigma","Number").value)))
def fun_lognormvariate(data:DSPD): return NumberValue(random.lognormvariate(float(DSAPI.check_ret(data, "mu", "Number").value),float(DSAPI.check_ret(data,"sigma","Number").value)))
def fun_normalvariate(data:DSPD): return NumberValue(random.normalvariate(float(DSAPI.check_ret(data, "mu", "Number").value),float(DSAPI.check_ret(data,"sigma","Number").value)))
def fun_paretovariate(data:DSPD): return NumberValue(random.paretovariate(float(DSAPI.check_ret(data, "alpha", "Number").value)))
def fun_triangular(data:DSPD): return NumberValue(random.triangular(float(DSAPI.check_ret(data, "low", "Number").value),float(DSAPI.check_ret(data,"high","Number").value),DSAPI.check_ret(data,"mode",["Number","Null"]).value))
def fun_vonmisesvariate(data:DSPD): return NumberValue(random.vonmisesvariate(float(DSAPI.check_ret(data, "mu", "Number").value),float(DSAPI.check_ret(data,"kappa","Number").value)))
def fun_randbits(data:DSPD): return NumberValue(random.getrandbits(int(DSAPI.check_ret(data, "k", "Number").value)))
def fun_weibullvariate(data:DSPD): return NumberValue(random.weibullvariate(float(DSAPI.check_ret(data, "alpha", "Number").value),float(DSAPI.check_ret(data,"beta","Number").value)))

def fun_shuffle(data:DSPD):
    copy = DSAPI.check_ret(data, "list","List").value.copy()
    random.shuffle(copy)
    return ListValue(copy)

module = {
    "name":"random",
    "functions":{
        "random": [fun_random, []],
        "randint": [fun_randint, ["a", "b"]],
        "randfloat": [fun_randfloat, ["a", "b"]],
        "randrange": [fun_randrange, ["start", "stop", "step"]],
        "seed": [fun_randint, ["seed"]],
        "randchoice": [fun_randchoice, ["list"]],
        "shuffle": [fun_shuffle, ["list"]],
        "betavariate": [fun_betavariate, ["alpha", "beta"]],
        "expovariate": [fun_expovariate, ["lambda"]],
        "gammavariate": [fun_gammavariate, ["alpha", "beta"]],
        "gauss": [fun_gauss, ["mu", "sigma"]],
        "lognormvariate": [fun_lognormvariate, ["mu", "sigma"]],
        "normalvariate": [fun_normalvariate, ["mu", "sigma"]],
        "paretovariate": [fun_paretovariate, ["alpha"]],
        "triangular": [fun_triangular, ["low", "high", "mode"]],
        "vonmisesvariate": [fun_vonmisesvariate, ["mu", "kappa"]],
        "randbits": [fun_randbits, ["k"]],
        "weibullvariate": [fun_weibullvariate, ["alpha", "beta"]],
    }
}

DSAPI.add_module(module)