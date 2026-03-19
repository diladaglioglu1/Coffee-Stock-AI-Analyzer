import React from "react";
import {
  X,
  Sparkles,
  Package,
  DatabaseZap,
  CircleCheckBig,
  ShieldAlert,
} from "lucide-react";

const AnalysisModal = ({ open, onClose, analysis }) => {
  if (!open || !analysis) return null;

  const sourceLabelMap = {
    gemini: "Gemini",
    cache: "Cache",
    rate_limited: "Rate Limited",
    "ai-service": "AI Service",
  };

  const sourceLabel =
    sourceLabelMap[analysis.source] || analysis.source || "AI Service";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-md px-4">
      <div className="w-full max-w-2xl rounded-[2.5rem] bg-[#FDFBF9] shadow-2xl overflow-hidden border border-[#E9DED4]">
        <div className="px-10 py-8 border-b border-[#F2EDE8] flex justify-between items-center">
          <div>
            <p className="text-[10px] font-black uppercase tracking-[0.3em] text-[#D98E5E] mb-2">
              AI Optimization Result
            </p>
            <h2 className="text-3xl font-black text-[#1F1311] tracking-tighter">
              {analysis.product_name}
            </h2>
          </div>

          <button
            onClick={onClose}
            className="p-3 rounded-2xl bg-[#FAF7F2] border border-[#E9DED4] text-[#847B78] hover:bg-white transition-all"
          >
            <X size={20} />
          </button>
        </div>

        <div className="p-10 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="p-6 bg-[#FAF7F2] rounded-3xl border border-[#EEE4DA]">
              <div className="flex items-center gap-2 text-[#847B78] mb-3">
                <Package size={14} />
                <span className="text-[9px] font-black uppercase">Stock</span>
              </div>
              <p className="text-3xl font-black text-[#1F1311]">
                {analysis.current_stock}
                <span className="text-xs ml-2 uppercase text-[#847B78]">
                  {analysis.unit}
                </span>
              </p>
            </div>

            <div className="p-6 bg-[#FAF7F2] rounded-3xl border border-[#EEE4DA]">
              <div className="flex items-center gap-2 text-[#847B78] mb-3">
                <DatabaseZap size={14} />
                <span className="text-[9px] font-black uppercase">Source</span>
              </div>
              <p className="text-2xl font-black text-[#1F1311] uppercase">
                {sourceLabel}
              </p>
            </div>

            <div className="p-6 bg-[#FAF7F2] rounded-3xl border border-[#EEE4DA]">
              <div className="flex items-center gap-2 text-[#847B78] mb-3">
                <CircleCheckBig size={14} />
                <span className="text-[9px] font-black uppercase">Cache</span>
              </div>
              <p className="text-2xl font-black text-[#1F1311]">
                {analysis.cache_hit === null ? "Demo" : analysis.cache_hit ? "Hit" : "Miss"}
              </p>
            </div>
          </div>

          <div className="bg-[#1F1311] p-8 rounded-[2rem] relative">
            <div className="flex items-center gap-3 text-[#D98E5E] mb-4">
              <Sparkles size={18} />
              <span className="text-[10px] font-black uppercase tracking-widest">
                Advisory Insight
              </span>
            </div>

            <p className="text-[#E8DDDA] leading-8 text-sm font-medium">
              {analysis.advice}
            </p>
          </div>

          {analysis.rate_limited && (
            <div className="rounded-2xl border border-yellow-200 bg-yellow-50 p-4 flex items-start gap-3">
              <ShieldAlert size={18} className="text-yellow-600 mt-0.5" />
              <p className="text-sm text-yellow-800">
                The AI service is currently rate-limited. The displayed response
                may be a temporary fallback message.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AnalysisModal;