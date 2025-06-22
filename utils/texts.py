TEXTS = {
    "commands": {
        "start": {
            "language": {
                "ru": "<b>🌍 Выберите язык / Choose a language</b>\n\n"
                      "Выберите язык бота и уведомлений.\n"
                      "Choose the language in which you want to receive notifications.",
                "en": "<b>🌍 Choose a language / Выберите язык</b>\n\n"
                      "Choose the language in which you want to receive notifications.\n"
                      "Выберите язык бота и уведомлений."
            },
            "welcome": {
                "ru": (
                    "🚀 <b>Arbitrage Screener</b>\n\n"
                    "- Больше 20 криптобирж\n"
                    "- Обновление каждые 5 секунд\n"
                    "- Максимальная фильтрация связок\n\n"
                    "🎁 Приглашай пользователей и получай вознаграждения\n\n"
                    "💬 Все действия выполняются через кнопки или команды:\n"
                    "<b>[ /start,  /menu,  /arbitrage, /settings,\n"
                    "/language,  /referral_program,  /help,\n"
                    "/subscriptions ]</b>"
                ),
                "en": (
                    "🚀 <b>Arbitrage Screener</b>\n\n"
                    "- More than 20 crypto exchanges\n"
                    "- Updates every 5 seconds\n"
                    "- Advanced filtering\n\n"
                    "🎁 Invite users and get rewards\n\n"
                    "💬 Use buttons or commands:\n"
                    "<b>[ /start,  /menu,  /arbitrage, /settings,\n"
                    "/language,  /referral_program,  /help,\n"
                    "/subscriptions ]</b>"
                )
            },
            "referral_invitation": {
                "ru": "<b>🔗 {first_name} был приглашён по вашей ссылке!\n\n"
                      "🎁 Если ваш реферал совершит платёж за подписку, вы получите вознаграждение.</b>\n\n"
                      "Подробнее о реферальной программе: <b>/referral_program</b>",
                "en": "<b>🔗 {first_name} was invited by your link!\n\n"
                      "🎁 If your referral makes a subscription payment, you will receive a reward.</b>\n\n"
                      "Learn more about the referral program: <b>/referral_program</b>"
            }
        },
        "menu": {
            "ru": "<b>МЕНЮ:</b>",
            "en": "<b>MENU:</b>"
        },
        "referrals": {
            "set_referrals": {
                "ru": "<b>💸 РЕФЕРАЛЬНАЯ ПРОГРАММА:</b>\n\n"
                      ""
                      "Приглашай друзей и зарабатывай вместе с нами!\n"
                      "Ты получаешь <b>40%</b> от стоимости подписки, оформленной приглашённым пользователем.\n\n"
                      ""
                      "<b>👥 Как это работает:\n</b>"
                      "    1. Отправь свою уникальную ссылку другу.\n"
                      "    2. Он запускает бота и покупает подписку.\n"
                      "    3. Ты моментально получаешь <b>40%</b> от его оплаты.\n\n"
                      ""
                      "🔗 Твоя ссылка:\n"
                      "<b>{user_referral_link}</b>\n\n"
                      ""
                      "📌 Бонусы начисляются автоматически после каждой оплаты.",
                "en": "<b>💸 REFERRAL PROGRAM:</b>\n\n"
                      ""
                      "Invite your friends and earn with us!\n"
                      "You receive <b>40%</b> of the subscription amount paid by the referred user.\n\n"
                      ""
                      "<b>👥 How it works:\n</b>"
                      "    1. Send your unique link to a friend.\n"
                      "    2. They start the bot and purchase a subscription.\n"
                      "    3. You instantly receive <b>40%</b> of their payment.\n\n"
                      ""
                      "🔗 Your link:\n"
                      "<b>{user_referral_link}</b>\n\n"
                      "📌 Bonuses are credited automatically after each payment.",
            },
            "common_statistics": {
                "ru": "<b>📊 ОБЩАЯ СТАТИСТИКА:</b>\n\n"
                      "Приглашено пользователей: <b>{referrals_count}</b>\n"
                      "Оплачено подписок: <b>{paid_subscriptions_quantity}</b>\n"
                      "Баланс: <b>${referral_balance}</b>\n\n"
                      "💰 <b>Всего заработано: ${total_earned}</b>",
                "en": "<b>📊 GENERAL STATISTICS:</b>\n\n"
                      "Users invited: <b>{referrals_count}</b>\n"
                      "Subscriptions paid: <b>{paid_subscriptions_quantity}</b>\n"
                      "Balance: <b>${referral_balance}</b>\n\n"
                      "💰 <b>Total earned: ${total_earned}</b>"
            },
            "withdraw": {
                "set_network": {
                    "ru": "<b>💸 ВЫВОД СРЕДСТВ:</b>\n\n"
                          "🔽 Впишите ниже сеть для вывода средств в монете USDT.\n\n"
                          "Например: <b>TRC20, ERC20, BEP20</b> и т.д.",
                    "en": "<b>💸 WITHDRAW FUNDS:</b>\n\n"
                          "🔽 Enter the network for withdrawing funds in USDT below.\n\n"
                          "For example: <b>TRC20, ERC20, BEP20</b> etc."
                },
                "set_address": {
                    "ru": "<b>💸 ВЫВОД СРЕДСТВ:</b>\n\n"
                          "🔽 Впишите ниже адрес для вывода средств в монете USDT.\n\n"
                          "После ввода адреса, вы сможете подтвердить вывод средств.",
                    "en": "<b>💸 WITHDRAW FUNDS:</b>\n\n"
                          "🔽 Enter the address for withdrawing funds in USDT below.\n\n"
                          "After entering the address, you will be able to confirm the withdrawal."
                },
                "confirm_withdraw": {
                    "ru": "<b>💸 ПОДТВЕРДИТЕ ВЫВОД:</b>\n\n"
                          "Вывод <b>${amount}</b> USDT\n"
                          "Сеть: <b>{network}</b>\n"
                          "Адрес вывода: <code>{address}</code>\n\n"
                          "После подтверждения ожидайте зачисление в течении 3 часов.\n\n"
                          "Если была не полностью или некорректно указана сеть или адрес, "
                          "то мы свяжемся с вами напрямую для уточнения.",
                    "en": "<b>💸 CONFIRM WITHDRAW:</b>\n\n"
                          "Withdrawal of <b>${amount}</b> USDT\n"
                          "Network: <b>{network}</b>\n"
                          "Withdrawal address: <code>{address}</code>\n\n"
                          "After confirmation, please wait for the deposit within 3 hours.\n\n"
                          "If the network or address was not fully or correctly specified, "
                          "we will contact you directly for clarification."
                },
                "success": {
                    "ru": "<b>✅ Вывод успешно инициирован, а ваш баланс обнулен!</b>\n\n"
                          "Ожидайте поступление средств в течении 3 часов.\n\n",
                    "en": "<b>✅ Withdrawal successfully initiated, and your balance has been reset!</b>\n\n"
                          "Please wait for the funds to arrive within 3 hours.\n\n"
                }
            },
            "convert_to_subscription": {
                "set_exchanges": {
                    "ru": "<b>💳 ВЫБЕРИТЕ ТИП ПОДПИСКИ В КОТОРЫЙ ХОТИТЕ КОНВЕРТИРОВАТЬ СВОЙ БАЛАНС</b>\n\n"
                          "❕ После нажатия кнопки сразу будет оформлена подписка, а с вашего баланса "
                          "будет списана сумма, соответствующая выбранной подписке.\n\n"
                          "<b>Ваш баланс: {balance}$</b>",
                    "en": "<b>💳 CHOOSE THE TYPE OF SUBSCRIPTION YOU WANT TO CONVERT YOUR BALANCE TO</b>\n\n"
                          "❕ After clicking the button, the subscription will be activated immediately, "
                          "and the amount corresponding to the selected subscription will be deducted "
                          "from your balance.\n\n"
                          "<b>Your balance: {balance}$</b>"
                },
                "errors": {
                    "insufficient_balance": {
                        "ru": "<b>❗️ У вас недостаточно средств для конвертации!\n\n"
                              "Ваш баланс: <code>{balance}$</code></b>\n\n"
                              "<b>💳 Цены на подписки на межбиржевой арбитраж:</b>\n\n"
                              "<b>1 неделя:</b> <code>{one_week_price}$</code>\n"
                              "<b>1 месяц:</b> <code>{one_month_price}$</code>\n"
                              "<b>3 месяца:</b> <code>{three_month_price}$</code>\n"
                              "<b>НАВСЕГДА:</b> <code>{lifetime_price}$</code>",
                        "en": "<b>❗️ You have insufficient funds for conversion!\n\n"
                              "Your balance: <code>{balance}$</code></b>\n\n"
                              "<b>💳 Prices for inter-exchange arbitrage subscriptions:</b>\n\n"
                              "<b>1 week:</b> <code>{one_week_price}$</code>\n"
                              "<b>1 month:</b> <code>{one_month_price}$</code>\n"
                              "<b>3 months:</b> <code>{three_month_price}$</code>\n"
                              "<b>FOREVER:</b> <code>{lifetime_price}$</code>"
                    }
                },
                "success": {
                    "ru": "<b>✅ Подписка успешно оформлена!</b>\n\n"
                          "<b>Ваш баланс: {balance}$</b>",
                    "en": "<b>✅ Subscription successfully activated!</b>\n\n"
                          "<b>Your balance: {balance}$</b>"
                }
            }
        },
        "settings": {
            "ru": "<b>⚙️ НАСТРОЙКИ:</b>\n\n"
                  "ID Аккаунта: <code><b>{user_id}</b></code>\n"
                  "Статус подписок: \n"
                  "    Межбиржевой - <b>{subscription_status}</b>",
            "en": "<b>⚙️ SETTINGS:</b>\n\n"
                  "Account ID: <code><b>{user_id}</b></code>\n"
                  "Subscriptions status: \n"
                  "    Inter-Exchange - <b>{subscription_status}</b>",
            "day": {
                "ru": "д.",
                "en": "d."
            },
            "hour": {
                "ru": "ч.",
                "en": "h."
            },
            "minute": {
                "ru": "м.",
                "en": "m."
            },
            "seconds": {
                "ru": "с.",
                "en": "s."
            },
            "remain": {
                "ru": "осталось",
                "en": "remain"
            },
            "no_subscription": {
                "ru": "Нет подписки",
                "en": "No subscription"
            },
            "language": {
                "ru": "<b>🌍 Выберите язык / Choose a language</b>\n\n"
                      "Выберите язык бота и уведомлений.\n"
                      "Choose the language in which you want to receive notifications.",
                "en": "<b>🌍 Choose a language / Выберите язык</b>\n\n"
                      "Choose the language in which you want to receive notifications.\n"
                      "Выберите язык бота и уведомлений."
            },
            "exchanges": {
                "ru": "<b>💱 УСТАНОВИТЬ БИРЖИ</b>\n\n"
                      "Выберите биржи, которые хотите использовать.",
                "en": "<b>💱 SET EXCHANGES</b>\n\n"
                      "Choose the exchanges you want to use."
            },
            "spread": {
                "current_spread": {
                    "ru": "<b>Ваши текущие настройки спреда:</b>\n\n"
                          "Максимальный спред: <b>{max_spread}%</b>\n"
                          "Минимальный спред: <b>{min_spread}%</b>",
                    "en": "<b>Your current spread settings:</b>\n\n"
                          "Maximum spread: <b>{max_spread}%</b>\n"
                          "Minimum spread: <b>{min_spread}%</b>"
                },
                "set_max_spread": {
                    "ru": "<b>Введите максимальный спред ниже ⬇️</b>",
                    "en": "<b>Input max spread below ⬇️</b>"
                },
                "set_min_spread": {
                    "ru": "<b>Введите минимальный спред ниже ⬇️</b>",
                    "en": "<b>Input min spread below ⬇️</b>"
                },
                "errors": {
                    "max_spread": {
                        "not_a_number": {
                            "ru": "❗️ Максимальный спред должен быть числом!\n\n"
                                  "<b>Введите максимальный спред ниже ⬇️</b>",
                            "en": "❗️ The maximum spread must be a number!\n\n"
                                  "<b>Input maximum spread below ⬇️</b>"
                        },
                        "less_than_min": {
                            "ru": "❗️ Максимальный спред не может быть меньше или равен минимальному спреду!!\n\n"
                                  "<b>Введите максимальный спред ниже ⬇️</b>",
                            "en": "❗️ The maximum spread can't be less than or equal to the minimum spread!!\n\n"
                                  "<b>Input maximum spread below ⬇️</b>"
                        },
                        "greater_than_100": {
                            "ru": "❗️ Максимальный спред не может быть больше 100%!\n\n"
                                  "<b>Введите максимальный спред ниже ⬇️</b>",
                            "en": "❗️ The maximum spread can't be more than 100%!\n\n"
                                  "<b>Input maximum spread below ⬇️</b>"
                        }
                    },
                    "min_spread": {
                        "not_a_number": {
                            "ru": "❗️ Минимальный спред должен быть числом!\n\n"
                                  "<b>Введите минимальный спред ниже ⬇️</b>",
                            "en": "❗️ The minimum spread must be a number!\n\n"
                                  "<b>Input minimum spread below ⬇️</b>"
                        },
                        "less_than_0": {
                            "ru": "❗️ Минимальный спред не может быть меньше нуля!\n\n"
                                  "<b>Введите минимальный спред ниже ⬇️</b>",
                            "en": "❗️ The minimum spread can't be less than zero!\n\n"
                                  "<b>Input minimum spread below ⬇️</b>"
                        },
                        "greater_than_max": {
                            "ru": "❗️ Минимальный спред не может быть больше или равен максимальному спреду!\n\n"
                                  "<b>Введите минимальный спред ниже ⬇️</b>",
                            "en": "❗️ The minimum spread can't be greater than or equal to the maximum spread!\n\n"
                                  "<b>Input minimum spread below ⬇️</b>"
                        }
                    }
                },
                "success": {
                    "max_spread": {
                        "ru": "<b>✅ Максимальный спред успешно изменён!</b>\n\n"
                              "Минимальный спред: <b>{min_spread}%</b>\n"
                              "Максимальный спред: <b>{max_spread}%</b>",
                        "en": "<b>✅ Maximum spread successfully changed!</b>\n\n"
                              "Minimum spread: <b>{min_spread}%</b>\n"
                              "Maximum spread: <b>{max_spread}%</b>"
                    },
                    "min_spread": {
                        "ru": "<b>✅ Минимальный спред успешно изменён!</b>\n\n"
                              "Минимальный спред: <b>{min_spread}%</b>\n"
                              "Максимальный спред: <b>{max_spread}%</b>",
                        "en": "<b>✅ Minimum spread successfully changed!</b>\n\n"
                              "Minimum spread: <b>{min_spread}%</b>\n"
                              "Maximum spread: <b>{max_spread}%</b>"
                    }
                }
            },
            "profit": {
                "current_profit": {
                    "ru": "<b>Ваши текущие настройки профита:</b>\n\n"
                          "Минимальный профит: <b>{profit}$</b>",
                    "en": "<b>Your current profit settings:</b>\n\n"
                          "Minimum profit: <b>{profit}$</b>"
                },
                "set_profit": {
                    "ru": "<b>Введите минимальный профит ниже ⬇️</b>",
                    "en": "<b>Input minimum profit below ⬇️</b>"
                },
                "errors": {
                    "not_a_number": {
                        "ru": "❗️ Минимальный профит должен быть числом!\n\n"
                              "<b>Введите минимальный профит ниже ⬇️</b>",
                        "en": "❗️ The minimum profit must be a number!\n\n"
                              "<b>Input minimum profit below ⬇️</b>"
                    },
                    "less_than_0": {
                        "ru": "❗️ Минимальный профит не может быть меньше или равен нулю!\n\n"
                              "<b>Введите минимальный профит ниже ⬇️</b>",
                        "en": "❗️ The minimum profit can't be less than or equal to zero!\n\n"
                              "<b>Input minimum profit below ⬇️</b>"
                    },
                    "greater_than_50000": {
                        "ru": "❗️ Минимальный профит не может быть больше 50,000!\n\n"
                              "<b>Введите минимальный профит ниже ⬇️</b>",
                        "en": "❗️ The minimum profit can't be greater than 50,000!\n\n"
                              "<b>Input minimum profit below ⬇️</b>"
                    }
                },
                "success": {
                    "profit": {
                        "ru": "<b>✅ Минимальный профит успешно изменён!</b>\n\n"
                              "<b>Текущий минимальный профит: {profit}$</b>",
                        "en": "<b>✅ Minimum profit successfully changed!</b>\n\n"
                              "<b>Current minimum profit: {profit}$</b>"
                    }
                }
            },
            "volume": {
                "current_volume": {
                    "ru": "<b>Ваши текущие настройки объёма:</b>\n\n"
                          "Максимальный объём: <b>{volume} USDT</b>",
                    "en": "<b>Your current volume settings:</b>\n\n"
                          "Max volume: <b>{volume} USDT</b>"
                },
                "set_volume": {
                    "ru": "<b>Введите максимальный объём ниже ⬇️</b>",
                    "en": "<b>Input max volume below ⬇️</b>"
                },
                "errors": {
                    "not_a_number": {
                        "ru": "❗️ Максимальный объём должен быть числом!\n\n"
                              "<b>Введите минимальный объём ниже ⬇️</b>",
                        "en": "❗️ The max volume must be a number!\n\n"
                              "<b>Input max volume below ⬇️</b>"
                    },
                    "less_than_0": {
                        "ru": "❗️ Максимальный объём не может быть меньше или равен нулю!\n\n"
                              "<b>Введите минимальный объём ниже ⬇️</b>",
                        "en": "❗️ The max volume can't be less than or equal to zero!\n\n"
                              "<b>Input max volume below ⬇️</b>"
                    },
                    "greater_than_1000000": {
                        "ru": "❗️ Максимальный объём не может быть больше 1,000,000 USDT!\n\n"
                              "<b>Введите минимальный объём ниже ⬇️</b>",
                        "en": "❗️ The max volume can't be greater than 1,000,000 USDT!\n\n"
                              "<b>Input max volume below ⬇️</b>"
                    }
                },
                "success": {
                    "volume": {
                        "ru": "<b>✅ Максимальный объём успешно изменён!</b>\n\n"
                              "<b>Текущий максимальный объём: {volume} USDT</b>",
                        "en": "<b>✅ Max volume successfully changed!</b>\n\n"
                              "<b>Current max volume: {volume} USDT</b>"
                    }
                }
            },
            "network_speed": {
                "set_network_speed": {
                    "ru": "<b>Выберите ниже скорость сети</b>\n\n"
                          "⚡️ - До 2 минут\n"
                          "🟢 - До 5 минут\n"
                          "🟡 - До 20 минут\n"
                          "🔴 - До 1 часа\n"
                          "💀 - Более 1 часа\n\n"
                          "⚪️ - Неопределённая скорость сети\n\n"
                          "Выбирая скорость сети, вы опеределяете до какого максимального времени подтверждения буду показываться связки.",
                    "en": "<b>Select network speed below</b>\n\n"
                          "⚡️ - Up to 2 minutes\n"
                          "🟢 - Up to 5 minutes\n"
                          "🟡 - Up to 20 minutes\n"
                          "🔴 - Up to 1 hour\n"
                          "💀 - More than 1 hour\n\n"
                          "⚪️ - Undefined network speed\n\n"
                          "By selecting network speed you determine the maximum confirmation time for which pairs will be shown."
                }
            },
            "contracts": {
                "set_contracts": {
                    "ru": "<b>📜 ФИЛЬТР ПО КОНТРАКТАМ</b>\n\n"
                          "Выберите, какие связки показывать:\n"
                          "• Только с одинаковыми контрактами\n"
                          "• Или все, независимо от контрактов",
                    "en": "<b>📜 CONTRACTS FILTER</b>\n\n"
                          "Choose which pairs to show:\n"
                          "• Only with the same contracts\n"
                          "• Or all, regardless of contracts"
                }
            },
            "withdraw_fee": {
                "current_withdraw_fee": {
                    "ru": "<b>Ваши текущие настройки комиссии вывода:</b>\n\n"
                          "Максимальная комиссия вывода: <b>{withdraw_fee} USDT</b>",
                    "en": "<b>Your current withdrawal fee settings:</b>\n\n"
                          "Max ithdrawal fee: <b>{withdraw_fee} USDT</b>"
                },
                "set_withdraw_fee": {
                    "ru": "<b>Введите максимальную комиссию вывода ниже ⬇️</b>",
                    "en": "<b>Input max withdrawal fee below ⬇️</b>"
                },
                "errors": {
                    "not_a_number": {
                        "ru": "❗️ Максимальная комиссия вывода должна быть числом!\n\n"
                              "<b>Введите максимальную комиссию вывода ниже ⬇️</b>",
                        "en": "❗️ The max withdrawal fee must be a number!\n\n"
                              "<b>Input max withdrawal fee below ⬇️</b>"
                    },
                    "less_than_0": {
                        "ru": "❗️ Максимальная комиссия вывода не может быть меньше или равна нулю!\n\n"
                              "<b>Введите максимальную комиссию вывода ниже ⬇️</b>",
                        "en": "❗️ The max withdrawal fee can't be less than or equal to zero!\n\n"
                              "<b>Input max withdrawal fee below ⬇️</b>"
                    },
                    "greater_than_100000": {
                        "ru": "❗️ Максимальная комиссия вывода не может быть больше 100,000 USDT!\n\n"
                              "<b>Введите максимальную комиссию вывода ниже ⬇️</b>",
                        "en": "❗️ The max withdrawal fee can't be greater than 100,000 USDT!\n\n"
                              "<b>Input max withdrawal fee below ⬇️</b>"
                    }
                },
                "success": {
                    "withdraw_fee": {
                        "ru": "<b>✅ Максимальная комиссия вывода успешно изменена!</b>\n\n"
                              "<b>Текущая максимальная комиссия вывода: {withdraw_fee} USDT</b>",
                        "en": "<b>✅ Max withdrawal fee successfully changed!</b>\n\n"
                              "<b>Current max withdrawal fee: {withdraw_fee} USDT</b>"
                    }
                }
            },
            "volume_24h": {
                "current_volume_24h": {
                    "ru": "<b>Ваши текущие настройки оборота за 24ч:</b>\n\n"
                          "Максимальный оборот: <b>{max_coin_volume_24h} USDT</b>\n"
                          "Минимальный оборот: <b>{min_coin_volume_24h} USDT</b>",
                    "en": "<b>Your current 24h turnover settings:</b>\n\n"
                          "Max turnover: <b>{max_coin_volume_24h} USDT</b>\n"
                          "Minimum turnover: <b>{min_coin_volume_24h} USDT</b>"
                },
                "set_max_coin_volume_24h": {
                    "ru": "<b>Введите максимальный оборот за 24ч ниже ⬇️</b>",
                    "en": "<b>Input max 24h turnover below ⬇️</b>"
                },
                "set_min_coin_volume_24h": {
                    "ru": "<b>Введите минимальный оборот за 24ч ниже ⬇️</b>",
                    "en": "<b>Input min 24h turnover below ⬇️</b>"
                },
                "errors": {
                    "max_coin_volume_24h": {
                        "not_a_number": {
                            "ru": "❗️ Максимальный оборот должен быть числом!\n\n"
                                  "<b>Введите максимальный оборот за 24ч ниже ⬇️</b>",
                            "en": "❗️ The max 24h turnover must be a number!\n\n"
                                  "<b>Input max 24h turnover below ⬇️</b>"
                        },
                        "less_than_0": {
                            "ru": "❗️ Максимальный оборот не может быть меньше или равен нулю!\n\n"
                                  "<b>Введите максимальный оборот за 24ч ниже ⬇️</b>",
                            "en": "❗️ The max 24h turnover can't be less than or equal to zero!\n\n"
                                  "<b>Input max 24h turnover below ⬇️</b>"
                        },
                        "greater_than_100000000000": {
                            "ru": "❗️ Максимальный оборот не может быть больше 100,000,000,000 USDT!\n\n"
                                  "<b>Введите максимальный оборот за 24ч ниже ⬇️</b>",
                            "en": "❗️ The max 24h turnover can't be greater than 100,000,000,000 USDT!\n\n"
                                  "<b>Input max 24h turnover below ⬇️</b>"
                        },
                        "less_than_min": {
                            "ru": "❗️ Максимальный оборот не может быть меньше или равен минимальному обороту!\n\n"
                                  "<b>Введите максимальный оборот за 24ч ниже ⬇️</b>",
                            "en": "❗️ The max 24h turnover can't be less than or equal to the min 24h turnover!\n\n"
                                  "<b>Input max 24h turnover below ⬇️</b>"
                        }
                    },
                    "min_coin_volume_24h": {
                        "not_a_number": {
                            "ru": "❗️ Минимальный оборот должен быть числом!\n\n"
                                  "<b>Введите минимальный оборот за 24ч ниже ⬇️</b>",
                            "en": "❗️ The min 24h turnover must be a number!\n\n"
                                  "<b>Input min 24h turnover below ⬇️</b>"
                        },
                        "less_than_0": {
                            "ru": "❗️ Минимальный оборот не может быть меньше или равен нулю!\n\n"
                                  "<b>Введите минимальный оборот за 24ч ниже ⬇️</b>",
                            "en": "❗️ The min 24h turnover can't be less than or equal to zero!\n\n"
                                  "<b>Input min 24h turnover below ⬇️</b>"
                        },
                        "greater_than_max": {
                            "ru": "❗️ Минимальный оборот не может быть больше или равен максимальному обороту!\n\n"
                                  "<b>Введите минимальный оборот за 24ч ниже ⬇️</b>",
                            "en": "❗️ The min 24h turnover can't be greater than or equal to the max 24h turnover!\n\n"
                                  "<b>Input min 24h turnover below ⬇️</b>"
                        }
                    }
                },
                "success": {
                    "max_coin_volume_24h": {
                        "ru": "<b>✅ Максимальный оборот за 24ч успешно изменён!</b>\n\n"
                              "<b>Текущий максимальный оборот: {max_coin_volume_24h} USDT</b>",
                        "en": "<b>✅ Max 24h turnover successfully changed!</b>\n\n"
                              "<b>Current max 24h turnover: {max_coin_volume_24h} USDT</b>"
                    },
                    "min_coin_volume_24h": {
                        "ru": "<b>✅ Минимальный оборот за 24ч успешно изменён!</b>\n\n"
                              "<b>Текущий минимальный оборот: {min_coin_volume_24h} USDT</b>",
                        "en": "<b>✅ Min 24h turnover successfully changed!</b>\n\n"
                              "<b>Current min 24h turnover: {min_coin_volume_24h} USDT</b>"
                    }
                }
            },
            "last_trade_time": {
                "current_last_trade_time": {
                    "ru": "<b>Ваши текущие настройки времени последней торговли:</b>\n\n"
                          "Максимальное время: <b>{max_last_trade_time}</b>\n"
                          "Минимальное время: <b>{min_last_trade_time}</b>\n\n"
                          "Связки будут показываться, если время последней торговли монеты на второй бирже будет "
                          "входить в ваш диапазон времени - <b>ОТ</b> {min_last_trade_time} "
                          "<b>ДО</b> {max_last_trade_time}.",
                    "en": "<b>Your current last trade time settings:</b>\n\n"
                          "Maximum time: <b>{max_last_trade_time}</b>\n"
                          "Minimum time: <b>{min_last_trade_time}</b>\n\n"
                          "Pairs will be shown if the last trade time of the coin on the second exchange falls "
                          "within your time range - <b>FROM</b> {min_last_trade_time} <b>TO</b> {max_last_trade_time}."
                },
                "set_max_last_trade_time": {
                    "ru": "🕒 Введите максимальное время в формате: <b>Часы Минуты Секунды</b>\n\n"
                          "Например: <code>2 30 0</code> — это 2 часа 30 минут.\n"
                          "Если вы хотите ввести только минуты — можно так: <code>0 15 0</code>\n"
                          "Если вы хотите ввести только секунды — можно так: <code>0 0 15</code>",
                    "en": "🕒 Input max time in format: <b>Hours Minutes Seconds</b>\n\n"
                          "For example: <code>2 30 0</code> — this is 2 hours 30 minutes.\n"
                          "If you want to input only minutes — you can do it like this: <code>0 15 0</code>\n"
                          "If you want to input only seconds — you can do it like this: <code>0 0 15</code>"
                },
                "set_min_last_trade_time": {
                    "ru": "🕒 Введите минимальное время в формате: <b>Часы Минуты Секунды</b>\n\n"
                          "Например: <code>2 30 0</code> — это 2 часа 30 минут.\n"
                          "Если вы хотите ввести только минуты — можно так: <code>0 15 0</code>\n"
                          "Если вы хотите ввести только секунды — можно так: <code>0 0 15</code>\n"
                          "Связки включая от текущего времени последней торговли:\n"
                          "<code>0</code> ИЛИ <code>0 0 0</code>",
                    "en": "🕒 Input min time in format: <b>Hours Minutes Seconds</b>\n\n"
                          "For example: <code>2 30 0</code> — this is 2 hours 30 minutes.\n"
                          "If you want to input only minutes — you can do it like this: <code>0 15 0</code>\n"
                          "If you want to input only seconds — you can do it like this: <code>0 0 15</code>\n"
                          "Pairs including from the current last trade time:\n"
                          "<code>0</code> OR <code>0 0 0</code>"
                },
                "errors": {
                    "max_last_trade_time": {
                        "not_a_number": {
                            "ru": "❗️ Максимальное время должно быть числом!\n\n"
                                  "<b>Введите максимальное время ниже ⬇️</b>",
                            "en": "❗️ The max time must be a number!\n\n"
                                  "<b>Input max time below ⬇️</b>"
                        },
                        "less_than_min": {
                            "ru": "❗️ Максимальное время не может быть меньше или равно минимальному времени!\n\n"
                                  "<b>Введите максимальное время ниже ⬇️</b>",
                            "en": "❗️ The max time can't be less than or equal to the min time!\n\n"
                                  "<b>Input max time below ⬇️</b>"
                        },
                        "less_than_0": {
                            "ru": "❗️ Максимальное время не может быть меньше нуля!\n\n"
                                  "<b>Введите максимальное время ниже ⬇️</b>",
                            "en": "❗️ The max time can't be less than zero!\n\n"
                                  "<b>Input max time below ⬇️</b>"
                        },
                        "invalid_format": {
                            "ru": "❗️ Неверный формат времени!\n\n"
                                  "<b>Введите время в формате: Часы Минуты Секунды</b>\n\n"
                                  "Например: <code>2 30 0</code> — это 2 часа 30 минут.\n"
                                  "Если вы хотите ввести только минуты — можно так: <code>0 15 0</code>\n"
                                  "Если вы хотите ввести только секунды — можно так: <code>0 0 15</code>\n",
                            "en": "❗️ Invalid time format!\n\n"
                                  "<b>Input time in format: Hours Minutes Seconds</b>\n\n"
                                  "For example: <code>2 30 0</code> — this is 2 hours 30 minutes.\n"
                                  "If you want to input only minutes — you can do it like this: <code>0 15 0</code>\n"
                                  "If you want to input only seconds — you can do it like this: <code>0 0 15</code>\n"
                        },
                        "greater_than_1000000": {
                            "ru": "❗️ Слишком много!\n\n"
                        }
                    },
                    "min_last_trade_time": {
                        "not_a_number": {
                            "ru": "❗️ Минимальное время должно быть числом!\n\n"
                                  "<b>Введите минимальное время ниже ⬇️</b>",
                            "en": "❗️ The min time must be a number!\n\n"
                                  "<b>Input min time below ⬇️</b>"
                        },
                        "greater_than_max": {
                            "ru": "❗️ Минимальное время не может быть больше или равно максимальному времени!\n\n"
                                  "<b>Введите минимальное время ниже ⬇️</b>",
                            "en": "❗️ The min time can't be greater than or equal to the max time!\n\n"
                                  "<b>Input min time below ⬇️</b>"
                        },
                        "less_than_0": {
                            "ru": "❗️ Минимальное время не может быть меньше нуля!\n\n"
                                  "<b>Введите минимальное время ниже ⬇️</b>",
                            "en": "❗️ The min time can't be less than zero!\n\n"
                                  "<b>Input min time below ⬇️</b>"
                        },
                        "invalid_format": {
                            "ru": "❗️ Неверный формат времени!\n\n"
                                  "<b>Введите время в формате: Часы Минуты Секунды</b>\n\n"
                                  "Например: <code>2 30 0</code> — это 2 часа 30 минут.\n"
                                  "Если вы хотите ввести только минуты — можно так: <code>0 15 0</code>\n"
                                  "Если вы хотите ввести только секунды — можно так: <code>0 0 15</code>\n"
                                  "Связки включая от текущего времени последней торговли: \n"
                                  "<code>0</code> ИЛИ <code>0 0 0</code>",
                            "en": "❗️ Invalid time format!\n\n"
                                  "<b>Input time in format: Hours Minutes Seconds</b>\n\n"
                                  "For example: <code>2 30 0</code> — this is 2 hours 30 minutes.\n"
                                  "If you want to input only minutes — you can do it like this: <code>0 15 0</code>\n"
                                  "If you want to input only seconds — you can do it like this: <code>0 0 15</code>"
                                  "Pairs including from the current last trade time: \n"
                                  "<code>0</code> OR <code>0 0 0</code>"
                        },
                        "greater_than_1000000": {
                            "ru": "❗️ Слишком много!\n\n"
                        }
                    }
                },
                "success": {
                    "max_last_trade_time": {
                        "ru": "<b>✅ Максимальное время успешно изменено!</b>\n\n"
                              "<b>Текущее максимальное время: {max_last_trade_time}</b>",
                        "en": "<b>✅ Max time successfully changed!</b>\n\n"
                              "<b>Current max time: {max_last_trade_time}</b>"
                    },
                    "min_last_trade_time": {
                        "ru": "<b>✅ Минимальное время успешно изменено!</b>\n\n"
                              "<b>Текущее минимальное время: {min_last_trade_time}</b>",
                        "en": "<b>✅ Min time successfully changed!</b>\n\n"
                              "<b>Current min time: {min_last_trade_time}</b>"
                    }
                }
            },
            "notification": {
                "current_notification": {
                    "ru": "<b>Включение/отключение транслирования связок</b>",
                    "en": "<b>Enable/disable pair broadcasting</b>"
                }
            },
            "is_low_bids": {
                "current_is_low_bids": {
                    "ru": "<b>📉 ФИЛЬТР ПО КОЛИЧЕСТВУ ОРДЕРОВ</b>\n\n"
                          "Показывать связки с малым количеством ордеров в стакане?",
                    "en": "<b>📉 ORDERS FILTER</b>\n\n"
                          "Show pairs with a small number of orders in the order book?"

                }
            },
            "hedging_types": {
                "current_hedging_types": {
                    "ru": "<b>⚖️ ТИПЫ ХЕДЖИРОВАНИЯ:</b>\n\n",
                    "en": "<b>⚖️ HEDGING TYPES:</b>\n\n"
                },
                "set_futures_hedging": {
                    "ru": "Выберите фильтр фьючерсного хеджирования:",
                    "en": "Select futures hedging filter:"
                },
                "set_margin_hedging": {
                    "ru": "Выберите фильтр маржинального хеджирования:",
                    "en": "Select margin hedging filter:"
                },
                "set_loan_hedging": {
                    "ru": "Выберите фильтр займового хеджирования:",
                    "en": "Select loan hedging filter:"
                }
            },
            "blacklist_types": {
                "current_blacklist_types": {
                    "ru": "<b>🗑 ТИПЫ ЧЁРНЫХ СПИСКОВ:</b>\n\n",
                    "en": "<b>🗑 BLACKLIST TYPES:</b>\n\n"
                },
                "coins_blacklist": {
                    "current_coins_blacklist": {
                        "ru": "<b>🗑 МОНЕТЫ В ЧЕРНОМ СПИСКЕ:</b>\n\n",
                        "en": "<b>🗑 COINS IN BLACKLIST:</b>\n\n"
                    },
                    "no_coins_in_blacklist": {
                        "ru": "<b>🗑 Чёрный список монет пуст</b>",
                        "en": "<b>🗑 Coins blacklist is empty</b>"
                    },
                    "add_coins_blacklist": {
                        "ru": "<b>Введите название монеты, либо выберите монету ниже ⬇️</b>",
                        "en": "Input coin name or select coin below ⬇️"
                    },
                    "remove_coins_blacklist": {
                        "ru": "<b>Введите название монеты для удаления, либо выберите монету ниже ⬇️</b>",
                        "en": "<b>Input coin name to remove or select coin below ⬇️</b>"
                    },
                    "errors": {
                        "already_in_blacklist": {
                            "ru": "<b>️❗ Монета {coin} уже в чёрном списке!</b>\n\n"
                                  "<b>Введите название монеты, либо выберите монету ниже ⬇️</b>",
                            "en": "<b>❗️ Coin {coin} is already in the blacklist!</b>\n\n"
                                  "Input coin name or select coin below ⬇️"
                        },
                        "coin_name_too_long": {
                            "ru": "<b>️❗ Название монеты слишком длинное!\n\n</b>"
                                  "Максимальная длина названия монеты: <b>15 символов</b>\n\n"
                                  "Введите название монеты, либо выберите монету ниже ⬇️",
                            "en": "<b>❗️ Coin name is too long!\n\n</b>"
                                  "Maximum coin name length: <b>15 characters</b>\n\n"
                                  "Input coin name or select coin below ⬇️"
                        },
                        "unexpected_error": {
                            "ru": "<b>❗️ Произошла непредвиденная ошибка!</b>\n\n"
                                  "<b>Введите название монеты, либо выберите монету ниже ⬇️</b>",
                            "en": "<b>❗️ An unexpected error occurred!</b>\n\n"
                                  "Input coin name or select coin below ⬇️"
                        },
                        "not_in_blacklist": {
                            "ru": "<b>❗ Монета {coin} не в чёрном списке!</b>\n\n"
                                  "<b>Введите название монеты для удаления, либо выберите монету ниже ⬇️</b>",
                            "en": "<b>❗️ Coin {coin} is not in the blacklist!</b>\n\n"
                                  "<b>Input coin name to remove or select coin below ⬇️</b>"
                        }
                    },
                    "success": {
                        "coin_added": {
                            "ru": "<b>✅ Монета {coin} успешно добавлена в чёрный список!</b>",
                            "en": "<b>✅ Coin {coin} successfully added to the blacklist!</b>"
                        },
                        "coin_removed": {
                            "ru": "<b>✅ Монета {coin} успешно удалена из чёрного списка!</b>",
                            "en": "<b>✅ Coin {coin} successfully removed from the blacklist!</b>"
                        }
                    }
                },
                "networks_blacklist": {
                    "current_networks_blacklist": {
                        "ru": "<b>🗑 СЕТИ В ЧЁРНОМ СПИСКЕ:</b>\n\n",
                        "en": "<b>🗑 NETWORKS IN BLACKLIST:</b>\n\n"
                    },
                    "no_networks_in_blacklist": {
                        "ru": "<b>🗑 Чёрный список сетей пуст</b>",
                        "en": "<b>🗑 Networks blacklist is empty</b>"
                    },
                    "add_networks_blacklist": {
                        "ru": "<b>Введите название сети, либо выберите сеть ниже ⬇️</b>",
                        "en": "Input network name or select network below ⬇️"
                    },
                    "remove_networks_blacklist": {
                        "ru": "<b>Введите название сети для удаления, либо выберите сеть ниже ⬇️</b>",
                        "en": "<b>Input network name to remove or select network below ⬇️</b>"
                    },
                    "errors": {
                        "already_in_blacklist": {
                            "ru": "<b>️❗ Сеть {network} уже в чёрном списке!</b>\n\n"
                                  "<b>Введите название сети, либо выберите сеть ниже ⬇️</b>",
                            "en": "<b>❗️ Network {network} is already in the blacklist!</b>\n\n"
                                  "Input network name or select network below ⬇️"
                        },
                        "network_name_too_long": {
                            "ru": "<b>️❗ Название сети слишком длинное!\n\n</b>"
                                  "Максимальная длина названия сети: <b>15 символов</b>\n\n"
                                  "Введите название сети, либо выберите сеть ниже ⬇️",
                            "en": "<b>❗️ Network name is too long!\n\n</b>"
                                  "Maximum network name length: <b>15 characters</b>\n\n"
                                  "Input network name or select network below ⬇️"
                        },
                        "unexpected_error": {
                            "ru": "<b>❗️ Произошла непредвиденная ошибка!</b>\n\n"
                                  "<b>Введите название сети, либо выберите сеть ниже ⬇️</b>",
                            "en": "<b>❗️ An unexpected error occurred!</b>\n\n"
                                  "Input network name or select network below ⬇️"
                        },
                        "not_in_blacklist": {
                            "ru": "<b>❗ Сеть {network} не в чёрном списке!</b>\n\n"
                                  "<b>Введите название сети для удаления, либо выберите сеть ниже ⬇️</b>",
                            "en": "<b>❗️ Network {network} is not in the blacklist!</b>\n\n"
                                  "<b>Input network name to remove or select network below ⬇️</b>"
                        }
                    },
                    "success": {
                        "network_added": {
                            "ru": "<b>✅ Сеть {network} успешно добавлена в чёрный список!</b>",
                            "en": "<b>✅ Network {network} successfully added to the blacklist!</b>"
                        },
                        "network_removed": {
                            "ru": "<b>✅ Сеть {network} успешно удалена из чёрного списка!</b>",
                            "en": "<b>✅ Network {network} successfully removed from the blacklist!</b>"
                        }
                    }
                },
                "coin_for_exchange_blacklist": {
                    "current_coin_for_exchange_blacklist": {
                        "ru": "<b>🗑 МОНЕТЫ К БИРЖЕ В ЧЁРНОМ СПИСКЕ:</b>\n\n",
                        "en": "<b>🗑 COINS FOR EXCHANGE IN BLACKLIST:</b>\n\n"
                    },
                    "no_coin_for_exchange_blacklist": {
                        "ru": "<b>🗑 Чёрный список монет к бирже пуст</b>",
                        "en": "<b>🗑 Coins for exchange blacklist is empty</b>"
                    },
                    "add_coin_for_exchange_blacklist": {
                        "ru": "<b>Введите название монеты или монеты к бирже в формате:</b>\n\n"
                              "<code>Монета</code>\n"
                              "<code>Монета-Биржа</code>\n\n"
                              "<b>Например:</b> <code>BTC-Binance</code>",
                        "en": "<b>Input coin name or coins for exchange in format:</b>\n\n"
                              "<code>Coin</code>\n"
                              "<code>Coin-Exchange</code>\n\n"
                              "<b>For example:</b> <code>BTC-Binance</code>"
                    },
                    "remove_coin_for_exchange_blacklist": {
                        "ru": "<b>Введите название монеты или монеты к бирже для удаления в формате:</b>\n\n"
                              "<code>Монета</code>\n"
                              "<code>Монета-Биржа</code>\n\n"
                              "<b>Например:</b> <code>BTC-Binance</code>",
                        "en": "<b>Input coin name or coins for exchange to remove in format:</b>\n\n"
                              "<code>Coin</code>\n"
                              "<code>Coin-Exchange</code>\n\n"
                              "<b>For example:</b> <code>BTC-Binance</code>"
                    },
                    "select_exchange": {
                        "ru": "Выберите биржу для монеты <b>{coin}</b>",
                        "en": "Select exchange for coin <b>{coin}</b>"
                    },
                    "errors": {
                        "add": {
                            "wrong_input_format": {
                                "ru": "<b>❗️ Неверный формат ввода!</b>\n\n"
                                      "<b>Введите название монеты или монеты к бирже в формате:</b>\n\n"
                                      "<code>Монета</code>\n"
                                      "<code>Монета-Биржа</code>\n\n"
                                      "<b>Например:</b> <code>BTC-Binance</code>",
                                "en": "<b>❗️ Wrong input format!</b>\n\n"
                                      "<b>Input coin name or coins for exchange in format:</b>\n\n"
                                      "<code>Coin</code>\n"
                                      "<code>Coin-Exchange</code>\n\n"
                                      "<b>For example:</b> <code>BTC-Binance</code>"
                            },
                            "more_than_15_symbols": {
                                "ru": "<b>❗️ Название монеты не может быть длиннее 15 символов!</b>\n\n"
                                      "<b>Введите название монеты или монеты к бирже в формате:</b>\n\n"
                                      "<code>Монета</code>\n"
                                      "<code>Монета-Биржа</code>\n\n"
                                      "<b>Например:</b> <code>BTC-Binance</code>",
                                "en": "<b>❗️ Coin name can't be longer than 15 characters!</b>\n\n"
                                      "<b>Input coin name or coins for exchange in format:</b>\n\n"
                                      "<code>Coin</code>\n"
                                      "<code>Coin-Exchange</code>\n\n"
                                      "<b>For example:</b> <code>BTC-Binance</code>"
                            },
                            "wrong_exchange": {
                                "ru": "<b>❗️ Биржа не найдена!</b>\n\n"
                                      "<b>Введите название монеты или монеты к бирже в формате:</b>\n\n"
                                      "<code>Монета</code>\n"
                                      "<code>Монета-Биржа</code>\n\n"
                                      "<b>Например:</b> <code>BTC-Binance</code>",
                                "en": "<b>❗️ Exchange not found!</b>\n\n"
                                      "<b>Input coin name or coins for exchange in format:</b>\n\n"
                                      "<code>Coin</code>\n"
                                      "<code>Coin-Exchange</code>\n\n"
                                      "<b>For example:</b> <code>BTC-Binance</code>"
                            },
                            "coin_for_exchange_already_exists": {
                                "ru": "<b>❗️ Монета {coin} к бирже {exchange} уже в чёрном списке!</b>\n\n"
                                      "<b>Введите название монеты или монеты к бирже в формате:</b>\n\n"
                                      "<code>Монета</code>\n"
                                      "<code>Монета-Биржа</code>\n\n"
                                      "<b>Например:</b> <code>BTC-Binance</code>",
                                "en": "<b>❗️ Coin {coin} for exchange {exchange} is already in the blacklist!</b>\n\n"
                                      "<b>Input coin name or coins for exchange in format:</b>\n\n"
                                      "<code>Coin</code>\n"
                                      "<code>Coin-Exchange</code>\n\n"
                                      "<b>For example:</b> <code>BTC-Binance</code>"
                            }
                        },
                        "remove": {
                            "wrong_input_format": {
                                "ru": "<b>❗️ Неверный формат ввода!</b>\n\n"
                                      "<b>Введите название монеты или монеты к бирже для удаления в формате:</b>\n\n"
                                      "<code>Монета</code>\n"
                                      "<code>Монета-Биржа</code>\n\n"
                                      "<b>Например:</b> <code>BTC-Binance</code>\n\n",
                                "en": "<b>❗️ Wrong input format!</b>\n\n"
                                      "<b>Input coin name or coins for exchange to remove in format:</b>\n\n"
                                      "<code>Coin</code>\n"
                                      "<code>Coin-Exchange</code>\n\n"
                                      "<b>For example:</b> <code>BTC-Binance</code>\n\n"
                            },
                            "no_available_exchanges": {
                                "ru": "<b>❗️ Монеты {coin} нет в чёрном списке!</b>\n\n"
                                      "<b>Введите название монеты или монеты к бирже для удаления в формате:</b>\n\n"
                                      "<code>Монета</code>\n"
                                      "<code>Монета-Биржа</code>\n\n"
                                      "<b>Например:</b> <code>BTC-Binance</code>",
                                "en": "<b>❗️ Coin {coin} is not in the blacklist!</b>\n\n"
                                      "<b>Input coin name or coins for exchange to remove in format:</b>\n\n"
                                      "<code>Coin</code>\n"
                                      "<code>Coin-Exchange</code>\n\n"
                                      "<b>For example:</b> <code>BTC-Binance</code>"
                            },
                            "wrong_exchange": {
                                "ru": "<b>❗️ Биржа {exchange} к монете {coin} не найдена!</b>\n\n"
                                      "<b>Введите название монеты или монеты к бирже для удаления в формате:</b>\n\n"
                                      "<code>Монета</code>\n"
                                      "<code>Монета-Биржа</code>\n\n"
                                      "<b>Например:</b> <code>BTC-Binance</code>",
                                "en": "<b>❗️ Exchange {exchange} for coin {coin} not found!</b>\n\n"
                                      "<b>Input coin name or coins for exchange to remove in format:</b>\n\n"
                                      "<code>Coin</code>\n"
                                      "<code>Coin-Exchange</code>\n\n"
                                      "<b>For example:</b> <code>BTC-Binance</code>"
                            }
                        }
                    },
                    "success": {
                        "add_coin_for_exchange": {
                            "ru": "<b>✅ Монета {coin} к бирже {exchange} успешно добавлена в чёрный список!</b>\n\n",
                            "en": "<b>✅ Coin {coin} for exchange {exchange} successfully added to the blacklist!</b>\n\n"
                        },
                        "remove_coin_for_exchange": {
                            "ru": "<b>✅ Монета {coin} к бирже {exchange} успешно удалена из чёрного списка!</b>\n\n",
                            "en": "<b>✅ Coin {coin} for exchange {exchange} successfully removed from the blacklist!</b>\n\n"
                        }
                    }
                }
            }
        },
        "state": {
            "canceled_state": {
                "ru": "<b>❗ Действие отменено</b>",
                "en": "<b>❗ Action has been canceled</b>"
            },
        },
        "arbitrage": {
            "choose_arbitrage_type": {
                "ru": "<b>Выберите тип арбитража:</b>",
                "en": "<b>Select arbitrage type:</b>"
            },
            "day": {
                "ru": "д.",
                "en": "d."
            },
            "hour": {
                "ru": "ч.",
                "en": "h."
            },
            "minute": {
                "ru": "м.",
                "en": "m."
            },
            "seconds": {
                "ru": "с.",
                "en": "s."
            },
            "remain": {
                "ru": "осталось",
                "en": "remain"
            },
            "inter_exchange": {
                "active_subscription": {
                    "ru": "<b>✅ Подписка на межбиржевой арбитраж активная!</b>\n\n"
                          "Время подписки: <b>{subscription_status}</b>",
                    "en": "<b>✅ Inter-exchange arbitrage subscription is active!</b>\n\n"
                          "Subscription time: <b>{subscription_status}</b>"
                },
                "no_subscription": {
                    "ru": "<b>❗️ У вас нет подписки на межбиржевой арбитраж!</b>\n\n"
                          "Оформить подписку можно по команде <b>/subscriptions</b> или в меню бота.",
                    "en": "<b>❗️ You don't have a subscription for inter-exchange arbitrage!</b>\n\n"
                          "You can subscribe by using the command <b>/subscriptions</b> or in the bot menu."
                }
            }
        },
        "subscriptions": {
            "choose_arbitrage_type": {
                "ru": "<b>Выберите тип арбитража:</b>",
                "en": "<b>Select arbitrage type:</b>"
            },
            "inter_exchange": {
                "price_list_legacy": {
                    "ru": "<b>💳 Цены на подписки на межбиржевой арбитраж:</b>\n\n"
                          "<b>1 неделя:</b> <code>{one_week_price}$</code>\n"
                          "<b>1 месяц:</b> <code>{one_month_price}$</code>\n"
                          "<b>3 месяца:</b> <code>{three_month_price}$</code>\n"
                          "<b>НАВСЕГДА:</b> <code>{lifetime_price}$</code>\n\n\n"
                          "<b>USDT. Network - BSC (BEP20)</b>\n"
                          "<code>{bep20_address}</code>\n\n"
                          "<b>USDT. Network - Tron (TRC20)</b>\n"
                          "<code>{trc20_address}</code>\n\n"
                          "После оплаты сообщите в поддержку бота — отправьте скриншот транзакции с вашей "
                          "биржи/кошелька, или отправьте хеш транзакции.",
                    "en": "<b>💳 Prices for inter-exchange arbitrage subscriptions:</b>\n\n"
                          "<b>1 week:</b> <code>{1_week_price}$</code>\n"
                          "<b>1 month:</b> <code>{1_month_price}$</code>\n"
                          "<b>3 months:</b> <code>{3_month_price}$</code>\n"
                          "<b>LIFETIME:</b> <code>{lifetime_price}$</code>\n\n\n"
                          "<b>USDT. Network - BSC (BEP20)</b>\n"
                          "<code>{bep20_address}</code>\n\n"
                          "<b>USDT. Network - Tron (TRC20)</b>\n"
                          "<code>{trc20_address}</code>\n\n"
                          "After payment, please contact the bot support — send a screenshot of the transaction "
                          "from your exchange/wallet or send the transaction hash."
                },
                "price_list": {
                    "ru": "<b>💳 Цены на подписки на межбиржевой арбитраж:</b>\n\n"
                          "<b>1 неделя:</b> <code>{one_week_price}$</code>\n"
                          "<b>1 месяц:</b> <code>{one_month_price}$</code>\n"
                          "<b>3 месяца:</b> <code>{three_month_price}$</code>\n"
                          "<b>НАВСЕГДА:</b> <code>{lifetime_price}$</code>\n\n\n"
                          "<b>❕ Оплата в USDT BEP20/TRC20</b>"
                          "{current_subscription_message}\n\n\n"
                          "<b>ВЫБЕРИТЕ НИЖЕ ТИП ПОДПИСКИ, КОТОРЫЙ ХОТИТЕ ОФОРМИТЬ ⬇️</b>",
                    "en": "<b>💳 Prices for inter-exchange arbitrage subscriptions:</b>\n\n"
                          "<b>1 week:</b> <code>{one_week_price}$</code>\n"
                          "<b>1 month:</b> <code>{one_month_price}$</code>\n"
                          "<b>3 months:</b> <code>{three_month_price}$</code>\n"
                          "<b>LIFETIME:</b> <code>{lifetime_price}$</code>\n\n\n"
                          "<b>❕ Payment in USDT BEP20/TRC20</b>"
                          "{current_subscription_message}\n\n\n"
                          "<b>SELECT BELOW THE TYPE OF SUBSCRIPTION YOU WANT TO SUBSCRIBE TO ⬇️</b>"

                },
                "current_subscription_message": {
                    "ru": "\n\n<b>💎 У вас уже есть подписка на межбиржевой арбитраж!\n"
                          "Поэтому текущая подписка и оформленная подписка будут суммироваться</b>"
                },
                "confirm_payment": {
                    "ru": "<b>💳 Подтверждение выбраного типа подписки:</b>\n\n"
                          "<b>Тип арбитража:</b> <code>{arbitrage_type}</code>\n"
                          "<b>Время подписки:</b> <code>{subscription_type}</code>\n\n"
                          "❕ После нажатия кнопки <b>«💳 ОПЛАТИТЬ»</b> у вас будет <b>20 минут</b>, "
                          "чтобы оплатить выбранный вами тип подписки на сумму <b>не менее {price} USDT</b>\n\n"
                          "✅ Оплата определяется автоматически в течении 5 минут",
                    "en": "<b>💳 Confirmation of the selected subscription type:</b>\n\n"
                          "<b>Arbitrage type:</b> <code>{arbitrage_type}</code>\n"
                          "<b>Subscription time:</b> <code>{subscription_type}</code>\n\n"
                          "❕ After clicking the <b>«💳 PAY»</b> button, you will have <b>20 minutes</b> "
                          "to pay for the selected subscription type in the amount of <b>at least {price} USDT</b>\n\n"
                          "✅ Payment is automatically determined within 5 minutes"

                },
                "monitoring_payment": {
                    "ru": "<b>💳 Ожидание оплаты...</b>\n\n"
                          "⏳ У вас есть <b>{minutes} минут {seconds} секунд</b> на оплату подписки!\n\n"
                          "Тип арбитража: <code>{arbitrage_type}</code>\n"
                          "Время подписки: <code>{subscription_type}</code>\n"
                          "Сумма оплаты: <code>{price} USDT</code>\n\n\n"
                          "<b>ОПЛАТИТЕ НА ОДИН ИЗ АДРЕСОВ НИЖЕ</b>\n\n"
                          "<code>{usdt_bep20_address}</code>\n"
                          "<b>Монета - USDT. Сеть - BSC (BEP20)</b>\n\n"
                          "<code>{usdt_trc20_address}</code>\n"
                          "<b>Монета - USDT. Сеть - Tron (TRC20)</b>\n\n\n"
                          "🤖 Оплата будет автоматически определена в течении 5 минут после оплаты, "
                          "а подписка будет моментально "
                          "подключена после подтверждения оплаты в системе.",
                    "en": "<b>💳 Waiting for payment...</b>\n\n"
                          "⏳ You have <b>{minutes} minutes {seconds} seconds</b> to pay for the subscription!\n\n"
                          "Arbitrage type: <code>{arbitrage_type}</code>\n"
                          "Subscription time: <code>{subscription_type}</code>\n"
                          "Payment amount: <code>{price} USDT</code>\n\n\n"
                          "<b>PAY TO ONE OF THE ADDRESSES BELOW</b>\n\n"
                          "<code>{usdt_bep20_address}</code>\n"
                          "<b>Coin - USDT. Network - BSC (BEP20)</b>\n\n"
                          "<code>{usdt_trc20_address}</code>\n"
                          "<b>Coin - USDT. Network - Tron (TRC20)</b>\n\n\n"
                          "🤖 Payment will be automatically determined within 5 minutes after payment, "
                          "and the subscription will be instantly "
                          "connected after payment confirmation in the system."
                }
            }
        },
        "subscriptions_monitoring": {
            "notifications": {
                "time_reminder": {
                    "payment_pending": {
                        "ru": "<b>⏳ Внимание!</b>\n\n"
                              "До окончания времени проверки оплаты осталось {minutes_left} минут.\n\n"
                              "Тип арбитража: <code>{arbitrage_type}</code>\n"
                              "Время подписки: <code>{subscription_type}</code>\n"
                              "Сумма оплаты: <code>{subscription_price} USDT</code>\n\n\n"
                              "<b>ОПЛАТИТЕ НА ОДИН ИЗ АДРЕСОВ НИЖЕ</b>\n\n"
                              "<code>{usdt_bep20_address}</code>\n"
                              "<b>Монета - USDT. Сеть - BSC (BEP20)</b>\n\n"
                              "<code>{usdt_trc20_address}</code>\n"
                              "<b>Монета - USDT. Сеть - Tron (TRC20)</b>\n\n\n"
                              "🤖 Оплата будет автоматически определена в течении 5 минут после оплаты, "
                              "а подписка будет моментально "
                              "подключена после подтверждения оплаты в системе.",
                        "en": "<b>⏳ Attention!</b>\n\n"
                              "There are {minutes_left} minutes left until the end of the payment "
                              "verification time.\n\n"
                              "Arbitrage type: <code>{arbitrage_type}</code>\n"
                              "Subscription time: <code>{subscription_type}</code>\n"
                              "Payment amount: <code>{subscription_price} USDT</code>\n\n\n"
                              "<b>PAY TO ONE OF THE ADDRESSES BELOW</b>\n\n"
                              "<code>{usdt_bep20_address}</code>\n"
                              "<b>Coin - USDT. Network - BSC (BEP20)</b>\n\n"
                              "<code>{usdt_trc20_address}</code>\n"
                              "<b>Coin - USDT. Network - Tron (TRC20)</b>\n\n\n"
                              "🤖 Payment will be automatically determined within 5 minutes after payment, "
                              "and the subscription will be instantly "
                              "connected after payment confirmation in the system."
                    },
                    "payment_time_expired": {
                        "ru": "<b>⏳ Внимание!</b>\n\n"
                              "Время ожидания оплаты истекло!",
                        "en": "<b>⏳ Attention!</b>\n\n"
                              "Payment waiting time has expired!"
                    }

                },
                "pending_confirmation_trc20": {
                    "ru": "👍 <b>Оплата обнаружена!</b>\n\n"
                          "Оплачено: <code>{amount} USDT</code>\n\n"
                          "Хэш транзакции: <code>{transaction_hash}</code>\n\n"
                          "<b><a href='https://tronscan.org/#/transaction/{transaction_hash}'>"
                          "Посмотртеь в обозревателе</a></b>\n\n"
                          "Ожидается подтверждение транзакции в сети Tron (TRC20)...",
                    "en": "👍 <b>Payment detected!</b>\n\n"
                          "Paid: <code>{amount} USDT</code>\n\n"
                          "Transaction hash: <code>{transaction_hash}</code>\n\n"
                          "<b><a href='https://tronscan.org/#/transaction/{transaction_hash}'>"
                          "View in explorer</a></b>\n\n"
                          "Waiting for transaction confirmation in the Tron (TRC20) network..."
                },
                "insufficient_trc20": {
                    "ru": "❗️ <b>Оплачена недостаточная сумма!</b>\n\n"
                          "Цена подписки: <code>{subscription_price} USDT</code>\n"
                          "Оплачено: <code>{paid_amount} USDT</code>\n\n"
                          "Для активации подписки необходимо <b>ДОПЛАТИТЬ</b> <code>{missing_amount} USDT</code>\n\n"
                          "USDT (TRC20): <code>{usdt_trc20_address}</code>\n\n\n"
                          "<b>До окончания времени проверки оплаты осталось {available_minutes} минут "
                          "{available_seconds} секунд!</b>",
                    "en": "❗️ <b>Insufficient amount paid!</b>\n\n"
                          "Subscription price: <code>{subscription_price} USDT</code>\n"
                          "Paid: <code>{paid_amount} USDT</code>\n\n"
                          "To activate the subscription, you need to <b>TOP UP</b> <code>{missing_amount} USDT</code>\n\n"
                          "USDT (TRC20): <code>{usdt_trc20_address}</code>\n\n\n"
                          "<b>There are {available_minutes} minutes "
                          "{available_seconds} seconds left until the end of the payment verification time!</b>"
                },
                "payment_success_trc20": {
                    "ru": "🎉 <b>Оплата успешно подтверждена!</b>\n\n"
                          "Оплаченная сумма: <code>{current_usdt_trc20_balance} USDT</code>\n"
                          "Тип арбитража: <code>{arbitrage_type_message}</code>\n"
                          "Тип подписки: <code>{subscription_type_message}</code>\n\n"
                          "<b>Подписка успешно активирована!</b>",
                    "en": "🎉 <b>Payment successfully confirmed!</b>\n\n"
                          "Total paid amount: <code>{current_usdt_trc20_balance} USDT</code>\n"
                          "Arbitrage type: <code>{arbitrage_type_message}</code>\n"
                          "Subscription type: <code>{subscription_type_message}</code>\n\n"
                          "<b>Subscription successfully activated!</b>"
                }
            }
        }
    },
    "callback": {
        "language": {
            "language_changed": {
                "ru": "✅ Язык успешно изменён",
                "en": "✅ Language successfully changed"
            }
        },
        "exchange_changed": {
            "ru": "✅ Успешно изменено!",
            "en": "✅ Successfully changed!"
        },
        "network_speed": {
            "ru": "✅ Скорость сети успешно изменена!",
            "en": "✅ Network speed successfully changed!"
        },
        "no_changes": {
            "ru": "❕ Нет изменений!",
            "en": "❕ No changes!"
        },
        "no_subscription": {
            "ru": "❕ У вас нет подписки!",
            "en": "❕ You don't have a subscription!"
        },
        "successfully_changed": {
            "ru": "✅ Успешно изменено!",
            "en": "✅ Successfully changed!"
        },
        "notification": {
            "notification_enabled": {
                "ru": "🔔 Уведомления включены",
                "en": "🔔 Notifications enabled"
            },
            "notification_disabled": {
                "ru": "🔕 Уведомления отключены",
                "en": "🔕 Notifications disabled"
            }
        },
        "successfully_added": {
            "ru": "✅ Успешно добавлено!",
            "en": "✅ Successfully added!"
        },
        "successfully_removed": {
            "ru": "✅ Успешно удалено!",
            "en": "✅ Successfully removed!"
        },
        "referrals": {
            "referrals_statistics": {
                "withdraw": {
                    "errors": {
                        "zero_balance": {
                            "ru": "❗️ У вас недостаточно средств для вывода!",
                            "en": "❗️ You don't have enough funds to withdraw!"
                        },
                        "balance_less_than_5": {
                            "ru": "❗️ Минимальная сумма для вывода: 5$",
                            "en": "❗️ Minimum withdrawal amount: 5$"
                        },
                        "paid_subscriptions_quantity_less_than_2": {
                            "ru": "❗️ Вывод доступен после 2 оплат от приглашённых — в целях защиты от абуза!",
                            "en": "❗️ Withdrawal is available after 2 payments from referrals — to prevent abuse!"
                        }
                    }
                }
            }
        },
        "subscriptions": {
            "too_many_wallets": {
                "ru": "⚠️ Слишком много оплат на проверке. Попробуйте через {minutes} мин. {seconds} сек., "
                      "либо воспользуйтесь ручной оплатой.",
                "en": "⚠️ Too many payments under verification. Try again in {minutes} min. {seconds} sec. "
                      "or use manual payment."
            },
            "cancel_monitoring": {
                "ru": "✅ Проверка оплаты успешно отменена",
                "en": "✅ Payment verification has been successfully canceled"
            }
        },
        "state": {
            "canceled_state": {
                "ru": "❗ Действие отменено",
                "en": "❗ Action has been canceled"
            },
        }
    },
    "keyboard": {
        "menu": {
            "buttons": {
                "arbitrage": {
                    "ru": "🔍 Поиск связок",
                    "en": "🔍 Find pairs"
                },
                "settings": {
                    "ru": "⚙️ Настройки",
                    "en": "⚙️ Settings"
                },
                "referrals": {
                    "ru": "🔗 Реферальная программа",
                    "en": "🔗 Referral program"
                },
                "subscriptions": {
                    "ru": "💳 Подписки",
                    "en": "💳 Subscriptions"
                },
                "support": {
                    "ru": "👨‍💻 Поддержка",
                    "en": "👨‍💻 Support"
                }
            }
        },
        "language": {
            "buttons": {
                "russian": {
                    "ru": "Русский",
                    "en": "Русский"
                },
                "english": {
                    "ru": "English",
                    "en": "English"
                }
            }
        },
        "referrals": {
            "buttons": {
                "invite": {
                    "ru": "📲 Поделиться ссылкой",
                    "en": "📲 Share link"
                },
                "copy": {
                    "ru": "📋 Копировать ссылку",
                    "en": "📋 Copy link"
                },
                "statistics": {
                    "set_statistics": {
                        "ru": "📊 Статистика",
                        "en": "📊 Statistics"
                    },
                    "one_day": {
                        "ru": "1 день",
                        "en": "1 day"
                    },
                    "one_week": {
                        "ru": "1 неделя",
                        "en": "1 week"
                    },
                    "one_month": {
                        "ru": "1 месяц",
                        "en": "1 month"
                    },
                    "one_year": {
                        "ru": "1 год",
                        "en": "1 year"
                    },
                    "withdraw": {
                        "ru": "💰 Вывод средств",
                        "en": "💰 Withdraw funds"
                    },
                    "convert_to_subscription": {
                        "ru": "💳 Конвертировать в подписку",
                        "en": "💳 Convert to subscription"
                    },
                    "confirm_withdraw": {
                        "ru": "✅ Подтвердить вывод",
                        "en": "✅ Confirm withdrawal"
                    }
                }
            }
        },
        "settings": {
            "buttons": {
                "language": {
                    "ru": "🌍 Язык",
                    "en": "🌍 Language"
                },
                "exchanges": {
                    "ru": "💱 Биржи",
                    "en": "💱 Exchanges"
                },
                "spread": {
                    "ru": "🔀 Спред",
                    "en": "🔀 Spread"
                },
                "profit": {
                    "ru": "💵 Профит",
                    "en": "💵 Profit"
                },
                "volume": {
                    "ru": "📊 Объём",
                    "en": "📊 Volume"
                },
                "network_speed": {
                    "ru": "⏳ Скорость сети",
                    "en": "⏳ Network speed"
                },
                "contracts": {
                    "ru": "📜 Контракты",
                    "en": "📜 Contracts"
                },
                "withdraw_fee": {
                    "ru": "💰 Комиссия вывода",
                    "en": "💰 Withdrawal fee"
                },
                "volume_24h": {
                    "ru": "📈 24ч. оборот",
                    "en": "📈 24h turnover"
                },
                "last_trade_time": {
                    "ru": "⏰ Время последней торговли",
                    "en": "⏰ Last trade time"
                },
                "notification": {
                    "ru": "🔔 Уведомления",
                    "en": "🔔 Notifications"
                },
                "is_low_bids": {
                    "ru": "📉 Контроль ордеров",
                    "en": "📉 Order control"
                },
                "hedging_types": {
                    "ru": "⚖️ Типы хеджирования",
                    "en": "⚖️ Hedging types"
                },
                "blacklist_types": {
                    "ru": "🗑 Черный список",
                    "en": "🗑 Blacklist"
                }
            },
            "spread": {
                "set_max_spread": {
                    "ru": "⬇️ Установить максимальный спред",
                    "en": "⬇️ Set maximum spread"
                },
                "set_min_spread": {
                    "ru": "⬆️ Установить минимальный спред",
                    "en": "⬆️ Set minimum spread"
                },

            },
            "profit": {
                "set_min_profit": {
                    "ru": "⬇️ Установить минимальный профит",
                    "en": "⬇️ Set minimum profit"
                }
            },
            "volume": {
                "set_max_volume": {
                    "ru": "⬇️ Установить максимальный объём",
                    "en": "⬇️ Set maximum volume"
                }
            },
            "network_speed": {
                "undefined_network_on": {
                    "ru": "Неопределённая скорость сети: ВКЛ",
                    "en": "Undefined network speed: ON"
                },
                "undefined_network_off": {
                    "ru": "Неопределённая скорость сети: ВЫКЛ",
                    "en": "Undefined network speed: OFF"
                }
            },
            "contracts": {
                "contracts_match": {
                    "ru": "Контракты совпадают",
                    "en": "Contracts match"
                },
                "all_pairs": {
                    "ru": "Все связки",
                    "en": "All arbitrage pairs"
                }
            },
            "withdraw_fee": {
                "set_max_withdraw_fee": {
                    "ru": "⬇️ Установить максимальную комиссию вывода",
                    "en": "⬇️ Set maximum withdrawal fee"
                }
            },
            "coin_volume_24h": {
                "set_max_coin_volume_24h": {
                    "ru": "⬇️ Установить максимальный оборот за 24ч",
                    "en": "⬇️ Set maximum 24h turnover"
                },
                "set_min_coin_volume_24h": {
                    "ru": "⬆️ Установить минимальный оборот за 24ч",
                    "en": "⬆️ Set minimum 24h turnover"
                }

            },
            "last_trade_time": {
                "set_min_last_trade_time": {
                    "ru": "⬇️ Установить минимальное время",
                    "en": "⬇️ Set minimum last trade time"
                },
                "set_max_last_trade_time": {
                    "ru": "⬆️ Установить максимальное время",
                    "en": "⬆️ Set maximum last trade time"
                }
            },
            "notification": {
                "inter_exchange": {
                    "ru": "Межбиржевые уведомления",
                    "en": "Inter-exchange notifications"
                }
            },
            "is_low_bids": {
                "show_low_bids": {
                    "ru": "Показывать",
                    "en": "Show"
                },
                "hide_low_bids": {
                    "ru": "Скрыть",
                    "en": "Hide"
                }
            },
            "hedging_types": {
                "futures_hedging_type": {
                    "ru": "Фьючерсное хеджирование",
                    "en": "Futures hedging"
                },
                "margin_hedging_type": {
                    "ru": "Маржинальное хеджирование",
                    "en": "Margin hedging"
                },
                "loan_hedging_type": {
                    "ru": "Займовое хеджирование",
                    "en": "Loan hedging"
                },
                "futures_hedging": {
                    "hedging_only": {
                        "ru": "Только с фьючерсным хеджированием",
                        "en": "Futures hedging only"
                    },
                    "all_pairs": {
                        "ru": "Все связки",
                        "en": "All pairs"
                    }
                },
                "margin_hedging": {
                    "hedging_only": {
                        "ru": "Только с маржинальным хеджированием",
                        "en": "Margin hedging only"
                    },
                    "all_pairs": {
                        "ru": "Все связки",
                        "en": "All pairs"
                    }
                },
                "loan_hedging": {
                    "hedging_only": {
                        "ru": "Только с займовым хеджированием",
                        "en": "Loan hedging only"
                    },
                    "all_pairs": {
                        "ru": "Все связки",
                        "en": "All pairs"
                    }
                }

            },
            "blacklist_types": {
                "coins_blacklist_type": {
                    "ru": "Чёрный список монет",
                    "en": "Coins blacklist"
                },
                "networks_blacklist_type": {
                    "ru": "Чёрный список сетей",
                    "en": "Networks blacklist"
                },
                "coin_for_exchange_blacklist_type": {
                    "ru": "Чёрный список монет к биржи",
                    "en": "Coins blacklist for exchange"
                },
                "coins_blacklist": {
                    "add_coin": {
                        "ru": "➕ Добавить монету",
                        "en": "➕ Add coin"
                    },
                    "remove_coin": {
                        "ru": "➖ Удалить монету",
                        "en": "➖ Remove coin"
                    }
                },
                "networks_blacklist": {
                    "add_network": {
                        "ru": "➕ Добавить сеть",
                        "en": "➕ Add network"
                    },
                    "remove_network": {
                        "ru": "➖ Удалить сеть",
                        "en": "➖ Remove network"
                    }
                },
                "coin_for_exchange_blacklist": {
                    "add_coin_for_exchange": {
                        "ru": "➕ Добавить монету к бирже",
                        "en": "➕ Add coin for exchange"
                    },
                    "remove_coin_for_exchange": {
                        "ru": "➖ Удалить монету к бирже",
                        "en": "➖ Remove coin for exchange"
                    }
                }
            }
        },
        "arbitrage": {
            "buttons": {
                "inter_exchange": {
                    "ru": "Межбиржевой",
                    "en": "Inter-exchange"
                }
            }
        },
        "subscriptions": {
            "inter_exchange": {
                "buttons": {
                    "one_week": {
                        "ru": "1 неделя",
                        "en": "1 week"
                    },
                    "one_month": {
                        "ru": "1 месяц",
                        "en": "1 month"
                    },
                    "three_month": {
                        "ru": "3 месяца",
                        "en": "3 months"
                    },
                    "lifetime": {
                        "ru": "НАВСЕГДА",
                        "en": "LIFETIME"
                    }
                }
            },
            "pay": {
                "ru": "💳 Оплатить",
                "en": "💳 Pay"
            },
            "manual_payment": {
                "ru": "💳 Ручная оплата",
                "en": "💳 Manual payment"
            },
            "cancel_monitoring": {
                "ru": "❌ Отменить проверку оплаты",
                "en": "❌ Cancel payment verification"
            }
        }
    },
    "button": {
        "back": {
            "ru": "< Назад",
            "en": "< Back"
        },
        "buy_exchange": {
            "ru": "Биржа покупки:",
            "en": "Exchange buy:"
        },
        "sell_exchange": {
            "ru": "Биржа продажи:",
            "en": "Exchange sell:"
        },
        "most_often_blocked": {
            "ru": "🔻ЧАЩЕ ВСЕГО БЛОКИРУЮТ🔻",
            "en": "🔻MOST OFTEN BLOCKED🔻"
        },
        "last_blocked": {
            "ru": "🔻ПОСЛЕДНИЕ ЗАБЛОКИРОВАННЫЕ🔻",
            "en": "🔻LAST BLOCKED🔻"
        }
    }
}
