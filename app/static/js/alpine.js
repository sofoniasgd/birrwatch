document.addEventListener('alpine:init', () => {
    Alpine.data('exchangeRates', () => ({
        cashRates: [],
        transactionalRates: [],
        date: new Date().toISOString().split('T')[0], // Default to current date,
        sortKey: 'currency',  // Default sort by currency
        sortOrder: 'asc',     // Default sort order is ascending
        activeTab: 'cash',    // Default active tab is cash
        availableCurrencies: [], // List of all unique currencies
        selectedCurrency: 'All Currencies', // Currently selected currency
        filteredCashRates: [],
        filteredTransactionalRates: [],

        async fetchData() {
            try {
                const response = await fetch(`/api/exchange_rates?date=${this.date}`);
                const data = await response.json();
                
                // data contains two lists for cash and transactional rates
                // split the data into two lists
                this.cashRates = data.cash_rates || [];
                console.log(this.cashRates);
                this.transactionalRates = data.tx_rates || [];
                console.log(this.transactionalRates);

                // Populate available currencies
                this.availableCurrencies = [...new Set(data.cash_rates.map(rate => rate.currency_code))];
                console.log(this.availableCurrencies);

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
            this.filterRates();
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
            this.cashRates.sort(sortFn);
            this.transactionalRates.sort(sortFn);
        }
    }));
});
