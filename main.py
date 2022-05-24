import pandas as pd

# get url for each market price type
price_url = {
    "Farm Price": "https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=04&PricingDt=2022/5/24&PricingDtPrev=2022/5/21",
    "Wholesale Price": "https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=01&PricingDt=2022/5/24&PricingDtPrev=2022/5/21",
    "Retail Price": "https://sdvi2.fama.gov.my/price/direct/price/daily_commodityRpt.asp?Pricing=A&LevelCd=03&PricingDt=2022/5/24&PricingDtPrev=2022/5/21"
    }

final_df = pd.DataFrame()

# for each page
for k in price_url.keys():
    # print(f"Table {k}")
    url = price_url[k]
    df_list = pd.read_html(url)
    i = 1
    #print(len(df_list))

    # for each table in the page
    for df in df_list[1:]:
        # print(i)
        # print(df.head())
        
        if i % 2 != 0:
            centre_name = df.iloc[:,0].item().split(" : ")[1]
        else:
            df = df.drop([0,1])
            df.columns = ["Variety Name", "Grade", "Unit", "Max Price", "Average Price", "Min. Price"]
            df[["Max Price","Average Price", "Min. Price"]] = df[["Max Price","Average Price", "Min. Price"]].astype("float")
            df.insert(0, "Market Price Type", k)
            df.insert(1, "Centre", centre_name)
            df["Unit"] = df["Unit"].replace(to_replace=r"^.*KILOGRAM$", value="KG", regex=True)

            # print(df.head())
            final_df = pd.concat([final_df, df], ignore_index=True)
            # print(final_df)

        i += 1
    
    final_df.to_csv("price.csv", index=False)
