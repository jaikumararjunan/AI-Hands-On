import os

from pathlib import Path
from typing import TypedDict

import pandas as pd

from sklearn.linear_model import (
    LinearRegression
)

from langchain_ollama import (
    ChatOllama
)

from langgraph.graph import (
    StateGraph,
    START,
    END
)


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = (
    Path(__file__).resolve().parent
    / ".."
    / "01_Python_DataScience"
    / "sales_100k_raw.csv"
).resolve()


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)


OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://127.0.0.1:11434"
)


# ============================================================
# GRAPH STATE
# ============================================================

class EnterpriseState(
    TypedDict,
    total=False
):
    question: str

    cleaned_question: str

    route: str

    quantity: float

    unit_price: float

    discount_pct: float

    marketing_spend: float

    answer: str

    valid: bool

    retry_count: int


# ============================================================
# SHARED MODEL
# ============================================================

llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)


# ============================================================
# NODE 1
# NORMALIZE USER INPUT
# ============================================================

def normalize_input(
    state: EnterpriseState
):
    question = (
        state["question"]
        .strip()
    )

    return {
        "cleaned_question":
            question,

        "retry_count":
            state.get(
                "retry_count",
                0
            )
    }


# ============================================================
# NODE 2
# CLASSIFY REQUEST
# ============================================================

def classify(
    state: EnterpriseState
):
    question = (
        state[
            "cleaned_question"
        ]
        .lower()
    )


    if (
        "predict" in question
        or
        "forecast" in question
    ):
        return {
            "route": "ml"
        }


    if (
        "sales" in question
        or
        "revenue" in question
        or
        "product" in question
        or
        "region" in question
    ):
        return {
            "route": "data"
        }


    return {
        "route": "general"
    }


# ============================================================
# ROUTER
# ============================================================

def choose_route(
    state: EnterpriseState
):
    return state["route"]


# ============================================================
# DATA NODE
# ============================================================

def data_analysis(
    state: EnterpriseState
):
    if not DATA_FILE.exists():
        return {
            "answer":
                f"Dataset not found: {DATA_FILE}"
        }


    df = pd.read_csv(
        DATA_FILE
    )


    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )


    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )


    df = df.drop_duplicates()


    df = df.dropna(
        subset=[
            "quantity",
            "unit_price",
            "region"
        ]
    )


    df = df[
        df["quantity"] > 0
    ]


    df["gross_revenue"] = (
        df["quantity"]
        *
        df["unit_price"]
    )


    df["net_revenue"] = (
        df["gross_revenue"]
        *
        (
            1
            -
            df["discount_pct"]
        )
    )


    question = (
        state[
            "cleaned_question"
        ]
        .lower()
    )


    # ----------------------------------------
    # Region question
    # ----------------------------------------

    if "region" in question:

        result = (
            df.groupby("region")[
                "net_revenue"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
        )


        return {
            "answer":
                "Revenue by region:\n\n"
                +
                result.to_string()
        }


    # ----------------------------------------
    # Product question
    # ----------------------------------------

    if "product" in question:

        result = (
            df.groupby("product")[
                "net_revenue"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(5)
        )


        return {
            "answer":
                "Top products by revenue:\n\n"
                +
                result.to_string()
        }


    # ----------------------------------------
    # Total revenue question
    # ----------------------------------------

    total_revenue = (
        df["net_revenue"]
        .sum()
    )


    return {
        "answer":
            (
                "Total net revenue: "
                f"{total_revenue:,.2f}"
            )
    }


# ============================================================
# GENERAL LLM NODE
# ============================================================

def general_llm(
    state: EnterpriseState
):
    response = llm.invoke(
        state["cleaned_question"]
    )


    return {
        "answer":
            response.content
    }


# ============================================================
# ML NODE
# ============================================================

def ml_prediction(
    state: EnterpriseState
):
    required_fields = [
        "quantity",
        "unit_price",
        "discount_pct",
        "marketing_spend"
    ]


    missing_fields = [
        field
        for field in required_fields
        if field not in state
    ]


    if missing_fields:

        return {
            "answer":
                (
                    "ML request is missing: "
                    +
                    ", ".join(
                        missing_fields
                    )
                )
        }


    if not DATA_FILE.exists():

        return {
            "answer":
                f"Dataset not found: {DATA_FILE}"
        }


    df = pd.read_csv(
        DATA_FILE
    )


    for column in required_fields:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


    df = df.dropna(
        subset=required_fields
    )


    df = df[
        df["quantity"] > 0
    ]


    df["net_revenue"] = (
        df["quantity"]
        *
        df["unit_price"]
        *
        (
            1
            -
            df["discount_pct"]
        )
    )


    X = df[
        required_fields
    ]

    y = df[
        "net_revenue"
    ]


    model = LinearRegression()

    model.fit(
        X,
        y
    )


    new_order = pd.DataFrame([
        {
            "quantity":
                state["quantity"],

            "unit_price":
                state["unit_price"],

            "discount_pct":
                state["discount_pct"],

            "marketing_spend":
                state["marketing_spend"]
        }
    ])


    prediction = float(
        model.predict(
            new_order
        )[0]
    )


    return {
        "answer":
            (
                "Predicted net revenue: "
                f"{prediction:,.2f}"
            )
    }


# ============================================================
# FORMAT NODE
# ============================================================

def format_answer(
    state: EnterpriseState
):
    route = state.get(
        "route",
        "unknown"
    )


    answer = state.get(
        "answer",
        ""
    )


    formatted = (
        f"[Route: {route}]\n\n"
        f"{answer}"
    )


    return {
        "answer":
            formatted
    }


# ============================================================
# VALIDATION NODE
# ============================================================

def validate_answer(
    state: EnterpriseState
):
    answer = (
        state.get(
            "answer",
            ""
        )
        .strip()
    )


    valid = (
        len(answer) > 10
    )


    return {
        "valid": valid
    }


# ============================================================
# VALIDATION ROUTER
# ============================================================

def validation_route(
    state: EnterpriseState
):
    if state.get(
        "valid",
        False
    ):
        return "end"


    retry_count = state.get(
        "retry_count",
        0
    )


    if retry_count < 1:
        return "retry"


    return "end"


# ============================================================
# RETRY NODE
# ============================================================

def retry_node(
    state: EnterpriseState
):
    retry_count = (
        state.get(
            "retry_count",
            0
        )
        +
        1
    )


    return {
        "retry_count":
            retry_count,

        "answer":
            (
                "Unable to produce a "
                "valid answer after retry."
            ),

        "valid":
            True
    }


# ============================================================
# BUILD GRAPH
# ============================================================

builder = StateGraph(
    EnterpriseState
)


builder.add_node(
    "normalize",
    normalize_input
)


builder.add_node(
    "classify",
    classify
)


builder.add_node(
    "data",
    data_analysis
)


builder.add_node(
    "general",
    general_llm
)


builder.add_node(
    "ml",
    ml_prediction
)


builder.add_node(
    "format",
    format_answer
)


builder.add_node(
    "validate",
    validate_answer
)


builder.add_node(
    "retry",
    retry_node
)


# ============================================================
# EDGES
# ============================================================

builder.add_edge(
    START,
    "normalize"
)


builder.add_edge(
    "normalize",
    "classify"
)


builder.add_conditional_edges(
    "classify",
    choose_route,
    {
        "data": "data",
        "general": "general",
        "ml": "ml"
    }
)


builder.add_edge(
    "data",
    "format"
)


builder.add_edge(
    "general",
    "format"
)


builder.add_edge(
    "ml",
    "format"
)


builder.add_edge(
    "format",
    "validate"
)


builder.add_conditional_edges(
    "validate",
    validation_route,
    {
        "end": END,
        "retry": "retry"
    }
)


builder.add_edge(
    "retry",
    END
)


# ============================================================
# COMPILE
# ============================================================

graph = builder.compile()


# ============================================================
# DEMO 1
# DATA QUESTION
# ============================================================

print()
print("=" * 70)
print("DEMO 1 - DATA")
print("=" * 70)


result = graph.invoke({
    "question":
        "Which products generate the highest revenue?"
})


print(
    result["answer"]
)


# ============================================================
# DEMO 2
# GENERAL LLM QUESTION
# ============================================================

print()
print("=" * 70)
print("DEMO 2 - GENERAL LLM")
print("=" * 70)


result = graph.invoke({
    "question":
        "Explain what a Python decorator is."
})


print(
    result["answer"]
)


# ============================================================
# DEMO 3
# ML QUESTION
# ============================================================

print()
print("=" * 70)
print("DEMO 3 - ML")
print("=" * 70)


result = graph.invoke({
    "question":
        "Predict revenue for this order.",

    "quantity":
        3,

    "unit_price":
        65000,

    "discount_pct":
        0.10,

    "marketing_spend":
        700
})


print(
    result["answer"]
)