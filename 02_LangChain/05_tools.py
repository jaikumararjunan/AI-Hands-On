from langchain.tools import tool


@tool
def multiply(
    number1: float,
    number2: float
) -> float:
    """
    Multiply two numbers.

    Use this tool when multiplication
    is required.
    """

    return number1 * number2


if __name__ == "__main__":

    print(
        "Tool name:",
        multiply.name
    )

    print(
        "Description:",
        multiply.description
    )

    result = multiply.invoke({
        "number1": 10,
        "number2": 20
    })

    print(
        "Result:",
        result
    )