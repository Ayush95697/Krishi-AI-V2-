import React, { useState, useEffect } from 'react';
import { YieldRequest } from '../../types/crop';

interface YieldFormProps {
  onSubmit: (data: YieldRequest) => void;
  isLoading: boolean;
  recommendedCrop: string | null;
}

export const YieldForm: React.FC<YieldFormProps> = ({ onSubmit, isLoading, recommendedCrop }) => {
  const [formData, setFormData] = useState<YieldRequest>({
    crop: '',
    state: '',
    season: '',
    crop_year: new Date().getFullYear(),
    annual_rainfall: 0,
    fertilizer: 0,
    pesticide: 0,
    area: 0,
  });

  useEffect(() => {
    if (recommendedCrop) {
      setFormData((prev) => ({ ...prev, crop: recommendedCrop.charAt(0).toUpperCase() + recommendedCrop.slice(1) }));
    }
  }, [recommendedCrop]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    const isNumeric = ['crop_year', 'annual_rainfall', 'fertilizer', 'pesticide', 'area'].includes(name);
    setFormData((prev) => ({
      ...prev,
      [name]: isNumeric ? (parseFloat(value) || 0) : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="bg-surface-paper border-2 border-monsoon-blue p-6">
      <h2 className="text-2xl mb-6">Yield & Revenue Estimation</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div>
            <label className="block mb-1 font-medium">Crop</label>
            <input type="text" name="crop" value={formData.crop} onChange={handleChange} required className="w-full border border-earthen-clay p-2 focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">State</label>
            <input type="text" name="state" value={formData.state} onChange={handleChange} required className="w-full border border-earthen-clay p-2 focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" placeholder="e.g. Uttar Pradesh" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Season</label>
            <input type="text" name="season" value={formData.season} onChange={handleChange} required className="w-full border border-earthen-clay p-2 focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" placeholder="e.g. Kharif" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Crop Year</label>
            <input type="number" name="crop_year" value={formData.crop_year || ''} onChange={handleChange} required min="2000" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          
          <div>
            <label className="block mb-1 font-medium">Annual Rain <span className="text-sm font-normal">(mm)</span></label>
            <input type="number" name="annual_rainfall" value={formData.annual_rainfall || ''} onChange={handleChange} required min="0" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Fertilizer <span className="text-sm font-normal">(kg)</span></label>
            <input type="number" name="fertilizer" value={formData.fertilizer || ''} onChange={handleChange} required min="0" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Pesticide <span className="text-sm font-normal">(kg)</span></label>
            <input type="number" name="pesticide" value={formData.pesticide || ''} onChange={handleChange} required min="0" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
          <div>
            <label className="block mb-1 font-medium">Area <span className="text-sm font-normal">(hectares)</span></label>
            <input type="number" name="area" value={formData.area || ''} onChange={handleChange} required min="0.1" step="0.1" className="w-full border border-earthen-clay p-2 font-data focus:outline-none focus:ring-2 focus:ring-earthen-clay bg-transparent" />
          </div>
        </div>
        <button 
          type="submit" 
          disabled={isLoading}
          className="w-full md:w-auto bg-monsoon-blue text-canvas-sand py-3 px-8 font-semibold hover:bg-opacity-90 transition-opacity disabled:opacity-50 mt-4"
        >
          {isLoading ? 'Estimating...' : 'Estimate Yield'}
        </button>
      </form>
    </div>
  );
};
