import React, { useState } from 'react';
import { RecommendationForm } from './RecommendationForm';
import { RecommendationResult } from './RecommendationResult';
import { YieldForm } from './YieldForm';
import { YieldResult } from './YieldResult';
import { getCropRecommendation, getYieldEstimation } from '../../services/cropService';
import { RecommendationRequest, RecommendationResponse, YieldRequest, YieldResponse } from '../../types/crop';

export const CropDashboard: React.FC = () => {
  const [recState, setRecState] = useState<{
    isLoading: boolean;
    data: RecommendationResponse | null;
    error: string | null;
  }>({ isLoading: false, data: null, error: null });

  const [yieldState, setYieldState] = useState<{
    isLoading: boolean;
    data: YieldResponse | null;
    error: string | null;
  }>({ isLoading: false, data: null, error: null });

  const handleRecommendationSubmit = async (data: RecommendationRequest) => {
    setRecState({ isLoading: true, data: null, error: null });
    try {
      const result = await getCropRecommendation(data);
      setRecState({ isLoading: false, data: result, error: null });
    } catch (err: any) {
      setRecState({ isLoading: false, data: null, error: err.message });
    }
  };

  const handleYieldSubmit = async (data: YieldRequest) => {
    setYieldState({ isLoading: true, data: null, error: null });
    try {
      const result = await getYieldEstimation(data);
      setYieldState({ isLoading: false, data: result, error: null });
    } catch (err: any) {
      setYieldState({ isLoading: false, data: null, error: err.message });
    }
  };

  return (
    <div className="min-h-screen bg-canvas-sand p-4 md:p-8">
      <header className="mb-10 max-w-6xl mx-auto border-b-2 border-monsoon-blue pb-6">
        <h1 className="text-4xl md:text-5xl text-monsoon-blue font-bold mb-2">KrishiAI+</h1>
        <p className="text-xl text-monsoon-blue/80">Agricultural Decision Support</p>
      </header>

      <main className="max-w-6xl mx-auto space-y-12">
        <section>
          <h2 className="text-3xl text-monsoon-blue font-bold mb-6 flex items-center">
            <span className="bg-monsoon-blue text-canvas-sand px-3 py-1 mr-4 text-xl">1</span>
            Crop Recommendation
          </h2>
          
          {recState.error && (
            <div className="bg-surface-paper border-l-4 border-earthen-clay p-4 mb-6">
              <p className="text-earthen-clay font-medium">{recState.error}</p>
            </div>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
            <RecommendationForm onSubmit={handleRecommendationSubmit} isLoading={recState.isLoading} />
            <RecommendationResult result={recState.data} />
          </div>
        </section>

        <section>
          <h2 className="text-3xl text-monsoon-blue font-bold mb-6 flex items-center">
            <span className="bg-monsoon-blue text-canvas-sand px-3 py-1 mr-4 text-xl">2</span>
            Yield & Revenue Estimation
          </h2>
          
          {yieldState.error && (
            <div className="bg-surface-paper border-l-4 border-earthen-clay p-4 mb-6">
              <p className="text-earthen-clay font-medium">Validation Error: {yieldState.error}</p>
            </div>
          )}

          <div className="flex flex-col">
            <YieldForm 
              onSubmit={handleYieldSubmit} 
              isLoading={yieldState.isLoading} 
              recommendedCrop={recState.data?.recommended_crop || null} 
            />
            <YieldResult result={yieldState.data} />
          </div>
        </section>
      </main>
    </div>
  );
};
