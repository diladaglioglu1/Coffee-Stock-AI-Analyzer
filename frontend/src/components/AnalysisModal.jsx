import React from "react";
import { X, Sparkles, Package, TrendingUp } from "lucide-react";

const AnalysisModal = ({ open, onClose, analysis }) => {
  if (!open || !analysis) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/45 backdrop-blur-sm px-4">
      <div className="w-full max-w-2xl rounded-[2rem] bg-[#FDFBF9] shadow-2xl border border-[#E9DED4] overflow-hidden">
        <div className="flex items-center justify-between px-8 py-6 border-b border-[#F2EDE8]">
          <div>
            <p className="text-[10px] font-black uppercase tracking-[0.3em] text-[#AFA19E] mb-2">
              AI Result
            </p>
            <h2 className="text-2xl font-black text-[#1F1311]">
              {analysis.product_name}
            </h2>
          </div>

          <button
            onClick={onClose}
            className="w-11 h-11 rounded-2xl border border-[#E9DED4] bg-white flex items-center justify-center text-[#847B78] hover:bg-[#FAF7F2] transition"
          >
            <X size={18} />
          </button>
        </div>

        <div className="p-8 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="rounded-2xl bg-[#FAF7F2] border border-[#EEE4DA] p-5">
              <div className="flex items-center gap-2 text-[#D98E5E] mb-2">
                <Package size={16} />
                <p className="text-[10px] uppercase font-black tracking-[0.3em]">
                  Current Stock
                </p>
              </div>
              <p className="text-3xl font-black text-[#1F1311]">
                {analysis.current_stock}
              </p>
            </div>

            <div className="rounded-2xl bg-[#FAF7F2] border border-[#EEE4DA] p-5">
              <div className="flex items-center gap-2 text-[#D98E5E] mb-2">
                <TrendingUp size={16} />
                <p className="text-[10px] uppercase font-black tracking-[0.3em]">
                  Average Daily Sales
                </p>
              </div>
              <p className="text-3xl font-black text-[#1F1311]">
                {analysis.average_daily_sales}
              </p>
            </div>
          </div>

          <div className="rounded-[1.5rem] bg-[#1F1311] p-6">
            <div className="flex items-center gap-3 text-[#D98E5E] mb-4">
              <Sparkles size={18} />
              <p className="text-[10px] uppercase font-black tracking-[0.3em]">
                Recommendation
              </p>
            </div>
            <p className="text-[#E8DDDA] leading-7">{analysis.recommendation}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisModal;