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
                    "<b>[/start,  /menu,  /arbitrage, /settings,\n"
                    "/language,  /referral_program,  /help ]</b>"
                ),
                "en": (
                    "🚀 <b>Arbitrage Screener</b>\n\n"
                    "- More than 20 crypto exchanges\n"
                    "- Updates every 5 seconds\n"
                    "- Advanced filtering\n\n"
                    "🎁 Invite users and get rewards\n\n"
                    "💬 Use buttons or commands:\n"
                    "<b>[/start,  /menu,  /arbitrage, /settings,\n"
                    "/language,  /referral_program,  /help ]</b>"
                )
            }
        },
        "menu": {
            "ru": "<b>МЕНЮ:</b>",
            "en": "<b>MENU:</b>"
        },
        "referrals": {
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
                  "📌 Bonuses are credited automatically after each payment."
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
            }
        },
        "state": {
            "canceled_state": {
                "ru": "<b>❗ Действие отменено</b>",
                "en": "<b>❗ Action has been canceled</b>"
            },
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
        }
    }
}
