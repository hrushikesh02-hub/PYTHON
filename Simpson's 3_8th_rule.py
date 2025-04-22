import math

def safe_eval(expr, x_val):
    # All safe math functions you can use
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names["x"] = x_val
    return eval(expr, {"__builtins__": None}, allowed_names)

def simpsons_three_eighth(fx, a, b, n):
    if n % 3 != 0:
        raise ValueError("Number of intervals (n) must be a multiple of 3 for Simpson's 3/8 Rule.")

    h = (b - a) / n
    result = safe_eval(fx, a) + safe_eval(fx, b)

    for i in range(1, n):
        x = a + i * h
        term = safe_eval(fx, x)
        if i % 3 == 0:
            result += 2 * term
        else:
            result += 3 * term

    result *= (3 * h) / 8
    return result

# 🎯 User input
print("Enter your function in terms of x.")
print("✅ You can use: sin, cos, tan, log, exp etc.")

fx = input("Function f(x): ").lower()
a = float(input("Lower limit (a): "))
b = float(input("Upper limit (b): "))
n = int(input("Number of intervals (must be multiple of 3): "))

try:
    result = simpsons_three_eighth(fx, a, b, n)
    print(f"\n✅ Approximate value of integral using Simpson’s 3/8 Rule: {result}")
except Exception as e:
    print(f"\n❌ Error: {e}")
