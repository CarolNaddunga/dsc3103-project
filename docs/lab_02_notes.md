# Lab 02 Notes

I changed [specific values — e.g., "missing market values were imputed as 'Unknown' 
rather than dropped, to preserve the price data in those rows"] and normalized 
inconsistent commodity spellings (e.g., "MAIZE", "maize " → "Maize") since these 
were clearly the same category written differently, not genuine data errors.

I distinguished an outlier from an error by [e.g., "using the price histogram from 
the profiler — values that were far from the distribution but still positive and 
plausible were treated as outliers and kept, while negative prices were treated as 
errors and rejected, since a negative price is impossible rather than just extreme"].

If this data were later used for prediction, leakage would occur if [e.g., "we 
imputed missing values using information computed from the full dataset (including 
future records) rather than only data available at prediction time — for example, 
filling missing prices using the overall mean price would leak future information 
into rows that occurred earlier"].