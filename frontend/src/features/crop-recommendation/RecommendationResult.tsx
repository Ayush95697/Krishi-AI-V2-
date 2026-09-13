import React from 'react';
import { RecommendationResponse } from '../../types/crop';

interface RecommendationResultProps {
  result: RecommendationResponse | null;
}

export const RecommendationResult: React.FC<RecommendationResultProps> = ({ result }) => {
  if (!result) {
    return (
      <div className="bg-surface-paper border-2 border-monsoon-blue p-6 h-full flex items-center justify-center text-monsoon-blue/70">
        <p>Enter field conditions to see a crop recommendation.</p>
      </div>
    );
  }

  const confidencePercentage = (result.confidence * 100).toFixed(0);

  return (
    <div className="bg-surface-paper border-2 border-monsoon-blue p-6 h-full flex flex-col">
      <h2 className="text-2xl mb-6">Recommendation</h2>
      
      <div className="mb-8">
        <p className="text-sm uppercase tracking-wide text-earthen-clay mb-2 font-semibold">Primary Match</p>
        <div className="bg-harvest-green text-canvas-sand p-6 border-b-4 border-monsoon-blue">
          <h3 className="text-4xl capitalize mb-2">{result.recommended_crop}</h3>
          <p className="font-data text-lg">Confidence: {confidencePercentage}%</p>
        </div>
      </div>

      <div>
        <p className="text-sm uppercase tracking-wide text-turmeric-gold mb-3 font-semibold">Viable Alternatives</p>
        <ul className="space-y-3">
          {result.top_3_alternatives.map((alt, idx) => (
            <li key={idx} className="flex justify-between items-center border-b border-monsoon-blue/20 pb-2">
              <span className="capitalize text-lg">{idx + 1}. {alt.crop}</span>
              <span className="font-data">{(alt.probability * 100).toFixed(0)}%</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};
