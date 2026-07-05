from app.models.base import InvestmentBase


def distribute_investments(
    target: InvestmentBase,
    sources: list[InvestmentBase],
) -> list[InvestmentBase]:
    changed = []
    for source in sources:
        transfer = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        for obj in (source, target):
            obj.invested_amount += transfer
            obj.close_if_fully_invested()
        changed.append(source)
        if target.fully_invested:
            break
    return changed
