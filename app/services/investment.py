async def distribute_investments(target, sources):
    """
    Распределяет средства между целевым объектом и источниками.
    target: CharityProject или Donation (новый объект)
    sources: список объектов противоположного типа (неинвестированные пожертвования или открытые проекты)
    Модифицирует объекты in-place.
    """
    for source in sources:
        if target.fully_invested:
            break
        # Защита от None
        target_inv = target.invested_amount or 0
        source_inv = source.invested_amount or 0
        target_need = target.full_amount - target_inv
        source_free = source.full_amount - source_inv
        transfer = min(source_free, target_need)
        source.invested_amount = source_inv + transfer
        target.invested_amount = target_inv + transfer
        if source.invested_amount == source.full_amount:
            source.close_project()
        if target.invested_amount == target.full_amount:
            target.close_project()
    return target, sources
