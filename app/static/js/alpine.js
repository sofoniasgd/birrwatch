document.addEventListener('alpine:init', () => {
    Alpine.data('exchangeRates', () => ({
        cashRates: [],
        transactionalRates: [],
        bankNames: [],
        date: new Date().toISOString().split('T')[0], // Default to current date,
        sortKey: 'currency',  // Default sort by currency
        sortOrder: 'asc',     // Default sort order is ascending
        activeTab: 'cash',    // Default active tab is cash
        availableCurrencies: [], // List of all unique currencies
        selectedCurrency: 'All Currencies', // Currently selected currency
        filteredCashRates: [],
        filteredTransactionalRates: [],
        currencyMap: new Map(),
        bestRates: {}, // Best rates for key currencies

        async fetchData() {
            try {
                const response = await fetch(`/api/exchange_rates?date=${this.date}`);
                const data = await response.json();
                // get bank names from api call
                const bankNames = await fetch('/api/banks');
                const bankData = await bankNames.json();
                // get currency names from api call
                const currencyNames = await fetch('/api/currencies');
                // replace bank id with bank name from bankData
                data.cash_rates.forEach(rate => {
                    rate.bank_id = bankData.find(bank => bank.bank_id === rate.bank_id).name;
                });
                data.tx_rates.forEach(rate => {
                    rate.bank_id = bankData.find(bank => bank.bank_id === rate.bank_id).name;
                });
                // save currency names in a map
                const currencyData = await currencyNames.json();

                update_best_rates = async () => {
                    // Update bestRates based on selected currency
                    if (this.selectedCurrency !== 'All Currencies') {
                        const selectedCurrencyCode = this.selectedCurrency.split(' - ')[0];
                        const response = await fetch(`/api/best_rates/${selectedCurrencyCode}`);
                        const rates = await response.json();

                        // clear bestRates of any previous data
                        Object.keys(this.bestRates).forEach(key => {
                            delete this.bestRates[key];
                        });

                        this.bestRates[selectedCurrencyCode] = {
                            best_cash_buy: {
                                bank_name: bankData.find(bank => bank.bank_id === rates.best_cash_buy.bank_id).name,
                                cash_buy: rates.best_cash_buy.cash_buy
                            },
                            best_cash_sell: {
                                bank_name: bankData.find(bank => bank.bank_id === rates.best_cash_sell.bank_id).name,
                                cash_sell: rates.best_cash_sell.cash_sell
                            },
                            best_tx_buy: {
                                bank_name: bankData.find(bank => bank.bank_id === rates.best_tx_buy.bank_id).name,
                                tx_buy: rates.best_tx_buy.tx_buy
                            },
                            best_tx_sell: {
                                bank_name: bankData.find(bank => bank.bank_id === rates.best_tx_sell.bank_id).name,
                                tx_sell: rates.best_tx_sell.tx_sell
                            }
                        };
                    } else {
                        // get key currency best rates from api call
                        // use (USD, GBP, EUR, CAD, CNY) as key currencies
                        const keyCurrencies = ['USD', 'GBP', 'EUR', 'CAD', 'CNY'];
                        const bestRates = this.bestRates;
                        for (const currency of keyCurrencies) {
                            const response = await fetch(`/api/best_rates/${currency}`);
                            const rates = await response.json();

                            bestRates[currency] = {
                                best_cash_buy: {
                                    bank_name: bankData.find(bank => bank.bank_id === rates.best_cash_buy.bank_id).name,
                                    cash_buy: rates.best_cash_buy.cash_buy
                                },
                                best_cash_sell: {
                                    bank_name: bankData.find(bank => bank.bank_id === rates.best_cash_sell.bank_id).name,
                                    cash_sell: rates.best_cash_sell.cash_sell
                                },
                                best_tx_buy: {
                                    bank_name: bankData.find(bank => bank.bank_id === rates.best_tx_buy.bank_id).name,
                                    tx_buy: rates.best_tx_buy.tx_buy
                                },
                                best_tx_sell: {
                                    bank_name: bankData.find(bank => bank.bank_id === rates.best_tx_sell.bank_id).name,
                                    tx_sell: rates.best_tx_sell.tx_sell
                                }
                            };
                        }
                    }
                }
                update_best_rates();
                const currencyMap = new Map();
                currencyData.forEach(currency => {
                    currencyMap.set(currency.currency_code, currency.name);
                });
                // console.log(currencyMap);
                // replace currency code in data with currency code and name
                data.cash_rates.forEach(rate => {
                    rate.currency_code = `${rate.currency_code} - ${currencyMap.get(rate.currency_code)}`;
                });
                data.tx_rates.forEach(rate => {
                    rate.currency_code = `${rate.currency_code} - ${currencyMap.get(rate.currency_code)}`;
                });
                // data contains two lists for cash and transactional rates
                // split the data into two lists
                this.cashRates = data.cash_rates || [];
                //console.log(this.cashRates);
                this.transactionalRates = data.tx_rates || [];
                //console.log(this.transactionalRates);

                // Populate available currencies including currency code and name
                this.availableCurrencies = [...new Set(data.cash_rates.map(rate => rate.currency_code))];
                //console.log(this.availableCurrencies);

                // Apply initial filter
                this.filterRates();

                // Sort data after fetching
                this.sortData();
            } catch (error) {
                console.error("Error fetching exchange rates:", error);
            }
        },

        selectCurrency(currency) { 
            this.selectedCurrency = currency;
            update_best_rates();
            this.filterRates();
            this.sortData();
        },

        // Filters rates by selected currency
        filterRates() {
            if (this.selectedCurrency === 'All Currencies') {
                this.filteredCashRates = this.cashRates;
                this.filteredTransactionalRates = this.transactionalRates;
            } else if (this.selectedCurrency) {
                this.filteredCashRates = this.cashRates.filter(rate => rate.currency_code === this.selectedCurrency);
                this.filteredTransactionalRates = this.transactionalRates.filter(rate => rate.currency_code === this.selectedCurrency);
            }
        },

        setSort(key) {
            // Toggle sort order if the same column is clicked
            if (this.sortKey === key) {
                this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                this.sortKey = key;
                this.sortOrder = 'asc';
            }
            this.sortData();
        },

        sortData() {
            const sortFn = (a, b) => {
                let valueA = a[this.sortKey];
                let valueB = b[this.sortKey];
        
                // Check if values exist and are of the expected types
                if (valueA === undefined || valueB === undefined) {
                    return 0; // Skip sorting if either value is undefined
                }
        
                // Handle numerical sorting
                if (typeof valueA === 'number' && typeof valueB === 'number') {
                    return this.sortOrder === 'asc' ? valueA - valueB : valueB - valueA;
                }
        
                // Convert to strings in case values aren't of string type
                valueA = valueA.toString();
                valueB = valueB.toString();
        
                // Handle alphabetical sorting
                return this.sortOrder === 'asc'
                    ? valueA.localeCompare(valueB)
                    : valueB.localeCompare(valueA);
            };

            // Sort both tables by the chosen key and order
            this.filteredCashRates.sort(sortFn);
            this.filteredTransactionalRates.sort(sortFn);
        }
    }));
});
