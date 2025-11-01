# Business Insights

This document synthesises the key insights derived from the exploratory analysis and forecasting conducted on the synthetic pharma sales dataset.  Although the data are simulated, they are designed to mirror realistic patterns observed in pharmaceutical markets, including seasonality, product mix concentration and promotion effects.

## Seasonality

The monthly sales trend and seasonality curves reveal clear patterns tied to therapeutic classes.  For example, demand peaks in the first quarter (January–March) correspond to cold and flu remedies, while a second uptick during April–August reflects allergy season.  Understanding these cycles enables supply chain teams to plan inventory levels proactively and align marketing campaigns with expected surges in demand.

## Product Mix & Pareto Analysis

Sales are highly concentrated among a relatively small subset of products.  A Pareto analysis shows that roughly 20 percent of SKUs account for around 80 percent of total revenue.  This concentration suggests that focusing resources on the best‑selling molecules—ensuring availability, negotiating favourable prices, and monitoring competitive activity—will yield the greatest return on investment.  Conversely, a long tail of low‑volume products may be candidates for rationalisation or alternative distribution strategies.

## Therapeutic Class Concentration

The ATC breakdown highlights which categories dominate revenue.  In the synthetic data, general analgesics and anti‑inflammatory drugs represent a large share of sales, while niche categories such as oncology contribute relatively little volume.  This distribution helps management prioritise R&D investments, marketing spend and partner negotiations in line with the most lucrative therapeutic areas.

## Price Elasticity

The price‑vs‑demand scatter plot indicates a mild negative relationship between unit price and quantity sold, consistent with modest price elasticity.  Products with higher prices tend to sell fewer units, but the relationship is not overly steep—suggesting that customers are somewhat sensitive to price changes but still value branded medicines and are willing to pay a premium within reasonable bounds.  Promotional activity, represented by the `promo_days` feature, can temporarily boost sales and should be timed strategically around seasonal peaks.

## Forecasting Takeaways

The SARIMA and XGBoost models offer complementary forecasting perspectives.  SARIMA, a purely statistical time series approach, captures recurring seasonal patterns and performs reliably on products with stable histories.  The machine learning approach incorporates exogenous variables (price, promotions) and can adapt to non‑linear relationships, often yielding lower forecast error on products with more volatile sales.  Combining both approaches (e.g. through simple averaging) may further improve accuracy and robustness.

These insights feed directly into dashboard design in Tableau: stakeholders can monitor seasonal trends, identify top performers, assess category share, and view forward‑looking projections in a single pane of glass.  The underlying code and methodology are reproducible and can be extended to real transactional datasets with minimal modification.
