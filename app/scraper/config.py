# contains scraping configuration data for each bank
# list of banks with exchange info on their website as of oct18, 2024
# source: National bank of ethiopia, https://nbe.gov.et/financial-institutions/banks/
# ========================================================================================
# CODE |        Bank name              |             url
# ----------------------------------------------------------------------------------------
# CBET - Commercial Bank of Ethiopia    API https://combanketh.et/en/exchange-rate
# DEET - Development Bank of Ethiopia   https://dbe.com.et/
# AWIN - Awash Bank S.C.                https://awashbank.com/exchange-historical/
# DASH - Dashen Bank S.C.               https://dashenbanksc.com/daily-exchange-rates/
# ABYS - Bank of Abyssinia              https://www.bankofabyssinia.com/exchange-rate-2/
# WEGA - Wegagen Bank S.C.              https://www.wegagen.com/
# UNTD - Hibret Bank S.C.               https://www.hibretbank.com.et/
# NIBI - Nib Int. Bank S.C.             https://www.nibbanksc.com/exchange-rate/
# CBOR - Cooperative Bank of Oromia     https://coopbankoromia.com.et/daily-exchange-rates/
# LIBS - Lion Int. Bank S.C.            https://anbesabank.com/
# ORIR - Oromia Bank S.C.               https://www.oromiabank.com/
# ZEME - Zemen Bank S.C.                https://www.zemenbank.com/
# BUNA - Bunna Bank S.C                 https://bunnabanksc.com/
# BERH - Berhan Bank S.C.               https://berhanbanksc.com/
# ABAY - Abay Bank S.C.                 https://abaybank.com.et/
# ABSC - Addis Int. Bank S.C            https://addisbanksc.com/
# ENAT - Enat Bank S.C.                 https://www.enatbanksc.com/
# DEGA - Global Bank S.C                https://www.globalbankethiopia.com/
# ZEMZ - ZamZam Bank S.C.               https://zamzambank.com/exchange-rates/todays-exchange-rate/
# SBEE - Shabelle Bank S.C.             NO DATA
# GOBT - Goh Betoch Bank S.C.           https://www.gohbetbank.com/todays-exchange-rate/
# HIJR - Hijra Bank S.C.                https://hijra-bank.com/
# AHUU - Ahadu Bank S.C.                telegram https://t.me/ahadubanket
# SINQ - Siinqee Bank S.C.              telegram https://t.me/SiinqeeBanksc
# TSDY - Tsedey Bank S.C.               telegram https://t.me/tsedeybanksc
# TSCP - Tsehay Bank S.C.               https://tsehaybank.com.et/exchange-rate/
# AMHR - Amhara Bank S.C.               https://www.amharabank.com.et/exchange-rate/
# GDAA - Gadaa Bank S.C.                NO DATA
# OSCO - Omo Bank S.C.                  NO DATA
# SDMA - Sidama Bank S.C.               telegram https://t.me/sidamabanksc
# RMSI - Rammis Bank S.C.               telegram https://t.me/rammisbankk
# SKTE - Siket Bank S.C                 NO DATA

bank_url = {
    "CBET" : {
        'name': 'Commercial Bank of Ethiopia',
        "URL" : "https://combanketh.et/cbeapi/daily-exchange-rates"
    },
    "DEET" : {
        'name': 'Development Bank of Ethiopia',
        "URL": "https://dbe.com.et/"
    },
    "AWIN" : {
        'name': 'Awash Bank S.C.',
        "URL" : "https://awashbank.com/exchange-historical/"
    },
    "DASH" : {
        'name': 'Dashen Bank S.C.',
        "URL" : "https://dashenbanksc.com/daily-exchange-rates/"
    },
    "ABYS" : {
        'name': 'Bank of Abyssinia',
        "URL" : "https://www.bankofabyssinia.com/exchange-rate-2/"
    },
    "WEGA" : {
        'name': 'Wegagen Bank S.C.',
        "URL" : "https://weg.back.strapi.wegagen.com/api/exchange-rates?populate=*"
    },
    "UNTD" : {
        'name': 'Hibret Bank S.C.',
        "URL" : "https://www.hibretbank.com.et/"
    },
    "NIBI" : {
        'name': 'Nib Int. Bank S.C.',
        "URL" : "https://www.nibbanksc.com/exchange-rate/"
    },
    "CBOR" : {
        'name': 'Cooperative Bank of Oromia',
        "URL" : "https://coopbankoromia.com.et/daily-exchange-rates/"
    },
    "LIBS" : {
        'name': 'Lion Int. Bank S.C.',
        "URL" : "https://anbesabank.com/"
    },
    "ORIR" : {
        'name': 'Oromia Bank S.C.',
        "URL" : "https://www.oromiabank.com/"
    },
    "ZEME" : {
        'name': 'Zemen Bank S.C.',
        "URL" : "https://www.zemenbank.com/exchange-rates"
    },
    "BUNA" : {
        'name': 'Bunna Bank S.C',
        "URL" : "https://bunnabanksc.com/foreign-exchange/"
    },
    "BERH" : {
        'name': 'Berhan Bank S.C.',
        "URL" : "https://berhanbanksc.com/"
    },
    "ABAY" : {
        'name': 'Abay Bank S.C.',
        "URL" : "https://abaybank.com.et/exchange-rates/"
    },
    "ABSC" : {
        'name': 'Addis Int. Bank S.C',
        "URL" : "https://addisbanksc.com/"
    },
    "ENAT" : {
        'name': 'Enat Bank S.C.',
        "URL" : "https://www.enatbanksc.com/"
    },
    "DEGA" : {
        'name': 'Global Bank S.C',
        "URL" : "https://www.globalbankethiopia.com/"
    },
    "ZEMZ" : {
        'name': 'ZamZam Bank S.C.',
        "URL" : "https://zamzambank.com/exchange-rates/todays-exchange-rate/"
    },
    "GOBT" : {
        'name': 'Goh Betoch Bank S.C.',
        "URL" : "https://www.gohbetbank.com/todays-exchange-rate/"
    },
    "HIJR" : {
        'name': 'Hijra Bank S.C.',
        "URL" : "https://hijra-bank.com/"
    },
    "TSCP" : {
        'name': 'Tsehay Bank S.C.',
        "URL" : "https://tsehaybank.com.et/exchange-rate/"
    },
    "AMHR" : {
        'name': 'Amhara Bank S.C.',
        "URL" : "https://www.amharabank.com.et/exchange-rate/"
    }
}