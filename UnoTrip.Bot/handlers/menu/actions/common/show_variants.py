async def show_variants(callback, response):
    for sight in response['results']:
        reply = f'✨ {sight["name"]}\n\n'
        reply += f'Категория: {sight["categories"][0]["name"]}\n\n'
        reply += f'Адрес: {sight["location"]["formatted_address"]}\n\n'

        if 'description' in sight and sight['description']:
            reply += f'Описание: {sight["description"]}\n\n'

        if 'rating' in sight and sight['rating']:
            reply += f'⭐️ Рейтинг: {sight["rating"]}/10\n'

        if 'price' in sight and sight['price']:
            reply += f'💵 Средний чек: {price_to_string(sight["price"])}\n'

        if 'hours' in sight and sight['hours'] and 'regular' in sight['hours'] and sight['hours']['regular']:
            for hour in sight['hours']['regular']:
                day = day_to_week(hour["day"])

                if day:
                    reply += f'🕒 <b>{day_to_week(hour["day"])}</b> {hour["open"][:2]}:{hour["open"][2:]} - {hour["close"][:2]}:{hour["close"][2:]}\n'

        if 'tel' in sight and sight['tel']:
            reply += f'📞 Телефон: {sight["tel"]}\n\n'

        if 'website' in sight and sight['website']:
            reply += f'🌐 Сайт: {sight["website"]}\n\n'

        reply += f'Находится в {sight["distance"]} метрах от локации\n'

        await callback.message.answer(
            text=reply,
            parse_mode='HTML'
        )

        await callback.message.answer_location(
            latitude=sight['geocodes']['main']['latitude'],
            longitude=sight['geocodes']['main']['longitude'])

    await callback.answer()


def day_to_week(day: int):
    if day == 0:
        return 'Понедельник'
    if day == 1:
        return 'Вторник'
    if day == 2:
        return 'Среда'
    if day == 3:
        return 'Четверг'
    if day == 4:
        return 'Пятница'
    if day == 5:
        return 'Суббота'
    if day == 6:
        return 'Воскресенье'


def price_to_string(price_type: int):
    if price_type == 1:
        return 'Дешево'
    if price_type == 2:
        return 'Средне'
    if price_type == 3:
        return 'Дорого'
    if price_type == 4:
        return 'Супер дорого'
