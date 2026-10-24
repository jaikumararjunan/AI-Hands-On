from langchain.tools import tool


@tool
def multiply(
    number1: float,
    number2: float
) -> float:
    """
    Multiply two numbers.

    Use this tool when two numeric values
    need to be multiplied.
    """

    return number1 * number2


print("Tool name:", multiply.name)

print("Tool description:")
print(multiply.description)


result = multiply.invoke({
    "number1": 10,
    "number2": 20
})


print("Result:", result)