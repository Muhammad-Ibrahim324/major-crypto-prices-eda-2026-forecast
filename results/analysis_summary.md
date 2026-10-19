# Snapshot findings and forecast interpretation

Author: Muhammad Ibrahim Shahrukh

Historical observations: 17,479. Completed data end 2026-10-18. Forecast horizon: 74 calendar days.

- **BTC:** last close $82,017.601562; selected **Last price**; December 31 projection $82,017.601562 (+0.00%). Illustrative band $58,570.930609–$114,850.266098. Held-out WAPE 17.19%; MAE $13,355.086782; MAE skill versus last price +0.0%; band test coverage 86.5%.
- **ETH:** last close $2,408.741455; selected **Extra Trees**; December 31 projection $2,420.526918 (+0.49%). Illustrative band $1,556.718033–$3,763.655613. Held-out WAPE 22.97%; MAE $555.435145; MAE skill versus last price -7.3%; band test coverage 67.6%.
- **BNB:** last close $722.255371; selected **Last price**; December 31 projection $722.255371 (+0.00%). Illustrative band $524.752100–$994.093823. Held-out WAPE 16.70%; MAE $118.943973; MAE skill versus last price +0.0%; band test coverage 74.3%.
- **XRP:** last close $1.304955; selected **Last price**; December 31 projection $1.304955 (+0.00%). Illustrative band $0.920230–$1.850525. Held-out WAPE 22.19%; MAE $0.297805; MAE skill versus last price +0.0%; band test coverage 43.2%.
- **USDT:** last close $0.998815; selected **Last price**; December 31 projection $0.998815 (+0.00%). Illustrative band $0.997502–$1.000130. Held-out WAPE 0.06%; MAE $0.000572; MAE skill versus last price +0.0%; band test coverage 75.7%.

The strongest full-common-period pairwise return correlation is BTC / ETH (0.782). Correlation can change during stress.

## Reading these results

A selected model can still lose to last price in the untouched test. Selection is not revised using that result. Flat forecasts are valid baseline outputs, not evidence that future prices will stay constant.
USDT is evaluated around its dollar peg. A small expected deviation does not rule out a future depeg or liquidity event.
Forecast direction reflects fitted historical patterns, not a fundamental valuation or a probability of profit. News, regulation, market liquidity, token events and macroeconomic shocks are absent from the features.
The illustrative bands rely on only three validation paths and a square-root-time error assumption. They omit many sources of model and data risk; their nominal 90th-percentile construction does not ensure 90% future coverage.

## Next research steps

Add more historical rolling origins, compare across market regimes, evaluate an independently sourced market feed, and test alternative direct models under the same untouched holdout protocol. Any trading study must include fees, slippage and realistic execution timing.