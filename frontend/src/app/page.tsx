'use client';

import { useState } from 'react';

export default function HomePage() {
  const [prediction, setPrediction] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    const formData = new FormData(e.target as HTMLFormElement);
    
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });
      
      const html = await response.text();
      // Extract prediction result from HTML response
      const match = html.match(/Review is (Real|Fake)/);
      setPrediction(match ? match[0] : 'Unable to get prediction');
    } catch (error) {
      setPrediction('Error making prediction');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-3xl w-full bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full mb-6">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 className="text-4xl font-bold mb-4 text-gray-900 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Fake Review Detection
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Advanced AI-powered system to detect fake Amazon reviews with high accuracy
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-8">
          <div className="space-y-2">
            <label htmlFor="news" className="block text-sm font-semibold text-gray-700">
              Review Text
            </label>
            <textarea
              name="news"
              id="news"
              placeholder="Enter the review text you want to analyze..."
              rows={6}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none text-gray-700 placeholder-gray-400"
              required
            />
            <p className="text-xs text-gray-500">Minimum 10 characters required for accurate analysis</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-2">
              <label htmlFor="rating" className="block text-sm font-semibold text-gray-700">
                Product Rating
              </label>
              <div className="relative">
                <input
                  type="number"
                  name="rating"
                  id="rating"
                  min="1"
                  max="5"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
                  placeholder="1-5"
                  required
                />
                <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                  <span className="text-yellow-400">★</span>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="verified_options" className="block text-sm font-semibold text-gray-700">
                Verified Purchase
              </label>
              <select
                name="verified_options"
                id="verified_options"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 bg-white"
              >
                <option value="Y">✓ Verified</option>
                <option value="N">✗ Not Verified</option>
              </select>
            </div>

            <div className="space-y-2">
              <label htmlFor="category_options" className="block text-sm font-semibold text-gray-700">
                Product Category
              </label>
              <select
                name="category_options"
                id="category_options"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200 bg-white"
              >
                <option value="Electronics">📱 Electronics</option>
                <option value="Books">📚 Books</option>
                <option value="Apparel">👕 Apparel</option>
                <option value="Home">🏠 Home & Garden</option>
                <option value="Beauty">💄 Beauty</option>
                <option value="Sports">⚽ Sports</option>
                <option value="Toys">🧸 Toys</option>
                <option value="Automotive">🚗 Automotive</option>
                <option value="Health & Personal Care">💊 Health & Personal Care</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-4 px-6 rounded-xl hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] font-semibold text-lg shadow-lg"
          >
            {isLoading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Analyzing Review...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span>Analyze Review</span>
              </div>
            )}
          </button>
        </form>

        {prediction && (
          <div className="mt-8 p-6 bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl border border-gray-200">
            <div className="flex items-center space-x-3 mb-3">
              <div className={`w-4 h-4 rounded-full ${
                prediction.includes('Real') ? 'bg-green-500' : 'bg-red-500'
              }`}></div>
              <h3 className="text-lg font-semibold text-gray-900">Analysis Result</h3>
            </div>
            <p className={`text-2xl font-bold ${
              prediction.includes('Real') 
                ? 'text-green-600 bg-green-50 border border-green-200' 
                : 'text-red-600 bg-red-50 border border-red-200'
            } px-4 py-3 rounded-lg inline-block`}>
              {prediction}
            </p>
            <p className="text-sm text-gray-600 mt-3">
              This prediction is based on advanced machine learning analysis of review patterns.
            </p>
          </div>
        )}

        <div className="mt-8 pt-6 border-t border-gray-200 text-center space-y-2">
          <div className="flex justify-center space-x-6 text-sm text-gray-500">
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Backend API: localhost:8000</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>Frontend: localhost:3000</span>
            </div>
          </div>
          <p className="text-xs text-gray-400">
            Powered by NLTK & Scikit-learn | Built with Next.js & FastAPI
          </p>
        </div>
      </div>
    </div>
  );
}
