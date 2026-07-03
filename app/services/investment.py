def distribute_investments(target, sources):
    for source in sources:
        if target.fully_invested:
            break
        target_need = target.full_amount - target.invested_amount
        source_free = source.full_amount - source.invested_amount
        transfer = min(source_free, target_need)
        source.invested_amount += transfer
        target.invested_amount += transfer
        if source.invested_amount == source.full_amount:
            source.close_project()
        if target.invested_amount == target.full_amount:
            target.close_project()
