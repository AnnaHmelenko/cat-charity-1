def distribute_investments(target, sources):
    for source in sources:
        if target.fully_invested:
            break
        transfer = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount,
        )
        source.invested_amount += transfer
        target.invested_amount += transfer
        if source.invested_amount == source.full_amount:
            source.close_project()
        if target.invested_amount == target.full_amount:
            target.close_project()
