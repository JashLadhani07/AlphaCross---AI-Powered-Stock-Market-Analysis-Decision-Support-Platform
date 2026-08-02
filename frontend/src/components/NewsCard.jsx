import React, { useState, useEffect } from 'react';
import { Newspaper, TrendingUp, TrendingDown, Minus, AlertTriangle, ExternalLink } from 'lucide-react';
import api from '../api/api';

const NewsCard = ({ symbol, preloadedNews = null }) => {
  const [news, setNews] = useState(preloadedNews);
  const [loading, setLoading] = useState(!preloadedNews);

  useEffect(() => {
    // If the parent already fetched news (e.g. Dashboard loading all data
    // together), use it directly and skip the extra network call.
    if (preloadedNews) {
      setNews(preloadedNews);
      setLoading(false);
      return;
    }

    let isMounted = true;
    setLoading(true);

    api.getNewsIntelligence(symbol).then((data) => {
      if (isMounted) {
        setNews(data);
        setLoading(false);
      }
    });

    return () => {
      isMounted = false;
    };
  }, [symbol, preloadedNews]);

  const getSentimentDisplay = (sentiment) => {
    const s = (sentiment || 'Neutral').toLowerCase();
    if (s.includes('bull')) {
      return { icon: <TrendingUp className="w-5 h-5" />, color: 'text-green-400', badge: 'bg-green-500/20 border-green-500/30', emoji: '🟢' };
    }
    if (s.includes('bear')) {
      return { icon: <TrendingDown className="w-5 h-5" />, color: 'text-red-400', badge: 'bg-red-500/20 border-red-500/30', emoji: '🔴' };
    }
    return { icon: <Minus className="w-5 h-5" />, color: 'text-gray-400', badge: 'bg-gray-500/20 border-gray-500/30', emoji: '⚪' };
  };

  if (loading) {
    return (
      <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-2xl p-6 border border-gray-700 backdrop-blur-sm animate-pulse">
        <div className="h-32 flex items-center justify-center text-gray-400">
          <Newspaper className="w-6 h-6 mr-2 animate-pulse" />
          <p>Loading news intelligence...</p>
        </div>
      </div>
    );
  }

  if (!news || !news.available) {
    return (
      <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-2xl p-6 border border-gray-700 backdrop-blur-sm">
        <div className="flex items-center gap-3 mb-3">
          <Newspaper className="w-6 h-6 text-blue-400" />
          <h3 className="text-xl font-semibold text-white">News Intelligence</h3>
        </div>
        <p className="text-sm text-gray-400">
          {news?.message || 'News intelligence is not available right now.'}
        </p>
      </div>
    );
  }

  const sentimentDisplay = getSentimentDisplay(news.sentiment);

  return (
    <div className="bg-gradient-to-br from-gray-800/80 to-gray-900/80 rounded-2xl p-6 border border-gray-700 backdrop-blur-sm hover:border-gray-600 transition-all">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <Newspaper className="w-6 h-6 text-blue-400" />
          <h3 className="text-xl font-semibold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            News Intelligence
          </h3>
        </div>
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full border ${sentimentDisplay.badge}`}>
          <span>{sentimentDisplay.emoji}</span>
          <span className={`text-sm font-semibold ${sentimentDisplay.color}`}>
            {news.sentiment} {news.confidence ? `(${news.confidence}%)` : ''}
          </span>
        </div>
      </div>

      {/* Headlines */}
      {news.headlines && news.headlines.length > 0 && (
        <div className="mb-4">
          <p className="text-xs uppercase tracking-wide text-gray-500 mb-2">Latest Headlines</p>
          <ul className="space-y-1.5">
            {news.headlines.slice(0, 5).map((h, idx) => (
              <li key={idx} className="text-sm text-gray-300 flex items-start gap-2">
                <span className="text-gray-600 mt-0.5">•</span>
                {h.url ? (
                  <a
                    href={h.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-blue-400 transition-colors flex items-center gap-1"
                  >
                    {h.title}
                    <ExternalLink className="w-3 h-3 flex-shrink-0 opacity-50" />
                  </a>
                ) : (
                  <span>{h.title}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* AI Summary */}
      {news.summary && (
        <div className="mb-4">
          <p className="text-xs uppercase tracking-wide text-gray-500 mb-2">AI Summary</p>
          <p className="text-sm text-gray-300 leading-relaxed">{news.summary}</p>
        </div>
      )}

      {/* Risk Factors */}
      {news.risks && news.risks.length > 0 && (
        <div className="mb-4">
          <p className="text-xs uppercase tracking-wide text-gray-500 mb-2">Risk Factors</p>
          <ul className="space-y-1">
            {news.risks.map((risk, idx) => (
              <li key={idx} className="text-sm text-yellow-300 flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
                <span>{risk}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Overall Impact */}
      {news.impact && (
        <div className="pt-3 border-t border-gray-700">
          <p className="text-xs uppercase tracking-wide text-gray-500 mb-1">Overall Impact</p>
          <p className="text-sm text-gray-300">{news.impact}</p>
        </div>
      )}
    </div>
  );
};

export default NewsCard;