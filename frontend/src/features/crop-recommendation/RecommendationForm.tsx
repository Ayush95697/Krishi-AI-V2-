import React, { useState } from 'react';
import { RecommendationRequest } from '../../types/crop';

interface RecommendationFormProps {
  onSubmit: (data: RecommendationRequest) => void;
  isLoading: boolean;
}

export const RecommendationForm: React.FC<RecommendationFormProps> = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState<RecommendationRequest>({
    N: 0,
    P: 0,
    K: 0,
    temperature: 0,
    humidity: 0,
    ph: 0,
    rainfall: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseFloat(value) || 0,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-surface-paper border-2 border-monsoon-blue p-6">
      <h2 className="text-2xl mb-6">Field Conditions</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block mb-1 font-medium">Nitrogen (N) <span className="text-sm font-normal">(mg/kg)</span></label>
            <input type="number" name="N" value={formData.N || ''} onChange={handleChange} required min="0" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Phosphorus (P) <span className="text-sm font-normal">(mg/kg)</span></label>
            <input type="number" name="P" value={formData.P || ''} onChange={handleChange} required min="0" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Potassium (K) <span className="text-sm font-normal">(mg/kg)</span></label>
            <input type="number" name="K" value={formData.K || ''} onChange={handleChange} required min="0" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Temperature <span className="text-sm font-normal">(°C)</span></label>
            <input type="number" name="temperature" value={formData.temperature || ''} onChange={handleChange} required min="-10" max="60" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Humidity <span className="text-sm font-normal">(%)</span></label>
            <input type="number" name="humidity" value={formData.humidity || ''} onChange={handleChange} required min="0" max="100" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">pH Level</label>
            <input type="number" name="ph" value={formData.ph || ''} onChange={handleChange} required min="0" max="14" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div className="md:col-span-2">
            <label className="block mb-1 font-medium">Rainfall <span className="text-sm font-normal">(mm)</span></label>
            <input type="number" name="rainfall" value={formData.rainfall || ''} onChange={handleChange} required min="0" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
        </div>
        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full bg-monsoon-blue text-canvas-sand py-3 px-4 font-semibold hover:bg-opacity-90 transition-opacity disabled:opacity-50 mt-4"
        >
          {isLoading ? 'Analyzing Field...' : 'Analyze Field'}
        </button>
      </form>
    </div>
  );
};
