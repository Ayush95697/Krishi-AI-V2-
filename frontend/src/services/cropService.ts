import axios, { AxiosError } from 'axios';
import { RecommendationRequest, RecommendationResponse, YieldRequest, YieldResponse } from '../types/crop';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getCropRecommendation = async (data: RecommendationRequest): Promise<RecommendationResponse> => {
  try {
    const response = await apiClient.post<RecommendationResponse>('/recommend-crop', data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Failed to get recommendation');
    }
    throw error;
  }
};

export const getYieldEstimation = async (data: YieldRequest): Promise<YieldResponse> => {
  try {
    const response = await apiClient.post<YieldResponse>('/estimate-yield-and-revenue', data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Expecting detail to specify which field was wrong per backend contract
      throw new Error(error.response?.data?.detail || 'Failed to estimate yield');
    }
    throw error;
  }
};
