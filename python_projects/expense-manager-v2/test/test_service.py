def test_amount_validation():

    amount = 100

    assert amount > 0


def test_expense_type():

    transaction_type = "expense"

    assert transaction_type in (
        "income",
        "expense"
    )