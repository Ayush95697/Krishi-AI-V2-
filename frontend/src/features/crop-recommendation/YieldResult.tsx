import React from 'react';
import { YieldResponse } from '../../types/crop';

interface YieldResultProps {
  result: YieldResponse | null;
}

export const YieldResult: React.FC<YieldResultProps> = ({ result }) => {
  if (!result) {
    return null;
  }

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 }).format(num);
  };
  
  const formatCurrency = (num: number) => {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(num);
  };

  return (
    <div className="bg-surface-paper border-2 border-monsoon-blue p-6 mt-6 border-t-8 border-t-harvest-green">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <p className="text-sm uppercase tracking-wide text-monsoon-blue/70 mb-1 font-semibold">Predicted Yield</p>
          <p className="text-3xl font-data text-monsoon-blue">{formatNumber(result.predicted_yield_per_unit_area)} <span className="text-lg font-sans">kg / hectare</span></p>
        </div>
        
        <div>
          <p className="text-sm uppercase tracking-wide text-monsoon-blue/70 mb-1 font-semibold">Estimated Production</p>
          <p className="text-3xl font-data text-monsoon-blue">{formatNumber(result.estimated_production_kg)} <span className="text-lg font-sans">kg total</span></p>
        </div>

        <div className="md:col-span-2 pt-4 border-t border-monsoon-blue/20">
          <p className="text-sm uppercase tracking-wide text-monsoon-blue/70 mb-1 font-semibold">Market Estimation</p>
          {result.estimated_revenue !== null && result.price_per_kg !== null ? (
            <div>
              <p className="text-4xl font-data text-harvest-green mb-2">{formatCurrency(result.estimated_revenue)}</p>
              <p className="text-monsoon-blue/80">Based on a market price of {formatCurrency(result.price_per_kg)} per kg.</p>
            </div>
          ) : (
            <div className="bg-canvas-sand border border-earthen-clay/30 p-4 mt-2">
              <p className="text-monsoon-blue">Market price data isn't available for this crop yet in the selected region and season.</p>
            </div>
          )}
          {result.note && (
            <p className="text-sm text-monsoon-blue/60 italic mt-4">{result.note}</p>
          )}
        </div>
      </div>
    </div>
  );
};
