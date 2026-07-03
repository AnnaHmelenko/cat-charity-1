def distribute_investments(target, sources):
    for source in sources:
        if target.fully_invested:
            break
        target_need = target.full_amount - (target.invested_amount or 0)
        source_free = source.full_amount - (source.invested_amount or 0)
        transfer = min(source_free, target_need)
        source.invested_amount = (source.invested_amount or 0) + transfer
        target.invested_amount = (target.invested_amount or 0) + transfer
        if source.invested_amount == source.full_amount:
            source.close_project()
        if target.invested_amount == target.full_amount:
            target.close_project()
    return target, sources
