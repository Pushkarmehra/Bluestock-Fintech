-- 1.
SELECT
    fund_house,
    MAX(aum_crore) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 5;
-- 2. 
SELECT
    d.year,
    d.month,
    ROUND(AVG(f.nav), 2) AS avg_nav
FROM fact_nav f
JOIN dim_date d
ON f.date = substr(d.date,1,10)
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 3. 
SELECT
    SUBSTR(month,1,4) AS year,
    SUM(sip_inflow_crore) AS total_sip
FROM fact_sip_industry
GROUP BY year
ORDER BY year;
-- 4. 
SELECT
    transaction_type,
    COUNT(*) AS num_transactions,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY transaction_type;
-- 5. 
SELECT
    amfi_code,
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1;

-- 6.
SELECT
    scheme_name,
    return_1yr_pct
FROM fact_performance
ORDER BY return_1yr_pct DESC
LIMIT 10;

-- 7.
SELECT
    amfi_code,
    ROUND(AVG(nav),2) AS avg_nav
FROM fact_nav
GROUP BY amfi_code
ORDER BY avg_nav DESC;
-- 8.
SELECT
    stock_symbol,
    sector,
    weight_pct
FROM fact_portfolio
ORDER BY weight_pct DESC
LIMIT 10;
-- 9.
SELECT
    fund_house,
    COUNT(*) AS total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC;
-- 10.
SELECT
    scheme_name,
    sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;