export interface RecommendationRequest {
  N: number;
  P: number;
  K: number;
  temperature: number;
  humidity: number;
  ph: number;
  rainfall: number;
}

export interface AlternativeCrop {
  crop: string;
  probability: number;
}

export interface RecommendationResponse {
  recommended_crop: string;
  confidence: number;
  top_3_alternatives: AlternativeCrop[];
}

export interface YieldRequest {
  crop: string;
  state: string;
  season: string;
  crop_year: number;
  annual_rainfall: number;
  fertilizer: number;
  pesticide: number;
  area: number;
}

export interface YieldResponse {
  predicted_yield_per_unit_area: number;
  estimated_production_kg: number;
  price_per_kg: number | null;
  estimated_revenue: number | null;
  note: string;
}

export interface ApiError {
  detail: string;
}
